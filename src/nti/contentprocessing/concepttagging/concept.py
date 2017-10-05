#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from functools import total_ordering

from zope import interface

from nti.contentprocessing.concepttagging.interfaces import IConcept

from nti.contentprocessing.representation import WithRepr

from nti.schema.eqhash import EqHash

logger = __import__('logging').getLogger(__name__)


@WithRepr
@total_ordering
@EqHash('text',)
@interface.implementer(IConcept)
class Concept(object):

    __slots__ = ('text', 'relevance', 'resource')

    def __init__(self, text=None, relevance=None, resource=None):
        self.text = text
        self.resource = resource
        self.relevance = relevance

    def __str__(self):
        return self.text

    def __lt__(self, other):
        try:
            return self.relevance < other.relevance
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.relevance > other.relevance
        except AttributeError:  # pragma: no cover
            return NotImplemented
