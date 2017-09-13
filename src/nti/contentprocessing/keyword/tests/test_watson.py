#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_key
from hamcrest import has_length
from hamcrest import assert_that

import fudge

import os
import unittest

import simplejson

from nti.contentprocessing.keyword import watson

from nti.contentprocessing.tests import SharedConfiguringTestLayer

class TestConceptTagger(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @property
    def sample(self):
        name = os.path.join(os.path.dirname(__file__), 'sample.txt')
        with open(name, "r") as f:
            return f.read()

    @property
    def response(self):
        name = os.path.join(os.path.dirname(__file__), 'response.json')
        with open(name, "r") as fp:
            return simplejson.load(fp)

    @fudge.patch('nti.contentprocessing.keyword.watson.analyze')
    def test_watson_keywords(self, mock_an):
        mock_an.is_callable().with_args().returns(self.response)
        terms = watson.get_keywords(self.sample)
        terms = {r.token: r.relevance for r in terms}
        assert_that(terms, has_length(20))
        assert_that(terms, has_key('knobby green objects'))
        assert_that(terms, has_key('blood cells'))
        assert_that(terms, has_key('red blood cells'))
