#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component

from nti.contentprocessing.keyword.interfaces import IKeyWordExtractor
from nti.contentprocessing.keyword.interfaces import ITermExtractKeyWordExtractor


def term_extract_key_words(content, lang='en', filtername=''):
    extractor = component.queryUtility(ITermExtractKeyWordExtractor, name=lang)
    if extractor is not None:
        return extractor(content, lang=lang, filtername=filtername)
    return ()


def extract_key_words(content, lang='en'):
    extractor = component.queryUtility(IKeyWordExtractor, name=lang)
    if extractor is not None:
        return extractor(content)
    return ()
