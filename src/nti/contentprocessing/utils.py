#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component

from zope.component.interfaces import ComponentLookupError

from nti.contentprocessing.interfaces import IWatsonAPIKey

logger = __import__('logging').getLogger(__name__)


def get_watson_api_key(name='', error=True):
    name = name or ''
    result = component.queryUtility(IWatsonAPIKey, name=name)
    if error and result is None:
        raise ComponentLookupError(IWatsonAPIKey, name)
    return result
getWatsonAPIKey = get_watson_api_key # BWC
