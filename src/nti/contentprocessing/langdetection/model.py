#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import functools

from zope import interface

from zope.cachedescriptors.property import readproperty

from nti.contentprocessing.langdetection.interfaces import ILanguage

from nti.contentprocessing.representation import WithRepr

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

logger = __import__('logging').getLogger(__name__)


@WithRepr
@EqHash('code',)
@functools.total_ordering
@interface.implementer(ILanguage)
class Language(SchemaConfigured):
    createDirectFieldProperties(ILanguage)

    @readproperty
    def name(self):
        # pylint: disable=no-member
        return self.code

    def __lt__(self, other):
        try:
            return self.code < other.code
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.code > other.code
        except AttributeError:  # pragma: no cover
            return NotImplemented
