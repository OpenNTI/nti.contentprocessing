#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Watson keyword extractor

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import watson_developer_cloud.natural_language_understanding.features.v1 as features

from zope import interface

from nti.contentprocessing.keyword.interfaces import IKeyWordExtractor

from nti.contentprocessing.keyword.model import ContentKeyWord

from nti.contentprocessing.watson import get_natural_lang_understanding_client

logger = __import__('logging').getLogger(__name__)


def analyze(client, content, **kwargs):
    response = client.analyze(text=content,
                              features=[features.Keywords()],
                              **kwargs)
    return response


def get_keywords(content, name='', **kwargs):
    result = ()
    watson_client = get_natural_lang_understanding_client(name)
    if watson_client is not None:
        try:
            response = analyze(watson_client, content, **kwargs)
        except Exception:
            result = ()
            logger.exception('Invalid request status while getting keywords')
        else:
            keywords = response.get('keywords', ())
            result = tuple(ContentKeyWord(d['text'], float(d.get('relevance', 0)))
                           for d in keywords)
    return result


@interface.implementer(IKeyWordExtractor)
class _WatsonAPIKeyWordExtractor(object):

    __slots__ = ()

    def __call__(self, content, keyname=None, **kwargs):
        result = ()
        if isinstance(content, (list, tuple, set)):
            content = u' '.join(content)
        if content:
            result = get_keywords(content, keyname, **kwargs)
        return result
