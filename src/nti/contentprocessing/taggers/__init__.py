#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import repoze.lru

from zope import component

from nti.contentprocessing.taggers.interfaces import INLTKTagger

logger = __import__('logging').getLogger(__name__)


@repoze.lru.lru_cache(500)
def tag_word(word, lang='en'):
    return tag_tokens((word,), lang)


def tag_tokens(tokens, lang='en'):
    tagger = component.queryUtility(INLTKTagger, name=lang)
    result = tagger.tag(tokens) if tagger is not None and tokens else ()
    return result or ()
