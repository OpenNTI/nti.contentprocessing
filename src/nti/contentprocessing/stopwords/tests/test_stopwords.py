#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.contentprocessing.stopwords import NoStopWords


class TestStopWords(unittest.TestCase):

    def test_no_stop_words(self):
        m = NoStopWords()
        assert_that(m.stopwords(), is_(()))
        assert_that(m.available_languages(),
                    is_(('en', 'es', 'ru')))
