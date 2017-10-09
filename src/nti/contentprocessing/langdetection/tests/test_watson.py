#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import fudge

import os
import unittest

import simplejson

from nti.contentprocessing.langdetection.interfaces import IWatsonLanguage

from nti.contentprocessing.langdetection.watson import WatsonLanguage
from nti.contentprocessing.langdetection.watson import _WatsonTextLanguageDetector

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestWatsonLangDetector(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @property
    def sample_en(self):
        name = os.path.join(os.path.dirname(__file__), 'sample_en.txt')
        with open(name, "r") as f:
            return f.read()

    @property
    def response(self):
        name = os.path.join(os.path.dirname(__file__), 'response.json')
        with open(name, "r") as fp:
            return simplejson.load(fp)

    @fudge.patch('nti.contentprocessing.langdetection.watson.identify')
    def test_watson_detector(self, mock_id):
        mock_id.is_callable().with_args().returns(self.response)
        lang = _WatsonTextLanguageDetector.detect(self.sample_en, 'translator')
        assert_that(lang, is_not(none()))
        assert_that(lang, has_property('code', is_('en')))
        assert_that(lang, has_property('confidence', is_(1.0)))

    def test_watson_language(self):
        a = WatsonLanguage(code=u'en', confidence=0.98)
        assert_that(a, validly_provides(IWatsonLanguage))
        assert_that(a, verifiably_provides(IWatsonLanguage))
