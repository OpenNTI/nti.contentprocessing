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

from nti.common.representation import WithRepr

from nti.contentprocessing.concepttagging.interfaces import IConcept
from nti.contentprocessing.concepttagging.interfaces import IConceptSource

from nti.schema.eqhash import EqHash

@WithRepr
@EqHash('uri','source')
@interface.implementer(IConceptSource)
class ConceptSource(object):

	def __init__(self, source, uri=None):
		self.uri = uri
		self.source = source

@WithRepr
@EqHash('text',)
@functools.total_ordering
@interface.implementer(IConcept)
class Concept(object):

	def __init__(self, text=None, relevance=None, sources=()):
		self.text = text
		self.sources = sources
		self.relevance = relevance

	@property
	def sourcemap(self):
		return {c.source:c.uri for c in self.sources}

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
