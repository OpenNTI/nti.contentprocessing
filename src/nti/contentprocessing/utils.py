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

from .interfaces import IAlchemyAPIKey

def getAlchemyAPIKey(name=None, error=True):
	if name is not None:
		names = (name,)
	else:
		names = (name,) 
	for name in names:
		result = component.queryUtility(IAlchemyAPIKey, name=name)
		if result is not None:
			break
	if error and result is None:
		raise ComponentLookupError(IAlchemyAPIKey, name)
	return result
