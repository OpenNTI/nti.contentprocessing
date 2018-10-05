#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NLTK based stemmers

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nltk import PorterStemmer

from zope import interface

from nti.contentprocessing.stemmers.interfaces import IStemmer

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IStemmer)
class _PorterStemmer(object):

    __slots__ = ()

    def stem(self, token, lang='en'):
        if lang == 'en':
            # The underlying stemmer object is NOT thread safe,
            # it must not be used concurrently
            stemmer = PorterStemmer()
            result = stemmer.stem(token)
            return result if result else token
        return token
