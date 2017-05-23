#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementations of API alchemy keys.

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from watson_developer_cloud.alchemy_language_v1 import AlchemyLanguageV1

from zope import interface

from nti.contentprocessing.interfaces import IAlchemyAPIKey

from nti.contentprocessing.utils import get_alchemy_api_key

from nti.contentprocessing.representation import WithRepr

from nti.property.property import alias as aka

from nti.schema.eqhash import EqHash


@WithRepr
@EqHash('name', 'value')
@interface.implementer(IAlchemyAPIKey)
class AlchemyAPIKey(object):

    key = aka('value')
    alias = aka('name')

    def __init__(self, name, value):
        self.name = name
        self.value = value


def create_api_key(name, value):
    result = AlchemyAPIKey(name=name, value=value)
    return result


def get_alchemy_client(keyname=None):
    """
    Returns an AlchemyAPI client for using the Alchemy service, or
    None if no key is configured.
    """
    alchemy_key = get_alchemy_api_key(keyname)
    result = None
    if alchemy_key:
        result = AlchemyLanguageV1(api_key=alchemy_key)
    return result
