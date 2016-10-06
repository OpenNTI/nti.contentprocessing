#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_length
from hamcrest import assert_that

import os
import unittest

from nti.contentprocessing.taggers.standford import StanfordPostagger

from nti.contentprocessing.tests import SharedConfiguringTestLayer

class TestStandford(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_utility(self):
		source = os.path.join(os.path.dirname(__file__), 'source.tag')
		with open(source, "r") as fp:
			tags = StanfordPostagger.parse_tags(fp)
			assert_that(tags, has_length(301))
