#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
POS tagger module

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import repoze.lru

from zope import component

from nti.contentprocessing.taggers.interfaces import ITagger
from nti.contentprocessing.taggers.interfaces import INLTKTagger
from nti.contentprocessing.taggers.interfaces import IStanfordTagger


@repoze.lru.lru_cache(500)
def tag_word(word, lang='en'):
    return tag_tokens((word,), lang)


def tag_tokens(tokens, lang='en'):
    for provided in (IStanfordTagger, INLTKTagger):
        tagger = component.queryUtility(provided, name=lang)
        result = tagger.tag(tokens) if tagger is not None and tokens else ()
        if result:
            return result
    return ()
