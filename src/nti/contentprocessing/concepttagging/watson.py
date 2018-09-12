#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import watson_developer_cloud.natural_language_understanding.features.v1 as features

from zope import interface

from nti.contentprocessing.concepttagging.concept import Concept

from nti.contentprocessing.concepttagging.interfaces import IConceptTagger

from nti.contentprocessing.watson import get_natural_lang_understanding_client

logger = __import__('logging').getLogger(__name__)


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
        except Exception: # pylint: disable=broad-except
            logger.exception('Invalid request status while getting concepts')
        else:
            response = response.get_result()
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
        result = get_ranked_concepts(content or '', name=keyname, **kwargs)
        return result

    def __call__(self, content, keyname=None, **kwargs):
        return self.tag(content, keyname, **kwargs)
