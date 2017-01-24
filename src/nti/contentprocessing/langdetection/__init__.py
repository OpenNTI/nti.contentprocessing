#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import functools

from zope import component

from nti.contentprocessing.langdetection.interfaces import ILanguageDetector

DETECTORS = ('alchemy', 'xerox', 'tika')


def detect_Language(content, name=None):
    names = (name,) if name else DETECTORS
    for name in names:
        detector = component.queryUtility(ILanguageDetector, name=name)
        if detector is not None:
            return detector(content)
    return None
