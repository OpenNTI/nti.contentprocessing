#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementations of API watson keys.

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from watson_developer_cloud import NaturalLanguageUnderstandingV1

from zope import interface

from nti.contentprocessing.interfaces import IWatsonAPIKey

from nti.contentprocessing.utils import get_watson_api_key

from nti.contentprocessing.representation import WithRepr

from nti.schema.eqhash import EqHash


@WithRepr
@EqHash('username', 'password')
@interface.implementer(IWatsonAPIKey)
class WatsonAPIKey(object):

    __slots__ = ('username', 'password')

    def __init__(self, username, password):
        self.username = username
        self.password = password


def create_api_key(username, password):
    result = WatsonAPIKey(username, password)
    return result


def get_natural_lang_understanding_client(name=''):
    """
    Returns an WatsonAPI client for using the Natural Language Understanding 
    service or None if no key is configured.
    """
    result = None
    watson_key = get_watson_api_key(name)
    if watson_key:
        result = NaturalLanguageUnderstandingV1(
                        username=watson_key.username,
                        password=watson_key.password,
                        version=NaturalLanguageUnderstandingV1.latest_version)
    return result
