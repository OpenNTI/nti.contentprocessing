#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from zope.component.interfaces import ComponentLookupError

from nti.contentprocessing.interfaces import IWatsonAPIKey


def get_watson_api_key(name='', error=True):
    name = name or ''
    result = component.queryUtility(IWatsonAPIKey, name=name)
    if error and result is None:
        raise ComponentLookupError(IWatsonAPIKey, name)
    return result
getWatsonAPIKey = get_watson_api_key # BWC
