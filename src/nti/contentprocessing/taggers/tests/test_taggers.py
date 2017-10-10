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

from nti.contentprocessing.taggers import tag_word

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestTaggers(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_stem_word(self):
        assert_that(tag_word('virus'),
                    is_([('virus', 'NN')]))
