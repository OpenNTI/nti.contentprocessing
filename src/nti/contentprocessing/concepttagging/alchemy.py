#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Alchemy concept tagging

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import sys
import requests

from simplejson.compat import StringIO

from zope import interface

from nti.common.string import to_unicode

from nti.contentprocessing.concepttagging.concept import Concept
from nti.contentprocessing.concepttagging.concept import ConceptSource

from nti.contentprocessing.concepttagging.interfaces import IConceptTagger

from nti.contentprocessing.utils import getAlchemyAPIKey

ALCHEMYAPI_LIMIT_KB = 150
ALCHEMYAPI_URL = u'http://access.alchemyapi.com/calls/text/TextGetRankedConcepts'

def get_ranked_concepts(content, name=None, **kwargs):
	apikey = getAlchemyAPIKey(name=name)
	headers = {u'content-type': u'application/x-www-form-urlencoded'}
	params = {
		u'text':to_unicode(content),
		u'apikey':apikey.value,
		u'outputMode':u'json'
	}
	params.update(kwargs)

	r = requests.post(ALCHEMYAPI_URL, data=params, headers=headers)
	data = r.json()

	if r.status_code == 200 and data.get('status', 'ERROR') == 'OK':
		result = []
		for entry in data.get('concepts', ()):
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
	else:
		result = ()
		logger.error('Invalid request status while getting ranked concepts; %s',
					 data.get('status', ''))

	return result

@interface.implementer(IConceptTagger)
class _AlchemyAPIKConceptTaggger(object):

	__slots__ = ()

	@staticmethod
	def tag(content, keyname=None, **kwargs):
		result = ()
		content = content or u''
		size_kb = sys.getsizeof(content) / 1024.0
		if size_kb > ALCHEMYAPI_LIMIT_KB:
			s = StringIO(content)
			content = s.read(ALCHEMYAPI_LIMIT_KB)
		try:
			if content:
				result = get_ranked_concepts(content, name=keyname, **kwargs)
		except:
			logger.exception('Error while getting concept tags from Alchemy')
		return result

	def __call__(self, content, keyname=None, **kwargs):
		return self.tag(content, keyname, **kwargs)
