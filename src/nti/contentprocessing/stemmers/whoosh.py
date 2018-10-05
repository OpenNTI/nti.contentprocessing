#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Whoosh based stemmers

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from whoosh.lang import has_stemmer
from whoosh.lang import stemmer_for_language

from zope import interface

from nti.contentprocessing.stemmers.interfaces import IStemmer

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IStemmer)
class _WhooshStemmer(object):

    __slots__ = ()

    def stem(self, token, lang='en'):
        if has_stemmer(lang):
            stemmer = stemmer_for_language(lang)
            result = stemmer(token) if stemmer is not None else token
            return result if result else token
        return token
