#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Alchemy concept tagging

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contentprocessing.alchemy import get_alchemy_client

from nti.contentprocessing.concepttagging.concept import Concept
from nti.contentprocessing.concepttagging.concept import ConceptSource

from nti.contentprocessing.concepttagging.interfaces import IConceptTagger

def get_ranked_concepts(content, name=None, **kwargs):
	alchemy_client = get_alchemy_client( name )
	result = ()
	if alchemy_client is not None:
		try:
			# XXX: Do we need to sniff (or convert to) for HTML or text?
			# max_items defaults to 8
			result = alchemy_client.concepts( text=content )
		except:
			result = ()
			logger.error('Invalid request status while getting concepts from Alchemy')
		else:
			for entry in result.get('concepts', ()):
				sources = []
				text = relevance = None
				for k, v in entry.items():
					if k not in ('text', 'relevance'):
						sources.append(ConceptSource(k, v))
					elif k == 'text':
						text = v
					elif v is not None:
						relevance = float(v)
				result.append(Concept(text, relevance, sources))
	return result

@interface.implementer(IConceptTagger)
class _AlchemyAPIKConceptTaggger(object):

	__slots__ = ()

	@staticmethod
	def tag(content, keyname=None, **kwargs):
		result = ()
		content = content or u''
		try:
			if content:
				result = get_ranked_concepts(content, name=keyname, **kwargs)
		except:
			logger.exception('Error while getting concept tags from Alchemy')
		return result

	def __call__(self, content, keyname=None, **kwargs):
		return self.tag(content, keyname, **kwargs)
