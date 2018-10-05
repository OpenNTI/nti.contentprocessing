#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ZOPYX based stemmers

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from zopyx.txng3.ext import stemmer

from nti.contentprocessing.stemmers.interfaces import IStemmer

Stemmer = getattr(stemmer, 'Stemmer')

lang_translation = {'en': 'english', 'es': 'spansih', 'ru': 'russian',
                    'fr': 'french', 'de': 'german', 'da': 'danish',
                    'nl': 'dutch', 'it': 'italian', 'no': 'norwegian',
                    'pt': 'portuguese', 'sv': 'swedish', 'fi': 'finnish',
                    'tr': 'turkish', 'hu': 'hungarian', 'ro': 'romanian'}


logger = __import__('logging').getLogger(__name__)


@interface.implementer(IStemmer)
class _ZopyYXStemmer(object):

    def __init__(self):
        self.stemmers = {}

    def _stemmer(self, lang='en'):
        lang = lang.lower() if lang else 'en'
        result = self.stemmers.get(lang, None)
        if result is None:
            language = lang_translation[lang]
            result = self.stemmers[lang] = Stemmer(language)
        return result

    def stem(self, token, lang='en'):
        try:
            result = self._stemmer(lang).stem((token,))
            return result[0] if result else token
        except (AttributeError, KeyError):  # lang not available
            pass
        return token
