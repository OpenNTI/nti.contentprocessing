#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import unittest

from nti.contentprocessing.concepttagging.concept import Concept

from nti.contentprocessing.concepttagging.interfaces import IConcept

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestConcept(unittest.TestCase):

    layer = SharedConfiguringTestLayer
    
    def test_model(self):
        ichigo = Concept(u'ichigo', 100, u'http://bleach.org')
        assert_that(ichigo, validly_provides(IConcept))
        assert_that(ichigo, verifiably_provides(IConcept))
        assert_that(str(ichigo), is_('ichigo'))
        
        aizen = Concept(u'aizen', 99, u'http://bleach.org')
        
        assert_that(sorted([ichigo, aizen]),
                    is_([aizen, ichigo]))
    
        assert_that(ichigo.__gt__(aizen), is_(True))
        assert_that(aizen.__lt__(ichigo), is_(True))
