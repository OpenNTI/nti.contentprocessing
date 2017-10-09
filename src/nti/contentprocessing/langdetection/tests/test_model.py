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

from nti.contentprocessing.langdetection.interfaces import ILanguage

from nti.contentprocessing.langdetection.model import Language

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestModel(unittest.TestCase):

    layer = SharedConfiguringTestLayer
    
    def test_model(self):
        en = Language(code=u'en', name=u'english')
        assert_that(en, validly_provides(ILanguage))
        assert_that(en, verifiably_provides(ILanguage))
        
        es = Language(code=u'es', name=u'spanish')
        
        assert_that(sorted([es, en]),
                    is_([en, es]))
    
        assert_that(es.__gt__(en), is_(True))
        assert_that(en.__lt__(es), is_(True))
