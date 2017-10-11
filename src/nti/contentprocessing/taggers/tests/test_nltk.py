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
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import greater_than

import six
import fudge
import unittest

from zope import component

from nti.contentprocessing.taggers.nltk import ITaggedCorpus
from nti.contentprocessing.taggers.nltk import INLTKBackoffNgramTaggerFactory

from nti.contentprocessing.taggers.nltk import get_training_sents
from nti.contentprocessing.taggers.nltk import load_tagger_pickle
from nti.contentprocessing.taggers.nltk import default_nltk_tagger
from nti.contentprocessing.taggers.nltk import nltk_tagged_corpora
from nti.contentprocessing.taggers.nltk import get_nltk_tagged_corpus
from nti.contentprocessing.taggers.nltk import get_backoff_ngram_tagger

from nti.contentprocessing.taggers.tests import NLTKConfiguringTestLayer


class TestNLTK(unittest.TestCase):

    layer = NLTKConfiguringTestLayer

    @unittest.skipUnless(six.PY2, 'python2')
    def test_nltk_tagged_corpora(self):
        corpora = nltk_tagged_corpora()
        assert_that(corpora, has_length(greater_than(0)))
        for corpus in corpora.values():
            assert_that(ITaggedCorpus.providedBy(corpus),
                        is_(True))
        assert_that(get_nltk_tagged_corpus('brown'),
                    is_not(none()))

    @unittest.skipUnless(six.PY2, 'python2')
    def test_nltk_tagged_sents(self):
        sents = get_training_sents('brown', 5)
        assert_that(sents, has_length(5))

    @unittest.skipUnless(six.PY2, 'python2')
    def test_default_nltk_tagger(self):
        tagger = default_nltk_tagger()
        assert_that(tagger, is_not(none()))
        tagger = get_backoff_ngram_tagger()
        assert_that(tagger, is_not(none()))

    @unittest.skipUnless(six.PY2, 'python2')
    @fudge.patch('nti.contentprocessing.taggers.nltk.get_training_sents')
    def test_get_backoff_ngram_tagger(self, mock_ts):
        mock_ts.is_callable().returns(())
        tagger = get_backoff_ngram_tagger(ngrams=1, corpus='ichigo',
                                          model='bleach')
        assert_that(tagger, is_not(none()))

    def test_tagger_factory(self):
        factory = component.queryUtility(INLTKBackoffNgramTaggerFactory)
        assert_that(factory, is_not(none()))
        assert_that(factory(), is_not(none()))

    def test_load_tagger_pickle(self):
        with self.assertRaises(Exception):
            load_tagger_pickle(__file__)
