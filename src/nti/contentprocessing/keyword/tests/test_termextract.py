#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property

import os
import unittest

from zope import component

from nti.contentprocessing.keyword import extract_key_words
from nti.contentprocessing.keyword import term_extract_key_words

from nti.contentprocessing.keyword.interfaces import IKeyWordExtractor

from nti.contentprocessing.keyword.termextract import NormRecord
from nti.contentprocessing.keyword.termextract import DefaultFilter

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestTermExtract(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @property
    def sample(self):
        name = os.path.join(os.path.dirname(__file__), 'sample.txt')
        with open(name, "r") as f:
            return f.read()

    def test_filter(self):
        df = DefaultFilter()
        assert_that(str(df), is_('DefaultFilter(2, 3)'))

    def test_normn_record(self):
        record = NormRecord('virus', 3, 1)
        assert_that(record,
                    has_property('relevance', is_(3)))

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

        assert_that(term_extract_key_words(self.sample, 'ru'),
                    is_(()))

        terms = term_extract_key_words(
            "And now for something completely Different")
        assert_that(terms, has_length(0))

        terms = term_extract_key_words(
            ["And",  "now",  "for", "something", "completely", "Different"]
        )
        assert_that(terms, has_length(0))

    def test_extract_key_words(self):
        terms = extract_key_words(self.sample, 'en')
        assert_that(terms, is_(()))

        class _MockExtractor(object):

            def __call__(self, unused):
                return ['1']

        mock = _MockExtractor()
        component.getGlobalSiteManager().registerUtility(mock, IKeyWordExtractor,
                                                         name='en')

        terms = extract_key_words(self.sample, 'en')
        assert_that(terms, is_(has_length(1)))

        component.getGlobalSiteManager().unregisterUtility(mock, IKeyWordExtractor,
                                                           name='en')
