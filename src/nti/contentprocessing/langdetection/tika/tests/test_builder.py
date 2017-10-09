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
from hamcrest import equal_to
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property

import os
import gzip
import shutil
import tempfile
import unittest
from six import StringIO

from nti.contentprocessing.langdetection.tika.builder import NGramEntry
from nti.contentprocessing.langdetection.tika.builder import QuickStringBuffer
from nti.contentprocessing.langdetection.tika.builder import LanguageProfilerBuilder

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestBuilder(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_quick_string_buffer(self):
        qsb = QuickStringBuffer("ichigo")
        assert_that(qsb, is_('ichigo'))
        assert_that(qsb, is_(equal_to(QuickStringBuffer("ichigo"))))
        assert_that(qsb, has_length(6))
        assert_that(str(qsb), is_('ichigo'))
        assert_that(list(qsb), is_(['i', 'c', 'h', 'i', 'g', 'o']))

        assert_that(qsb[0:4], is_(['i', 'c', 'h', 'i']))
        assert_that(qsb.subSequence(0, 4), is_('ichi'))

        qsb.append(" Kurosaki")
        assert_that(str(qsb), is_('ichigo Kurosaki'))

        qsb = qsb.lower()
        assert_that(str(qsb), is_('ichigo kurosaki'))

        assert_that(qsb.charAt(-1), is_('i'))

        assert_that(hash(qsb), is_not(none()))

        assert_that(QuickStringBuffer("ichigo"),
                    is_(equal_to(QuickStringBuffer("ichigo"))))

    def test_ngram_entry(self):
        a = NGramEntry("ichigo", 10)
        assert_that(a, has_length(6))
        assert_that(a, has_property('count', 10))
        assert_that(a, has_property('seq', is_('ichigo')))
        # coverage
        str(a)
        repr(a)
        hash(a)

        # comp
        b = NGramEntry("zaraki", 3)
        assert_that(a.__lt__(b), is_(True))

        assert_that(a, is_not(equal_to(b)))

        a.frequency = 10
        b.frequency = 1
        assert_that(b.__gt__(a), is_(False))

        # constructor
        a = NGramEntry(QuickStringBuffer("ichigo"), 10)
        assert_that(a, has_length(6))

    def test_builder(self):
        lp = LanguageProfilerBuilder()

        # load
        source = os.path.join(os.path.dirname(__file__), 'en.ngp')
        assert_that(lp.load(source), is_(14))
        assert_that(lp, has_property('sorted', has_length(14)))
        assert_that(lp.getSimilarity(lp), is_(0))

        # coverage
        assert_that(lp._add_cs(lp.SEP_CHARSEQ), is_(False))

        lp.add('ichigo')
        with self.assertRaises(ValueError):
            lp.add(None)

        lp.analyze('ichigo')
        lp.analyze('aizen')

        other = LanguageProfilerBuilder()
        assert_that(other.getSimilarity(lp),  is_(1))
        assert_that(lp.getSimilarity(other),  is_(1))

        lp.save(StringIO())

    def test_create_builder(self):
        source = os.path.join(os.path.dirname(__file__), 'welsh_corpus.txt.gz')
        source = gzip.GzipFile(source)
        profile = LanguageProfilerBuilder.create("test", source)
        try:
            outdir = tempfile.mkdtemp(dir="/tmp")
            target = os.path.join(outdir, "out.ngp")
            profile.save(target)
            assert_that(profile.sorted, has_length(1000))
        finally:
            shutil.rmtree(outdir, True)
