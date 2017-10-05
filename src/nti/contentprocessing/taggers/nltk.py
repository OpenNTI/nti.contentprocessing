#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NLTK based POS taggers

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import gzip
import inspect

from six.moves import cPickle

from zope import component
from zope import interface

from nltk.tag import NgramTagger
from nltk.tag import DefaultTagger

from nti.contentprocessing.taggers.interfaces import INLTKTagger

resource_exists = __import__('pkg_resources').resource_exists
resource_stream = __import__('pkg_resources').resource_stream

logger = __import__('logging').getLogger(__name__)


# Interfaces


class INLTKTaggedSents(interface.Interface):

    def __call__(corpus):
        """
        return tagged sents for the specified corpus
        """


class ITaggedCorpus(interface.Interface):
    """
    Define a POS tagged corpus.
    """

    def tagged_words():
        """
        return a list of POS tagged words
        """

    def tagged_sents():
        """
        return a list of POS tagged sentences
        """


class INLTKBackoffNgramTagger(INLTKTagger):
    pass


class INLTKBackoffNgramTaggerFactory(interface.Interface):

    def __call__(ngrams, corpus, train_sents, limit):
        """
        Create and train a backoff ngram tagger

        :param ngrams Number of ngrams
        :param corpus Optional corpus name
        :param train_sents: Training tagged sents
        :param limit Max munber of training sents
        """
# Implementation


def nltk_tagged_corpora():
    result = {}
    try:
        from nltk import corpus
        from nltk.corpus import LazyCorpusLoader, CorpusReader
        for k, v in inspect.getmembers(corpus):
            if      isinstance(v, (LazyCorpusLoader, CorpusReader)) \
                and hasattr(v, "tagged_sents") \
                and hasattr(v, "tagged_words"):
                result[k] = v
                interface.alsoProvides(v, ITaggedCorpus)
    except ImportError:
        logger.error("Error importing nltk corpora")
    return result


def get_nltk_tagged_corpus(corpus="brown"):
    return nltk_tagged_corpora().get(corpus)


@interface.implementer(INLTKTaggedSents)
class _NLTKTaggedSents(object):

    def __init__(self):
        self.tagged_sents = {}

    def __call__(self, corpus="brown", limit=-1):
        sents = self.tagged_sents.get(corpus, None)
        if sents is None:
            corpus = get_nltk_tagged_corpus(corpus)
            sents = corpus.tagged_sents() if corpus is not None else ()
            self.tagged_sents[corpus] = []
        return sents[:limit] if limit >= 0 else sents


def get_training_sents(corpus="brown", limit=-1):
    util = component.queryUtility(INLTKTaggedSents)
    util = util or _NLTKTaggedSents()
    return util(corpus, limit)


@interface.implementer(INLTKTagger)
def load_tagger_pickle(name_or_stream):
    result = None
    stream = None
    if hasattr(name_or_stream, 'read'):
        stream = gzip.GzipFile(fileobj=name_or_stream)
    elif os.path.exists(name_or_stream):
        stream = gzip.open(name_or_stream, 'rb')

    if stream is not None:
        with stream as f:
            result = cPickle.load(f)
    return result

_trained_taggers = {}


def get_backoff_ngram_tagger(ngrams=3, corpus="brown", limit=-1, train_sents=None):
    tagger = None
    if not train_sents:
        # check for a trained tagger
        pickles = 'nti.contentprocessing.taggers.pickles'
        name = "ngrams.%s.%s.%s.pickle.gz" % (ngrams, corpus, limit)
        if name in _trained_taggers:
            tagger = _trained_taggers[name]
        elif resource_exists(pickles, name):
            stream = resource_stream(pickles, name)
            tagger = load_tagger_pickle(stream)
            _trained_taggers[name] = tagger

    if tagger is None:
        if not train_sents:
            train_sents = get_training_sents(corpus, limit)

        tagger = DefaultTagger('NN')
        for n in range(1, ngrams + 1):
            tagger = NgramTagger(n, train=train_sents, backoff=tagger)

    interface.alsoProvides(tagger, INLTKBackoffNgramTagger)
    return tagger


@interface.implementer(INLTKBackoffNgramTaggerFactory)
class _NLTKBackoffNgramTaggerFactory(object):

    def __call__(self, ngrams=3, corpus="brown", limit=-1, train_sents=None):
        return get_backoff_ngram_tagger(ngrams, corpus, limit, train_sents)

_the_default_nltk_tagger = None


@interface.implementer(INLTKTagger)
def default_nltk_tagger():
    global _the_default_nltk_tagger
    if _the_default_nltk_tagger is None:
        _the_default_nltk_tagger = get_backoff_ngram_tagger()
    return _the_default_nltk_tagger
