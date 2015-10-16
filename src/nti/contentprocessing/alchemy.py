#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementations of API alchemy keys.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.common.property import alias as aka
from nti.common.representation import WithRepr

from nti.schema.schema import EqHash

from .interfaces import IAlchemyAPIKey

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
