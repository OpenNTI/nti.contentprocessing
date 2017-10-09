#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from nti.contentprocessing._compat import text_

from nti.contentprocessing.langdetection.model import Language

from nti.contentprocessing.langdetection.interfaces import ILanguageDetector

from nti.contentprocessing.langdetection.tika.identifier import initProfiles
from nti.contentprocessing.langdetection.tika.identifier import LanguageIdentifier

from nti.contentprocessing.langdetection.tika.profile import LanguageProfile

_profiles_loaded = False

logger = __import__('logging').getLogger(__name__)


def loadProfiles():
    global _profiles_loaded
    if not _profiles_loaded:
        initProfiles()
        _profiles_loaded = True


@interface.implementer(ILanguageDetector)
class _TikaLanguageDetector(object):

    __slots__ = ()

    @staticmethod
    def detect(content, **unused_kwargs):
        loadProfiles()
        profile = LanguageProfile(content)
        iden = LanguageIdentifier(profile)
        return Language(code=text_(iden.language))

    def __call__(self, content, **kwargs):
        return self.detect(content, **kwargs)
