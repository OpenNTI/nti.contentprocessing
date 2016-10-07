#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Keyword extractor module

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from collections import namedtuple
from functools import total_ordering

from zope import component
from zope import interface

from nti.common.representation import WithRepr

from nti.contentprocessing.keyword.interfaces import IContentKeyWord
from nti.contentprocessing.keyword.interfaces import IKeyWordExtractor
from nti.contentprocessing.keyword.interfaces import ITermExtractKeyWordExtractor

from nti.schema.eqhash import EqHash

@WithRepr
@EqHash('token',)
@total_ordering
@interface.implementer(IContentKeyWord)
class ContentKeyWord(object):

	__slots__ = ('token', 'relevance')

	def __init__(self, token=None, relevance=None):
		self.token = token
		self.relevance = relevance

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

def term_extract_key_words(content, lang='en', filtername=u''):
	extractor = component.queryUtility(ITermExtractKeyWordExtractor, name=lang)
	if extractor is not None:
		return extractor(content, lang=lang, filtername=filtername)
	return ()

def extract_key_words(content):
	extractor = component.queryUtility(IKeyWordExtractor)
	if extractor is not None:
		return extractor(content)
	return ()
