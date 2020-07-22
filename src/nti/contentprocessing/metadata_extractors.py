#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Objects for extracting metadata from different content formats. This
includes support for local and remote PDF files and HTML using
OpenGraph metadata or Twitter card metadata.

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import six
import shutil
import string
import tempfile

import pyquery

import rdflib

import requests

import PyPDF2 as pyPdf

from six.moves import urllib_parse

from zope import component
from zope import interface

from zope.cachedescriptors.property import Lazy

from zope.location.interfaces import IContained

from zope.mimetype.interfaces import IMimeTypeGetter
from zope.mimetype.interfaces import IContentTypeAware

from nti.contentprocessing._compat import text_

from nti.contentprocessing.interfaces import IImageMetadata
from nti.contentprocessing.interfaces import IContentMetadata
from nti.contentprocessing.interfaces import IContentMetadataExtractor
from nti.contentprocessing.interfaces import IContentMetadataURLHandler

from nti.property.property import alias

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import PermissiveSchemaConfigured

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IImageMetadata, IContained, IContentTypeAware)
class ImageMetadata(PermissiveSchemaConfigured):
    """
    Default implementation of :class:`.IImageMetadata`
    """

    __name__ = None
    __parent__ = None

    __external_class_name__ = "ImageMetadata"
    mime_type = mimeType = 'application/vnd.nextthought.metadata.imagemetadata'

    createDirectFieldProperties(IImageMetadata)


@interface.implementer(IContentMetadata, IContained, IContentTypeAware)
class ContentMetadata(PermissiveSchemaConfigured):
    """
    Default implementation of :class:`.IContentMetadata`
    """

    __name__ = None
    __parent__ = None

    __external_class_name__ = "ContentMetadata"
    mime_type = mimeType = 'application/vnd.nextthought.metadata.contentmetadata'

    createDirectFieldProperties(IContentMetadata, adapting=True)

    # BWC
    href = alias('contentLocation')


class _abstract_args(object):

    __name__ = None
    text = None

    @Lazy
    def pyquery_dom(self):
        return pyquery.PyQuery(url=self.__name__,
                               opener=lambda unused_url, **unused_kwgs: self.text)


class _request_args(_abstract_args):

    def __init__(self, url, response):
        self.__name__ = url
        self.response = response
        self.download_path = None

    def stream(self):
        return self.response.raw

    @Lazy
    def bidirectionalstream(self):
        fd, pdf_path = tempfile.mkstemp('.metadata', 'download')
        self.download_path = pdf_path
        pdf_file = os.fdopen(fd, 'wb')
        shutil.copyfileobj(self.response.raw, pdf_file)
        pdf_file.close()
        return open(pdf_path, 'rb')

    @property
    def text(self):
        return self.response.text

    @property
    def bytes(self):
        return self.response.content


class _file_args(_abstract_args):

    def __init__(self, path):
        self.path = path
        self.__name__ = path

    @Lazy
    def stream(self):
        return open(self.path, 'rb')
    bidirectionalstream = stream

    @Lazy
    def text(self):
        with open(self.path, 'r') as f:
            return text_(f.read())

    @Lazy
    def bytes(self):
        with open(self.path, 'r') as f:
            return f.read()


def _get_metadata_from_mime_type(location, mime_type, args_factory):
    args = None
    result = None
    processor = None

    if mime_type:
        processor = component.queryUtility(IContentMetadataExtractor,
                                           name=mime_type)
    if processor:
        args = args_factory()
        result = processor.extract_metadata(args)
    else:
        logger.warning('No processor found for mime_type %s', mime_type)

    if result is not None:
        result.sourceLocation = text_(location)
        result.contentMimeType = text_(mime_type)

    return result, args

# NOTE: See also https://github.com/coleifer/micawber
# for a library to find metadata about all kinds of things including
# youtube videos, etc


