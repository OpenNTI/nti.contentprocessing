#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Watson concept tagging

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import watson_developer_cloud.natural_language_understanding.features.v1 as features

from zope import interface
    
from nti.contentprocessing.watson import get_natural_lang_understanding_client

from nti.contentprocessing.concepttagging.concept import Concept

from nti.contentprocessing.concepttagging.interfaces import IConceptTagger


def analyze(client, content, **kwargs):
    response = client.analyze(text=content,
                              features=[features.Concepts()],
                              **kwargs)
    return response


def get_ranked_concepts(content, name='', **kwargs):
    result = []
    watson_client = get_natural_lang_understanding_client(name)
    if watson_client is not None:
        try:
            response = analyze(watson_client, content, **kwargs)
        except Exception:
            logger.exception('Invalid request status while getting concepts')
        else:
            for entry in response.get('concepts', ()):
                concept = Concept(entry.get('text'),
                                  entry.get('relevance'))
                for k, v in entry.items():
                    if k not in ('text', 'relevance'):
                        concept.resource = v
                        break
                result.append(concept)
    return result


@interface.implementer(IConceptTagger)
class _WatsonAPIKConceptTaggger(object):

    __slots__ = ()

    @staticmethod
    def tag(content, keyname=None, **kwargs):
        result = ()
        content = content or u''
        try:
            if content:
                result = get_ranked_concepts(content, name=keyname, **kwargs)
        except Exception:
            logger.exception('Error while getting concept tags')
        return result

    def __call__(self, content, keyname=None, **kwargs):
        return self.tag(content, keyname, **kwargs)
