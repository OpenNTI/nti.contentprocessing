#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.contentprocessing.stopwords import _FileBasedStopWords

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestStopWords(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_queryobject_ctor(self):
        util = _FileBasedStopWords()
        assert_that(util.available_languages(), has_length(15))
        words = util.stopwords('en')
        assert_that(words, has_length(33))
        words = util.stopwords('zh')
        assert_that(words, has_length(119))
        words = util.stopwords('ru')
        assert_that(words, has_length(421))
