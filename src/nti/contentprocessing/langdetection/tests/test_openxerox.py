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

import os
import fudge
import unittest

from nti.contentprocessing.langdetection.openxerox import _OpenXeroxLanguageDetector

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestOpenXeroxLangDetector(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @property
    def sample_en(self):
        name = os.path.join(os.path.dirname(__file__), 'sample_en.txt')
        with open(name, "r") as f:
            return f.read()

    @fudge.patch('requests.post')
    def test_lang_detector(self, mock_post):
        res = fudge.Fake().provides("json").calls(lambda: 'en')
        res.has_attr(status_code=200)
        mock_post.is_callable().returns(res)

        detector = _OpenXeroxLanguageDetector()
        lang = detector(self.sample_en)
        assert_that(lang, is_not(none()))
        assert_that(lang, has_property('code', is_('en')))

        res = fudge.Fake().provides("json").calls(lambda: 'en')
        res.has_attr(status_code=500)
        mock_post.is_callable().returns(res)

        lang = detector(self.sample_en)
        assert_that(lang, is_(none()))

        mock_post.is_callable().raises(IOError())
        lang = detector(self.sample_en)
        assert_that(lang, is_(none()))
