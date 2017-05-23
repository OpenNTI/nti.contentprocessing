#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NLTK based stemmers

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

try:
    from nltk import PorterStemmer
except ImportError:
    PorterStemmer = None

from zope import interface

from nti.contentprocessing._compat import text_

from nti.contentprocessing.stemmers.interfaces import IStemmer


@interface.implementer(IStemmer)
class _PorterStemmer(object):

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    def stem(self, token, lang='en'):
        token = text_(token)
        if lang == 'en' and PorterStemmer is not None:
            # The underlying stemmer object is NOT thread safe,
            # it must not be used concurrently
            stemmer = PorterStemmer()
            result = stemmer.stem(token)
            return result if result else token
        return token
