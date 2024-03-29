#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import six
import codecs
from six.moves import configparser

from nti.contentprocessing._compat import text_

from nti.contentprocessing.langdetection.tika.profile import LanguageProfile

DEFAULTSECT = 'DEFAULT'

logger = __import__('logging').getLogger(__name__)


def initProfiles():
    return LanguageIdentifier.initProfiles()


def clearProfiles():
    return LanguageIdentifier.clearProfiles()


def addProfile(language, profile):
    LanguageIdentifier.PROFILES[language] = profile


class LanguageIdentifier(object):

    PROFILES = {}

    CERTAINTY_LIMIT = 0.022

    distance = 1.0
    language = "unknown"

    def __init__(self, source):
        if isinstance(source, six.string_types):
            source = LanguageProfile(source)
        profile = source
        minDistance = 1.0
        minLanguage = "unknown"
        for key, value in self.PROFILES.items():
            distance = profile.distance(value)
            if distance < minDistance:
                minDistance = distance
                minLanguage = key
        self.language = minLanguage
        self.distance = minDistance

    def isReasonablyCertain(self):
        return self.distance < self.CERTAINTY_LIMIT

    def __str__(self):
        return "%s(%s)" % (self.language, self.distance)
    __repr__ = __str__

    @classmethod
    def addProfile(cls, language):
        profile = LanguageProfile()
        source = os.path.join(os.path.dirname(__file__),
                              'languages/%s.ngp' % language)
        with codecs.open(source, "r", "utf-8") as fp:
            for line in fp.readlines():
                line = text_(line) if line else None
                if line and line[0] != '#':
                    splits = line.split()
                    profile.add(splits[0].strip(), int(splits[1].strip()))

        cls.PROFILES[language] = profile
        return profile

    @classmethod
    def clearProfiles(cls):
        cls.PROFILES.clear()

    @classmethod
    def getSupportedLanguages(cls):
        return set(cls.PROFILES.keys())

    @classmethod
    def initProfiles(cls):
        cls.clearProfiles()
        source = os.path.join(os.path.dirname(__file__),
                              'languages/tika.language.properties')
        config = configparser.ConfigParser()
        config.readfp(open(source))

        languages = config.get(DEFAULTSECT, 'languages')
        languages = languages.split(",")
        for language in languages:
            language = text_(language.strip())
            name = config.get(DEFAULTSECT, "name." + language) or "Unknown"
            try:
                cls.addProfile(language)
            except Exception as e:  # pragma: no cover
                logger.error("language %s (%s) not not initialized; %s",
                             language, name, e)
        return len(cls.PROFILES)
