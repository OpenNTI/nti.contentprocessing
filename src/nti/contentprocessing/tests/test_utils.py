#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from zope.component import ComponentLookupError

from nti.contentprocessing.utils import get_watson_api_key

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestUtils(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_get_watson_api_key(self):

        with self.assertRaises(ComponentLookupError):
            get_watson_api_key('unknown')
