#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import functools

from zope import interface

from zope.schema.fieldproperty import FieldPropertyStoredThroughField as FP

from nti.common.representation import WithRepr

from nti.contentprocessing.langdetection.interfaces import ILanguage

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.schema.schema import SchemaConfigured

from nti.schema.fieldproperty import createDirectFieldProperties

@WithRepr
@EqHash('code',)
@functools.total_ordering
@interface.implementer(ILanguage)
class Language(SchemaConfigured):
	createDirectFieldProperties(ILanguage)

	def __lt__(self, other):
		try:
			return self.code < other.code
		except AttributeError:
			return NotImplemented

	def __gt__(self, other):
		try:
			return self.code > other.code
		except AttributeError:
			return NotImplemented
