#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component

from nti.contentprocessing.concepttagging.interfaces import IConceptTagger

logger = __import__('logging').getLogger(__name__)


def concept_tag(content, name=''):
    tagger = component.queryUtility(IConceptTagger, name=name)
    if tagger is not None:
        return tagger(content)
    return ()
