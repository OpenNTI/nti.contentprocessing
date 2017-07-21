#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import functools

from zope import interface

from nti.contentprocessing.langdetection.interfaces import ILanguage

from nti.contentprocessing.representation import WithRepr

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured


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
