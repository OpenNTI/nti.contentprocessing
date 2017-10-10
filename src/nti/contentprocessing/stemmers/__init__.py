#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import repoze.lru

from zope import component

from nti.contentprocessing.stemmers.interfaces import IStemmer


@repoze.lru.lru_cache(200)
def stem_word(word, lang='en', name=''):
    stemmer = component.queryUtility(IStemmer, name=name)
    if stemmer is not None:
        return stemmer.stem(word, lang) if word else None
    return word
stem = stem_word
