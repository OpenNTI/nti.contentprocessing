#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenXerox lang detector

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import requests

from zope import interface

from nti.common.string import to_unicode

from nti.contentprocessing.langdetection.model import Language

from nti.contentprocessing.langdetection.interfaces import ILanguageDetector

OPEN_XEROX_URL = u'https://services.open.xerox.com/RestOp/LanguageIdentifier/GetLanguageForString'

@interface.implementer(ILanguageDetector)
class _OpenXeroxLanguageDetector(object):
	
	__slots__ = ()
	
	@staticmethod
	def detect(content):
		result = None
		headers = {
			u'content-type': u'application/x-www-form-urlencoded', 
			u"Accept": "text/plain"
		}
		params = {u'document':to_unicode(content)}
		try:
			r = requests.post(OPEN_XEROX_URL, data=params, headers=headers)
			data = r.json()
			if r.status_code == 200 and data:
				result = Language(code=data)
			else:
				logger.error("%s is an invalid status response code; %s",
							 r.status_code, data)
		except Exception:
			result = None
			logger.exception('Error while detecting language using OpenXerox')

		return result
	
	def __call__(self, content, **kwargs):
		return self.detect(content)
