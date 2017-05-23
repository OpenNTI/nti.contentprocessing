#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest

from zope import component

from nti.contentprocessing.stemmers import interfaces

from nti.contentprocessing.stemmers.zopyx import stemmer

from nti.contentprocessing.tests import SharedConfiguringTestLayer


@unittest.skipIf(stemmer is None, "zopyx not installed")
class TestZopyYXStemmer(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_utility(self):
        stemmer = component.getUtility(interfaces.IStemmer, "zopyx")
        assert_that(stemmer.stem(u'viruses'), is_('virus'))
        assert_that(stemmer.stem(u'temptation'), is_('temptat'))