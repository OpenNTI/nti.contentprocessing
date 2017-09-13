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

from nti.contentprocessing.concepttagging.interfaces import IConcept

from nti.contentprocessing.representation import WithRepr

from nti.schema.eqhash import EqHash


@WithRepr
@EqHash('text',)
@functools.total_ordering
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
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.relevance > other.relevance
        except AttributeError:
            return NotImplemented
