#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import os
import unittest
import platform

from nti.contentprocessing.keyword import term_extract_key_words

from nti.contentprocessing.tests import SharedConfiguringTestLayer


py_impl = getattr(platform, 'python_implementation', lambda: None)
IS_PYPY = py_impl() == 'PyPy'


@unittest.skipUnless(not IS_PYPY, 'PyPy not supported')
class TestKeyWordExtract(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @property
    def sample(self):
        name = os.path.join(os.path.dirname(__file__), 'sample.txt')
        with open(name, "r") as f:
            return f.read()

    def test_term_extract(self):
        terms = term_extract_key_words(self.sample)
        terms = [(r.token, r.frequency, r.strength) for r in terms]
        assert_that(sorted(terms),
                    is_(sorted([('blood', 4, 1),
                                ('virus', 3, 1),
                                ('blood vessel', 1, 2),
                                ('blood cells', 1, 2),
                                ('body works', 1, 2),
                                ('blood cells viruses', 1, 3)])))