def _get_metadata_from_url(urlscheme, location):
    # 1) Need to redirect here based on url scheme
    schemehandler = component.queryUtility(IContentMetadataURLHandler,
                                           name=urlscheme)
    if schemehandler is not None:
        return schemehandler(location)


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"


def _http_scheme_handler(location):
    # Must use requests, not the url= argument, as
    # the default Python User-Agent is blocked
    # (note: pyquery 1.2.4 starts using requests internally by default)
    # The custom user-agent string is to trick Google into sending UTF-8.
    response = requests.get(location,
                            headers={
                                'User-Agent': USER_AGENT
                            },
                            stream=True)
    # Get the content type, splitting off encoding, etc
    mime_type = response.headers.get('content-type').split(';', 1)[0]

    result, args = _get_metadata_from_mime_type(
        location, mime_type, lambda: _request_args(location, response)
    )

    if result is not None:
        result.sourcePath = text_(args.download_path)
    return result
interface.directlyProvides(_http_scheme_handler, IContentMetadataURLHandler)


def _get_metadata_from_path(location):
    mime_type = component.getUtility(IMimeTypeGetter)(name=location)
    result, _ = _get_metadata_from_mime_type(location,
                                             mime_type,
                                             lambda: _file_args(location))

    if result is not None:
        result.sourcePath = text_(location)
    return result


def get_metadata_from_http_url(url):
    """
    Given a remote http or https url attempt to extract metadata
    from it and return an :class:`.IContentMetadata` object.

    Unlike get_metadata_from_content_location which may check local files
    or allow urls with other schemes a url with scheme other than http or https
    will raise a ValueError
    """

    urlscheme = urllib_parse.urlparse(url).scheme
    if urlscheme and urlscheme.startswith('http'):
        return _get_metadata_from_url(urlscheme, url)
    else:
        raise ValueError('unsupported url scheme', urlscheme)


def get_metadata_from_content_location(location):
    """
    Given the location of a piece of content (i.e., an HTML file or PDF),
    attempt to extract metadata from it and return an :class:`.IContentMetadata` object.

    This function will attempt to determine if the location is a local
    file or a URL of some sort. If it is a URL, it will query for a
    `URL handler` and pass it off to that. If it is a file, it will attempt
    to determine the file type from the filename.
    """

    # Is it a URL and not a local file (taking care not
    # to treat windoze paths like "c:\foo" as URLs)
    urlscheme = urllib_parse.urlparse(location).scheme
    if urlscheme and (len(urlscheme) != 1 or urlscheme not in string.ascii_letters):
        # look up a handler for the scheme and pass it over.
        # this lets us delegate responsibility for schemes we
        # can't access, like tag: schemes for NTIIDs
        return _get_metadata_from_url(urlscheme, location)

    # Ok, assume a local path.
    return _get_metadata_from_path(location)


