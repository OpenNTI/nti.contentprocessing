#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Alchemy keyword extractor

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contentprocessing.alchemy import get_alchemy_client

from nti.contentprocessing.keyword.interfaces import IKeyWordExtractor

from nti.contentprocessing.keyword.model import ContentKeyWord

def get_keywords(content, name=None, **kwargs):
	alchemy_client = get_alchemy_client( name )
	result = ()
	if alchemy_client is not None:
		try:
			# XXX: Do we need to sniff (or convert to) for HTML or text?
			# max_items defaults to 50
			result = alchemy_client.keywords( text=content )
		except:
			result = ()
			logger.error('Invalid request status while getting keywords from Alchemy')
		else:
			keywords = result.get('keywords', ())
			result = tuple(	ContentKeyWord(d['text'], float(d.get('relevance', 0)))
				  			for d in keywords)
	return result

@interface.implementer(IKeyWordExtractor)
class _AlchemyAPIKeyWordExtractor(object):

	__slots__ = ()

	def __call__(self, content, keyname=None, *args, **kwargs):
		result = ()
		if isinstance(content, (list, tuple)):
			content = ' '.join(content)
		try:
			if content:
				result = get_keywords(content, keyname, **kwargs)
		except:
			logger.exception('Error while getting keywords from Alchemy')
		return result
