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

import os
import unittest

from nti.contentprocessing.langdetection import detect_Language

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestModule(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @property
    def sample_en(self):
        name = os.path.join(os.path.dirname(__file__), 'sample_en.txt')
        with open(name, "r") as f:
            return f.read()

    def test_detect_Language(self):
        sample = self.sample_en
        lang = detect_Language(sample, 'no-detector')
        assert_that(lang, is_(none()))
        lang = detect_Language(sample, 'tika')
        assert_that(lang, is_not(none()))
