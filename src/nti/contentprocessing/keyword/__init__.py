#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from nti.contentprocessing.keyword.interfaces import IKeyWordExtractor
from nti.contentprocessing.keyword.interfaces import ITermExtractKeyWordExtractor

def term_extract_key_words(content, lang='en', filtername=u''):
	extractor = component.queryUtility(ITermExtractKeyWordExtractor, name=lang)
	if extractor is not None:
		return extractor(content, lang=lang, filtername=filtername)
	return ()

def extract_key_words(content, lang='en'):
	extractor = component.queryUtility(IKeyWordExtractor, name='en')
	if extractor is not None:
		return extractor(content)
	return ()
