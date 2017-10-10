#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import starts_with
from hamcrest import has_property

import os
import codecs
import unittest

from nti.contentprocessing.langdetection.tika.profile import LanguageProfile

from nti.contentprocessing.langdetection.tika.identifier import addProfile
from nti.contentprocessing.langdetection.tika.identifier import initProfiles
from nti.contentprocessing.langdetection.tika.identifier import clearProfiles
from nti.contentprocessing.langdetection.tika.identifier import LanguageIdentifier

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestIndentifier(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    languages = ("de", "en", "es")

    def test_initProfiles(self):
        c = initProfiles()
        assert_that(c, is_(27))

    def test_clearAddAndInitProfiles(self):
        LanguageIdentifier.initProfiles()
        enProfile = LanguageProfile()
        self.writeTo("en", enProfile)

        iden = LanguageIdentifier(enProfile)
        assert_that(iden, has_property('language', "en"))
        assert_that(iden.isReasonablyCertain(), is_(True))

        clearProfiles()
        iden = LanguageIdentifier(enProfile)
        assert_that(iden.isReasonablyCertain(), is_(False))

        addProfile("en", enProfile)
        iden = LanguageIdentifier(enProfile)
        assert_that(iden, has_property('language', "en"))
        assert_that(iden.isReasonablyCertain(), is_(True))

        source = os.path.join(os.path.dirname(__file__), 'en.ngp')
        iden = LanguageIdentifier(source)
        assert_that(iden, has_property('language', "en"))
        assert_that(str(iden), starts_with('en('))
        
        clearProfiles()
        profile = LanguageIdentifier.addProfile('en')
        assert_that(profile, is_(LanguageProfile))

        assert_that(LanguageIdentifier.getSupportedLanguages(),
                    is_({'en'}))

    def writeTo(self, language, writer):
        source = os.path.join(os.path.dirname(__file__), '%s.test' % language)
        with codecs.open(source, "r", "utf-8") as fp:
            writer.write(fp.read())

    def test_languageDetection(self):
        initProfiles()
        for language in self.languages:
            pro = LanguageProfile()
            self.writeTo(language, pro)
            iden = LanguageIdentifier(pro)
            assert_that(iden, has_property('language', language))
            assert_that(iden.isReasonablyCertain(), is_(True))
