#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Whoosh based stemmers

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

try:
	from whoosh.lang import has_stemmer
	from whoosh.lang import stemmer_for_language
except ImportError:
	has_stemmer = lambda x: False
	stemmer_for_language = lambda x: x

from zope import interface

from nti.contentprocessing._compat import to_unicode

from nti.contentprocessing.stemmers.interfaces import IStemmer

@interface.implementer(IStemmer)
class _WhooshStemmer(object):

	__slots__ = ()

	def __init__(self, *args, **kwargs):
		pass

	def stem(self, token, lang='en'):
		token = to_unicode(token)
		if has_stemmer(lang):
			stemmer = stemmer_for_language(lang)
			result = stemmer(token) if stemmer is not None else token
			return result if result else token
		return  token
