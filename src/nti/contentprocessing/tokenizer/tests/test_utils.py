#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import greater_than_or_equal_to

import unittest

from nti.contentprocessing.tokenizer.utils import mro
from nti.contentprocessing.tokenizer.utils import overridden
from nti.contentprocessing.tokenizer.utils import string_span_tokenize

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestUtils(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_overriden(self):
        class A(object):
            def eat(self, food):
                if overridden(self.batch_eat):
                    return food
                else:
                    raise NotImplementedError()

            def batch_eat(self, foods):
                return [self.eat(food) for food in foods]

        with self.assertRaises(NotImplementedError):
            A().batch_eat(('a', 'b'))

        class B(A):
            def batch_eat(self, foods):
                return [self.eat(food) for food in foods]

        B().batch_eat(('a', 'b'))

    def test_mro(self):
        class A(object):
            pass
        assert_that(mro(A), has_length(2))
        
        # old style classes
        class B():
            pass

        class C(B):
            pass
        assert_that(mro(C),
                    has_length(greater_than_or_equal_to(2)))

    def test_string_span_tokenize(self):
        with self.assertRaises(ValueError):
            list(string_span_tokenize('Good muffins', ''))
            
        assert_that(list(string_span_tokenize('Good muffins', ' ')),
                    is_([(0, 4), (5, 12)]))
