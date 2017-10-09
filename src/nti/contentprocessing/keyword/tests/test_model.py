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

from nti.contentprocessing.keyword.interfaces import IContentKeyWord

from nti.contentprocessing.keyword.model import ContentKeyWord

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestModel(unittest.TestCase):

    layer = SharedConfiguringTestLayer
    
    def test_model(self):
        ichigo = ContentKeyWord(u'ichigo', 100)
        assert_that(ichigo, validly_provides(IContentKeyWord))
        assert_that(ichigo, verifiably_provides(IContentKeyWord))
        
        aizen = ContentKeyWord(u'aizen', 99)
        
        assert_that(sorted([ichigo, aizen]),
                    is_([aizen, ichigo]))
    
        assert_that(ichigo.__gt__(aizen), is_(True))
        assert_that(aizen.__lt__(ichigo), is_(True))
