#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that

import unittest

import fudge

from six import unichr as _unichr

from zope import component

from nti.contentfragments.interfaces import IPunctuationMarkPattern
from nti.contentfragments.interfaces import IPunctuationMarkExpression
from nti.contentfragments.interfaces import IPunctuationMarkPatternPlus
from nti.contentfragments.interfaces import IPunctuationMarkExpressionPlus

from nti.contentprocessing.content_utils import normalize
from nti.contentprocessing.content_utils import rank_words
from nti.contentprocessing.content_utils import get_content
from nti.contentprocessing.content_utils import sent_tokenize
from nti.contentprocessing.content_utils import tokenize_content
from nti.contentprocessing.content_utils import clean_special_characters
from nti.contentprocessing.content_utils import get_content_translation_table

from nti.contentprocessing.content_utils import _SequenceMatcherWordSimilarity

from nti.contentprocessing.interfaces import IWordTokenizerPattern
from nti.contentprocessing.interfaces import IWordTokenizerExpression

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestContentUtils(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    sample_words = (u"alfa", u"bravo", u"charlie", u"delta", u"echo")

    def test_normalize(self):
        assert_that(normalize(u'alpha\t\nbravoﾖ'), is_(u'alpha bravo\uff96'))

    def test_split_conent(self):
        assert_that(tokenize_content(None), is_(()))

        s = u'ax+by=0'
        assert_that(tokenize_content(s), is_(['ax', 'by', '0']))

        s = u':)'
        assert_that(tokenize_content(s), is_([]))

        s = u"''''''''"
        assert_that(tokenize_content(s), is_([]))

    def test_get_content(self):
        assert_that(get_content(None), is_(u''))
        assert_that(get_content({}), is_(u''))
        assert_that(get_content(u'Zanpakuto Zangetsu'),
                    is_('Zanpakuto Zangetsu'))
        assert_that(get_content(u'\n\tZanpakuto,Zangetsu'),
                    is_('Zanpakuto Zangetsu'))
        assert_that(get_content(u'<html><b>Zangetsu</b></html>'),
                    is_('Zangetsu'))
        assert_that(get_content('orange-haired'), is_('orange-haired'))

        assert_that(get_content(u'U.S.A. vs Japan'), is_('U.S.A. vs Japan'))
        assert_that(get_content(u'$12.45'), is_('$12.45'))
        assert_that(get_content(u'82%'), is_('82%'))

        u = _unichr(40960) + u'bleach' + _unichr(1972)
        assert_that(get_content(u), is_(u'\ua000bleach'))

    def test_clean_special(self):
        source = u'Zanpakuto Zangetsu'
        assert_that(clean_special_characters(source), is_(source))

        source = u'?*?.\\+(ichigo^^{['
        assert_that(clean_special_characters(source), is_('ichigo'))

    def test_rank_words(self):
        terms = sorted(self.sample_words)
        word = u'stranger'
        w = rank_words(word, terms)
        assert_that(sorted(w),
                    is_(sorted([u'bravo', u'delta', u'charlie', u'alfa', u'echo'])))

    def test_content_translation_table(self):
        table = get_content_translation_table()
        assert_that(table, has_length(605))
        s = u'California Court of Appeal\u2019s said Bushman may \u2026be guilty of disturbing the peace through \u2018offensive\u2019'
        t = s.translate(table)
        assert_that(t,
                    is_("California Court of Appeal's said Bushman may ...be guilty of disturbing the peace through 'offensive'"))

        s = u'COPTIC OLD NUBIAN VERSE DIVIDER is \u2cFc deal with it'
        t = s.translate(table)
        assert_that(t, is_("COPTIC OLD NUBIAN VERSE DIVIDER is  deal with it"))

    def test_utilities(self):
        assert_that(component.queryUtility(IWordTokenizerPattern, name="en"),
                    is_not(none()))
        assert_that(component.queryUtility(IWordTokenizerExpression, name="en"),
                    is_not(none()))
        assert_that(component.queryUtility(IPunctuationMarkPattern, name="en"),
                    is_not(none()))
        assert_that(component.queryUtility(IPunctuationMarkExpression, name="en"),
                    is_not(none()))
        assert_that(component.queryUtility(IPunctuationMarkPatternPlus, name="en"),
                    is_not(none()))
        assert_that(component.queryUtility(IPunctuationMarkExpressionPlus, name="en"),
                    is_not(none()))

    def test_coverage(self):
        sim = _SequenceMatcherWordSimilarity()
        assert_that(sim.compute('alpha', 'bravo'), is_(0.2))

    @fudge.patch('nti.contentprocessing.content_utils.nltk_sent_tokenize')
    def test_sent_tokenize(self, mock_tock):
        data = "ichigo and rukia"
        mock_tock.is_callable().returns([data])
        assert_that(sent_tokenize(data), is_([data]))
