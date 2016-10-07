#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from zope.component.interfaces import ComponentLookupError

from nti.contentprocessing.interfaces import IAlchemyAPIKey

def get_alchemy_api_key(name=None, error=True):
	name = '' if not name else name
	result = component.queryUtility(IAlchemyAPIKey, name=name)
	if error and result is None:
		raise ComponentLookupError(IAlchemyAPIKey, name)
	return result
getAlchemyAPIKey = get_alchemy_api_key

