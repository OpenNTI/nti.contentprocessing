#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Objects for extracting metadata from different content formats. This
includes support for local and remote PDF files and HTML using
OpenGraph metadata or Twitter card metadata.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import six
import shutil
import string
import pyquery
import requests
import tempfile
import urlparse
import PyPDF2 as pyPdf

from zope import component
from zope import interface

from zope.cachedescriptors.property import Lazy

from zope.location.interfaces import IContained

from zope.mimetype.interfaces import IMimeTypeGetter

from nti.common.property import alias

from nti.schema.schema import PermissiveSchemaConfigured
from nti.schema.fieldproperty import createDirectFieldProperties

from .interfaces import IImageMetadata
from .interfaces import IContentMetadata
from .interfaces import IContentMetadataExtractor
from .interfaces import IContentMetadataURLHandler

@interface.implementer(IImageMetadata, IContained)
class ImageMetadata(PermissiveSchemaConfigured):
	"""
	Default implementation of :class:`.IImageMetadata`
	"""

	__name__ = None
	__parent__ = None

	createDirectFieldProperties(IImageMetadata)

@interface.implementer(IContentMetadata, IContained)
class ContentMetadata(PermissiveSchemaConfigured):
	"""
	Default implementation of :class:`.IContentMetadata`
	"""

	__name__ = None
	__parent__ = None

	createDirectFieldProperties(IContentMetadata, adapting=True)

	# BWC
	href = alias('contentLocation')

class _abstract_args(object):

	__name__ = None
	text = None

	@Lazy
	def pyquery_dom(self):
		return pyquery.PyQuery(url=self.__name__, opener=lambda url, **kwargs: self.text)

class _request_args(_abstract_args):

	def __init__(self, url, response):
		self.response = response
		self.__name__ = url
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
			return f.read().decode('utf-8')

	@Lazy
	def bytes(self):
		with open(self.path, 'r') as f:
			return f.read()

def _get_metadata_from_mime_type(location, mime_type, args_factory):

	processor = None
	args = None
	result = None

	if mime_type:
		processor = component.queryUtility(IContentMetadataExtractor,
										   name=mime_type)
	if processor:
		args = args_factory()
		result = processor.extract_metadata(args)

	if result is not None:
		result.sourceLocation = location
		result.mimeType = six.text_type(mime_type)

	return result, args

# NOTE: See also https://github.com/coleifer/micawber
# for a library to find metadata about all kinds of things including youtube videos, etc

def _get_metadata_from_url(urlscheme, location):
	# TODO: Need to redirect here based on url scheme

	schemehandler = component.queryUtility(IContentMetadataURLHandler,
										   name=urlscheme)
	if schemehandler is not None:
		return schemehandler(location)

def _http_scheme_handler(location):
	# Must use requests, not the url= argument, as
	# the default Python User-Agent is blocked (note: pyquery 1.2.4 starts using requests internally by default)
	# The custom user-agent string is to trick Google into sending UTF-8.
	response = requests.get(location,
							 headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"},
							 stream=True)
	# Get the content type, splitting off encoding, etc
	mime_type = response.headers.get('content-type').split(';', 1)[0]

	result, args = \
		 _get_metadata_from_mime_type(
					location, mime_type, lambda: _request_args(location, response))

	if result is not None:
		result.sourcePath = args.download_path
	return result
interface.directlyProvides(_http_scheme_handler, IContentMetadataURLHandler)

def _get_metadata_from_path(location):
	mime_type = component.getUtility(IMimeTypeGetter)(name=location)
	result, _ = _get_metadata_from_mime_type(location, mime_type, lambda: _file_args(location))

	if result is not None:
		result.sourcePath = location

	return result

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
	urlscheme = urlparse.urlparse(location).scheme
	if urlscheme and (len(urlscheme) != 1 or urlscheme not in string.ascii_letters):
		# look up a handler for the scheme and pass it over.
		# this lets us delegate responsibility for schemes we
		# can't access, like tag: schemes for NTIIDs
		return _get_metadata_from_url(urlscheme, location)

	# Ok, assume a local path.
	return _get_metadata_from_path(location)

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
		info = pdf.getDocumentInfo()  # TODO: Also check the xmpMetadata?
		# This dict is weird: [] and get() return different things,
		# with [] returning the strings we want
		if '/Title' in info and info['/Title']:
			result.title = info['/Title']
		if '/Author' in info and info['/Author']:
			result.creator = info['/Author']
		if '/Subject' in info and info['/Subject']:
			result.description = info['/Subject']
		return result
