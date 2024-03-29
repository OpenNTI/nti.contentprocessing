#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import functools

from zope import component

from nti.contentprocessing.langdetection.interfaces import ILanguageDetector

DETECTORS = ('watson', 'xerox', 'tika')

logger = __import__('logging').getLogger(__name__)


def detect_Language(content, name=None):
    names = (name,) if name else DETECTORS
    for name in names:
        detector = component.queryUtility(ILanguageDetector, name=name)
        if detector is not None:
            return detector(content)
    return None
