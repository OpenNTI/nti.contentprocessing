#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import contains
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import has_properties
from hamcrest import contains_inanyorder

from nti.testing.matchers import validly_provides

import os.path
import unittest

import fudge

import pyquery

from rdflib import Graph

from zope.cachedescriptors.property import Lazy

from nti.contentprocessing.metadata_extractors import _HTMLExtractor
from nti.contentprocessing.metadata_extractors import ContentMetadata

from nti.contentprocessing.metadata_extractors import _file_args
from nti.contentprocessing.metadata_extractors import _request_args
from nti.contentprocessing.metadata_extractors import _get_metadata_from_mime_type

from nti.contentprocessing.metadata_extractors import get_metadata_from_http_url
from nti.contentprocessing.metadata_extractors import get_metadata_from_content_location

from nti.contentprocessing.interfaces import IContentMetadata

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestMetadataExtractors(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_metadata_provides(self):
        metadata = ContentMetadata()
        assert_that(metadata, validly_provides(IContentMetadata))

    def test_opengraph_extraction_from_file(self):
        # Originally from NewYorker
        # http://www.newyorker.com/reporting/2013/01/07/130107fa_fact_green?currentPage=all
        the_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               u'og_metadata.html'))

        graph = Graph()
        graph.parse(the_file, format='rdfa')

        args = _file_args(the_file)

        def _check(result):
            assert_that(result,
                        has_property('title',
                                     'Adam Green: The Spectacular Thefts of Apollo Robbins, Pickpocket'))
            assert_that(result,
                        has_property('href',
                                     'http://www.newyorker.com/reporting/2013/01/07/130107fa_fact_green'))
            assert_that(result,
                        has_property('images',
                                     contains(has_property('url',
                                                           'http://www.newyorker.com/images/2013/01/07/g120/130107_r23011_g120_cropth.jpg'))))

            assert_that(result, validly_provides(IContentMetadata))

        extractor = _HTMLExtractor()
        result = extractor._extract_opengraph(ContentMetadata(), args)
        _check(result)
        
        result = extractor._extract_opengraph(result, args)
        assert_that(result,
                    has_property('title',
                                 'Adam Green: The Spectacular Thefts of Apollo Robbins, Pickpocket'))

        result.title = None
        result = extractor._extract_page(result, args)
        assert_that(result,
                    has_property('title',
                                 'Adam Green: The Spectacular Thefts of Apollo Robbins, Pickpocket : The New Yorker'))

        get_metadata_from_content_location(the_file)
      
    def test_twitter_extraction_from_file(self):
        # Originally from NYTimes:
        # https://www.nytimes.com/2013/05/17/health/exercise-class-obedience-not-required.html
        the_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                u'twitter_metadata.html'))

        graph = Graph()
        graph.parse(the_file, format='rdfa')

        args = _file_args(the_file)

        def _check(result):
            assert_that(result,
                        has_property('title', 'Exercise Class, Obedience Not Required'))
            assert_that(result,
                        has_property('href', 'http://www.nytimes.com/2013/05/17/health/exercise-class-obedience-not-required.html'))
            assert_that(result,
                        has_property('images',
                                     contains(has_property('url',
                                                           'http://graphics8.nytimes.com/images/2013/05/17/arts/17URBAN_SPAN/17URBAN_SPAN-thumbLarge-v2.jpg'))))
            assert_that(result, validly_provides(IContentMetadata))

        result = _HTMLExtractor()._extract_twitter(ContentMetadata(), args)
        _check(result)
        
        # pylint: disable=not-context-manager
        with args.stream as f:
            assert_that(f.read(), is_not(none()))
            
        assert_that(args.bytes, is_not(none()))

    def test_opengraph_extraction(self):
        template = """
        <html %s>
        <head>
        <title>The Rock (1996)</title>
        <meta property="og:title" content="The Rock" />
        <meta property="og:type" content="video.movie" />
        <meta property="og:url" content="http://www.imdb.com/title/tt0117500/" />
        <meta property="og:image" content="http://ia.media-imdb.com/images/rock.jpg" />

        <meta property="og:image:width" content="300" />
        <meta property="og:image:height" content="400" />

        </head>

        </html>"""

        class _args(object):
            __name__ = None
            text = None

        # No explicit prefix (relying on default in RDFa 1.1), an HTML5-style prefix,
        # and the XML style prefix
        for prefix in '', 'prefix="og: http://ogp.me/ns#"', 'xmlns:og="http://opengraphprotocol.org/schema/"':
            html = template % prefix
            __traceback_info__ = html  # pylint: disable=unused-variable
            args = _args()
            args.__name__ = u'http://example.com'
            args.text = html

            result = _HTMLExtractor()._extract_opengraph(ContentMetadata(), args)

            assert_that(result, has_property('title', 'The Rock'))
            assert_that(result,
                        has_property('href', 'http://www.imdb.com/title/tt0117500/'))
            # For one image, we can preserve the width and height, if given
            assert_that(result,
                        has_property('images',
                                     contains(has_properties(
                                         'url', 'http://ia.media-imdb.com/images/rock.jpg',
                                         'width', 300,
                                                'height', 400))))
            assert_that(result, validly_provides(IContentMetadata))

    def test_opengraph_extraction_multiple_images(self):
        template = """
        <html %s>
        <head>
        <title>The Rock (1996)</title>
        <meta property="og:title" content="The Rock" />
        <meta property="og:type" content="video.movie" />
        <meta property="og:url" content="http://www.imdb.com/title/tt0117500/" />

        <meta property="og:image" content="http://example.com/rock.jpg" />
        <meta property="og:image:width" content="300" />
        <meta property="og:image:height" content="300" />
        <meta property="og:image" content="http://example.com/rock2.jpg" />
        <meta property="og:image" content="http://example.com/rock3.jpg" />
        <meta property="og:image:height" content="1000" />
        <meta property="og:image:width" content="1000" />
        """

        class _args(object):
            __name__ = None
            text = None

        for prefix in '', 'prefix="og: http://ogp.me/ns#"', 'xmlns:og="http://opengraphprotocol.org/schema/"':
            html = template % prefix
            __traceback_info__ = html  # pylint: disable=unused-variable
            args = _args()
            args.__name__ = u'http://example.com'
            args.text = html

            result = _HTMLExtractor()._extract_opengraph(ContentMetadata(), args)

            assert_that(result, has_property('title', 'The Rock'))
            assert_that(result,
                        has_property('href', 'http://www.imdb.com/title/tt0117500/'))
            # Sadly, order is not preserved
            assert_that(result, has_property('images',
                                             contains_inanyorder(has_property('url', 'http://example.com/rock.jpg'),
                                                                 has_property('url', 'http://example.com/rock2.jpg'),
                                                                 has_property('url', 'http://example.com/rock3.jpg'))))

    @fudge.patch('requests.get')
    def test_extraction_remote_pdf(self, fake_get):
        pdf_file = os.path.join(os.path.dirname(__file__),
                                u'test_page574_12.pdf')

        class R1(object):

            def __init__(self):
                self.headers = {'content-type': 'application/pdf'}
                self.raw = open(pdf_file, 'rb')

        fake_get.is_callable().returns(R1())
        # remote href
        href = u'http://someserver.com/path/to/test_page574_12.pdf'
        result = get_metadata_from_content_location(href)

        # Values from the PDF
        assert_that(result, has_property('creator', 'Jason Madden'))
        assert_that(result, has_property('description', 'Subject'))

    def test_request_args(self):
        response = fudge.Fake().has_attr(raw=b'').has_attr(text=u'').has_attr(content=b'')
        r = _request_args('http://nti.org', response)
        assert_that(r.stream(), is_(b''))
        assert_that(r, 
                    has_properties('text', is_(u''),
                                   'bytes', is_(b'')))
        
    @fudge.patch('nti.contentprocessing.metadata_extractors._get_metadata_from_url')
    def test_get_metadata_from_http_url(self, mock_gmh):
        mock_gmh.is_callable().returns(True)
        assert_that(get_metadata_from_http_url('https://bleach.org'),
                    is_(True))
        with self.assertRaises(ValueError):
            get_metadata_from_http_url('ftp://bleach.org')

    def test_extract_from_html_props(self):
        template = """
        <html %s>
        <head>
        <title>The Rock (1996)</title>
        <meta name="description" content="Free Web tutorials">
        <meta name="keywords" content="HTML,CSS,JavaScript">
        <meta name="author" content="John Doe">
        </head>

        </html>"""

        class _args(object):
            __name__ = None
            text = None

            @Lazy
            def pyquery_dom(self):
                return pyquery.PyQuery(self.text)
                

        args = _args()
        args.__name__ = u'http://example.com'
        args.text = template

        result = _HTMLExtractor()._extract_page(ContentMetadata(), args)

        assert_that(result, has_property('creator', 'John Doe'))
        assert_that(result, has_property('title', 'The Rock (1996)'))
        assert_that(result, has_property('description', 'Free Web tutorials'))

    def test_coverage(self):
        assert_that(_get_metadata_from_mime_type(None, None, None),
                    is_((None, None)))
        
