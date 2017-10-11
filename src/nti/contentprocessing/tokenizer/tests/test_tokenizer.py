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

from nti.contentprocessing import default_word_tokenizer_expression

from nti.contentprocessing.tokenizer.tokenizer import SpaceTokenizer
from nti.contentprocessing.tokenizer.tokenizer import DefaultRegexpTokenizer

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestTokenizer(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_default_tokenizer(self):
        tokenizer = DefaultRegexpTokenizer(default_word_tokenizer_expression)
        assert_that(tokenizer.tokenize_sents(['alpha', 'beta']),
                    is_([['alpha'], ['beta']]))
        assert_that(list(tokenizer.span_tokenize_sents(['alpha', 'beta'])),
                    is_([[(0, 5)], [(0, 4)]]))

        tokenizer = DefaultRegexpTokenizer(default_word_tokenizer_expression,
                                           gaps=True)
        assert_that(tokenizer.tokenize('is virus a form of life?'),
                    is_([' ', ' ', ' ', ' ', ' ', '?']))

        assert_that(list(tokenizer.span_tokenize('is virus a form of life?')),
                    is_([(2, 3), (8, 9), (10, 11), (15, 16), (18, 19), (23, 24)]))

        tokenizer = DefaultRegexpTokenizer(default_word_tokenizer_expression,
                                           gaps=True, discard_empty=False)
        assert_that(tokenizer.tokenize('is virus a form of life?'),
                    is_(['', ' ', ' ', ' ', ' ', ' ', '?']))

        tokenizer = DefaultRegexpTokenizer(default_word_tokenizer_expression)
        assert_that(tokenizer.tokenize('is virus a form of life?'),
                    is_(['is', 'virus', 'a', 'form', 'of', 'life']))

        assert_that(list(tokenizer.span_tokenize('is virus a form of life?')),
                    is_([(0, 2), (3, 8), (9, 10), (11, 15), (16, 18), (19, 23)]))

        str(tokenizer)

    def test_string_tokenizer(self):
        tokenizer = SpaceTokenizer()
        assert_that(tokenizer.tokenize('alpha beta'),
                    is_(['alpha', 'beta']))
        assert_that(list(tokenizer.span_tokenize_sents(['alpha', 'beta'])),
                    is_([[(0, 5)], [(0, 4)]]))
