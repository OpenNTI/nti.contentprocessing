#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import has_property

import fudge
import os.path
import unittest

from nti.contentprocessing.metadata_extractors import ContentMetadata
from nti.contentprocessing.metadata_extractors import get_metadata_from_content_location

from nti.contentprocessing.interfaces import IContentMetadata

from nti.contentprocessing.tests import SharedConfiguringTestLayer

from nti.testing.matchers import validly_provides

class TestMetadataExtractors(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_metadata_provides(self):
		metadata = ContentMetadata()
		assert_that(metadata, validly_provides(IContentMetadata))

	@fudge.patch('requests.get')
	def test_extraction_remote_pdf(self, fake_get=None):
		# By commenting out the patch line, we can test with a real file
		if fake_get is not None:
			# This real URL has been download locally
			pdf_file = os.path.join(os.path.dirname(__file__), 'test_page574_12.pdf')

			class R1(object):
				def __init__(self):
					self.headers = {'content-type': 'application/pdf'}
					self.raw = open(pdf_file, 'rb')

			fake_get.is_callable().returns(R1())
			href = 'http://someserver.com/path/to/test_page574_12.pdf'  # remote href
		else:
			href = 'http://support.pokemon.com/FileManagement/Download/f6029520f8ea43f08790ec4975944bb3'

		result = get_metadata_from_content_location(href)

		# Values from the PDF
		assert_that(result, has_property('creator', 'Jason Madden'))
		assert_that(result, has_property('description', 'Subject'))