@interface.implementer(IContentMetadataExtractor)
class _HTMLExtractor(object):

    def extract_metadata(self, args):
        result = ContentMetadata()
        # Extract metadata. Need to handle OpenGraph
        # as well as twitter, with a final fallback to some
        # page attributes
        result = self._extract_opengraph(result, args)
        result = self._extract_twitter(result, args)
        result = self._extract_page(result, args)
        return result

    def _extract_opengraph(self, result, args):
        # The opengraph metadata is preferred if we can get
        # it. It may have one of two different
        # namespaces, depending on the data:
        # http://opengraphprotocol.org/schema/
        # http://ogp.me/ns#
        graph = rdflib.Graph()
        # The arguments to parse are quite sensitive.
        # If we are not careful, it can wind up trying
        # to re-open the URL and using
        # the wrong data or content type. Thus,
        # we do not provide the location argument,
        # and we do force the media type.
        graph.parse(data=args.text, format='rdfa',
                    publicID=args.__name__, media_type='text/html')

        nss = (rdflib.Namespace('http://ogp.me/ns#'),
               rdflib.Namespace('http://opengraphprotocol.org/schema/'))

        pairs = (('title', 'title'), ('url', 'href'), ('image', 'image'),
                 ('description', 'description'))

        for ns_name, attr_name in pairs:
            # Don't overwrite
            if getattr(result, attr_name, None):
                continue

            triples = graph.triples_choices(
                (None, [getattr(x, ns_name) for x in nss], None)
            )

            for _, _, val in triples:
                val = val.toPython()
                if isinstance(val, six.string_types):
                    val = text_(val)
                if ns_name == 'image':
                    if not result.images:
                        result.images = []
                    image = ImageMetadata(url=val)
                    image.__parent__ = result
                    # pylint: disable=no-member
                    image.__name__ = image.url
                    # NOTE: If there are multiple image elements,
                    # their relative order is not retained. This means
                    # that if they provide height and width values,
                    # we have no way to associate that with them.
                    # We can only do it if there is exactly one image.
                    result.images.append(image)
                else:
                    setattr(result, attr_name, val)
                    break

        if len(result.images) == 1:
            for k in 'height', 'width':
                triples = graph.triples_choices(
                    (None, [getattr(x, 'image:' + k) for x in nss], None)
                )
                for _, _, val in triples:
                    setattr(result.images[0], k, int(val.toPython()))
        return result

    def _extract_twitter(self, result, args):
        # Get the twitter card metadata. Stupid twitter cards
        # are "similar to OpenGraph", except that they are not
        # valid RDFa for no apparent reason, so they don't actually
        # have a namespace, just a prefix. idiots. Fortunately,
        # twitter will parse OG if present, which it usually seems to
        # be. Thus the stupid twitter metadata is only a fallback.

        # { meta: attr }
        prop_names = {'twitter:description': 'description',
                      'twitter:title': 'title',
                      'twitter:url': 'href'}

        dom = args.pyquery_dom
        for meta in dom.find('meta'):
            name = meta.get('name')
            val = meta.get('content')

            if name and val:
                val = text_(val)
                if name in prop_names:
                    attr_name = prop_names[name]
                    if not getattr(result, attr_name, None):
                        setattr(result, attr_name, val)
                elif name == 'twitter:image':
                    if not result.images:
                        result.images = []
                    image = ImageMetadata(url=val)
                    # pylint: disable=no-member
                    image.__name__ = image.url
                    image.__parent__ = result
                    result.images.append(image)
        return result

    def _extract_page(self, result, args):
        if not result.creator:
            # The typical case of the name is author, but there is evidence that
            # Author is also used. The spec claims these meta names are case insensitive
            # but the syntax we query with is not.
            for attr in ('author', 'Author'):
                meta = args.pyquery_dom('meta[name=%s]' % (attr),)
                text = meta.attr['content'] if meta else ''
                if text:
                    result.creator = text_(text)
                    break
        if not result.description:
            meta = args.pyquery_dom('meta[name=description]')
            text = meta.attr['content'] if meta else ''
            if text:
                result.description = text_(text)
        if not result.title:
            title = args.pyquery_dom('title')
            text = title.text()
            if text:
                result.title = text_(text)
        return result


@interface.implementer(IContentMetadataExtractor)
class _PDFExtractor(object):

    def extract_metadata(self, args):
        # pyPdf is a streaming parser. It only
        # has to load the xref table from the end of the stream initially,
        # and then objects are loaded on demand from the (seekable!)
        # stream. Thus, even for very large PDFs, it uses
        # minimal memory.
        result = ContentMetadata()
        pdf = pyPdf.PdfFileReader(args.bidirectionalstream)
        info = pdf.getDocumentInfo()  # NOTE: Also check the xmpMetadata?
        # This dict is weird: [] and get() return different things,
        # with [] returning the strings we want
        # pylint: disable=attribute-defined-outside-init
        if '/Title' in info and info['/Title']:
            result.title = text_(info['/Title'])
        if '/Author' in info and info['/Author']:
            result.creator = text_(info['/Author'])
        if '/Subject' in info and info['/Subject']:
            result.description = text_(info['/Subject'])
        return result
