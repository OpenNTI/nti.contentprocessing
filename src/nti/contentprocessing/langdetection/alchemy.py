#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Alchemy lang detector

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contentprocessing.alchemy import get_alchemy_client

from nti.contentprocessing.langdetection.model import Language

from nti.contentprocessing.langdetection.interfaces import IAlchemyLanguage
from nti.contentprocessing.langdetection.interfaces import ILanguageDetector

from nti.contentprocessing.representation import WithRepr

from nti.property.property import alias

from nti.schema.fieldproperty import createDirectFieldProperties


@WithRepr
@interface.implementer(IAlchemyLanguage)
class _AlchemyLanguage(Language):
    createDirectFieldProperties(IAlchemyLanguage)

    code = alias('ISO_639_1')

    def __str__(self):
        return self.code


@interface.implementer(ILanguageDetector)
class _AlchemyTextLanguageDetector(object):

    __slots__ = ()

    @staticmethod
    def detect(content, keyname=None, **kwargs):
        result = None
        content = content or u''
        try:
            if content:
                result = get_language(content, name=keyname, **kwargs)
        except:
            logger.exception('Error while detecting language using Alchemy')
        return result

    def __call__(self, content, keyname=None, **kwargs):
        return self.detect(content, keyname=keyname, **kwargs)


def get_language(content, name=None, **kwargs):
    result = None
    alchemy_client = get_alchemy_client(name)
    if alchemy_client is not None:
        try:
            # XXX: Do we need to sniff (or convert to) for HTML or text?
            data = alchemy_client.language(text=content)
        except Exception:
            result = None
            logger.error(
                'Invalid request status while detecting language from Alchemy')
        else:
            result = _AlchemyLanguage(ISO_639_1=data.get('iso-639-1'),
                                      ISO_639_2=data.get('iso-639-2', None),
                                      ISO_639_3=data.get('iso-639-3', None),
                                      name=data.get('language', None))
    return result
