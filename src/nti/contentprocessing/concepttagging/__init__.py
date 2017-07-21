#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from nti.contentprocessing.concepttagging.interfaces import IConceptTagger


def concept_tag(content, name=''):
    tagger = component.queryUtility(IConceptTagger, name=name)
    if tagger is not None:
        return tagger(content)
    return ()
