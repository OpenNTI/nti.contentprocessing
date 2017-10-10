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

from nti.contentprocessing.stemmers import stem_word

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestStemmer(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_stem_word(self):
        assert_that(stem_word(u'viruses', 'en', 'porter'), is_('virus'))
        assert_that(stem_word(u'viruses', 'en', 'foo'), is_('viruses'))
