#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NGRAM processing utilities

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import repoze.lru

from six import string_types

from zope import component
from zope import interface

from nti.contentprocessing import default_ngram_maxsize
from nti.contentprocessing import default_ngram_minsize

from nti.contentprocessing.content_utils import tokenize_content

from nti.contentprocessing.interfaces import INgramComputer

logger = __import__('logging').getLogger(__name__)


@repoze.lru.lru_cache(5000)
def _ngram_cache(text, minsize=3, maxsize=None, lower=True):
    result = []
    maxsize = maxsize or len(text)
    text = text.lower() if lower else text
    limit = min(maxsize, len(text))
    for size in range(minsize, limit + 1):
        ngram = text[:size]
        result.append(ngram)
    return result


def ngram_filter(text, minsize=3, maxsize=None, unique=True, lower=True):
    tokens = tokenize_content(text)
    result = set() if unique else list()
    for text in tokens:
        ngrams = _ngram_cache(text, minsize, maxsize, lower)
        if unique:
            result.update(ngrams)
        else:
            result.extend(ngrams)
    return result


@repoze.lru.lru_cache(100)
def compute_ngrams(text, lang="en"):
    computer = component.getUtility(INgramComputer, name=lang)
    return computer.compute(text)


@interface.implementer(INgramComputer)
class _DefaultNgramComputer(object):

    minsize = default_ngram_minsize
    maxsize = default_ngram_maxsize

    def compute(self, text):
        if text and isinstance(text, string_types):
            result = ngram_filter(text, self.minsize, self.maxsize)
            result = u' '.join(result)
        else:
            result = u''
        return result
