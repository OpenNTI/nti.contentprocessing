#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Alchemy keyword extractor

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

from nti.contentprocessing.keyword.interfaces import IKeyWordExtractor

from nti.contentprocessing.keyword.model import ContentKeyWord

from nti.contentprocessing.utils import get_alchemy_api_key

ALCHEMYAPI_LIMIT_KB = 150
ALCHEMYAPI_URL = u'http://access.alchemyapi.com/calls/text/TextGetRankedKeywords'

def get_keywords(content, name=None, **kwargs):
	apikey = get_alchemy_api_key(name=name)
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
		keywords = data.get('keywords', ())
		result = tuple(	ContentKeyWord(d['text'], float(d.get('relevance', 0)))
				  		for d in keywords)
	else:
		result = ()
		logger.error('Invalid request status while getting keywords from Alchemy; %s',
					 data.get('status', ''))

	return result

@interface.implementer(IKeyWordExtractor)
class _AlchemyAPIKeyWorExtractor(object):

	__slots__ = ()

	def __call__(self, content, keyname=None, *args, **kwargs):
		result = ()
		content = content or u''
		size_kb = sys.getsizeof(content) / 1024.0
		if size_kb > ALCHEMYAPI_LIMIT_KB:
			s = StringIO(content)
			content = s.read(ALCHEMYAPI_LIMIT_KB)
		try:
			if content: 
				result = get_keywords(content, keyname, **kwargs)
		except:
			logger.exception('Error while getting keywords from Alchemy')
		return result
