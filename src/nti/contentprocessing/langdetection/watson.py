#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Watson lang detector

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contentprocessing._compat import text_

from nti.contentprocessing.langdetection.model import Language

from nti.contentprocessing.langdetection.interfaces import IWatsonLanguage
from nti.contentprocessing.langdetection.interfaces import ILanguageDetector

from nti.contentprocessing.representation import WithRepr

from nti.contentprocessing.watson import get_language_translator_client

from nti.property.property import alias

from nti.schema.fieldproperty import createDirectFieldProperties


@WithRepr
@interface.implementer(IWatsonLanguage)
class WatsonLanguage(Language):
    createDirectFieldProperties(IWatsonLanguage)

    ISO_639_1 = alias('code')

    def __lt__(self, other):
        try:
            return (self.confidence, self.code) < (other.confidence, other.code)
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.confidence, self.code) > (other.confidence, other.code)
        except AttributeError:
            return NotImplemented


@interface.implementer(ILanguageDetector)
class _WatsonTextLanguageDetector(object):

    __slots__ = ()

    @staticmethod
    def detect(content, name='', min_confidence=0.9):
        result = None
        content = content or u''
        languages = get_languages(content, name) if content else ()
        for lang in languages or ():
            if lang.confidence >= min_confidence:
                result = lang
                break
        return result

    def __call__(self, content, keyname=None, **kwargs):
        return self.detect(content, keyname=keyname, **kwargs)


def identify(client, content):
    return client.identify(content)


def get_languages(content, name=''):
    result = []
    watson_client = get_language_translator_client(name)
    if watson_client is not None:
        try:
            response = identify(watson_client, content)
        except Exception:
            logger.exception('Invalid request status while detecting language')
        else:
            for lang in response.get('languages', ()):
                lang = WatsonLanguage(code=text_(lang['language']), 
                                      confidence=float(lang.get('confidence', 0)))
                result.append(lang)
            result.sort(reverse=True)
    return result
