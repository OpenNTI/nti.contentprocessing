#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest

from zope import component

from nti.contentprocessing.stemmers.interfaces import IStemmer

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestNLTKStemmer(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_utility(self):
        stemmer = component.getUtility(IStemmer, "porter")
        assert_that(stemmer.stem(u'viruses'), is_('virus'))
        assert_that(stemmer.stem(u'temptation'), is_('temptat'))
        assert_that(stemmer.stem(u'いちご', 'jp'), is_(u'いちご'))
