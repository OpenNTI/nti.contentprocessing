#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Content processing utilities

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import re
import difflib
import unicodedata
from six import string_types

resource_filename = __import__('pkg_resources').resource_filename

from zope import component
from zope import interface

try:
    from zopyx.txng3.ext.levenshtein import ratio as relative
except ImportError:  # pragma: no cover
    try:
        from whoosh.support.levenshtein import relative
    except ImportError:  # pragma: no cover
        def relative(*unused_args):
            return 0

from nti.contentfragments.interfaces import IPlainTextContentFragment

from nti.contentprocessing import space_pattern
from nti.contentprocessing import non_alpha_pattern
from nti.contentprocessing import special_regexp_chars
from nti.contentprocessing import default_word_tokenizer_pattern
from nti.contentprocessing import default_word_tokenizer_expression

from nti.contentprocessing._compat import text_

from nti.contentprocessing.interfaces import IWordSimilarity
from nti.contentprocessing.interfaces import IContentTokenizer
from nti.contentprocessing.interfaces import IWordTokenizerPattern
from nti.contentprocessing.interfaces import IContentTranslationTable
from nti.contentprocessing.interfaces import IWordTokenizerExpression

from nti.contentprocessing.tokenizer import DefaultRegexpTokenizer

logger = __import__('logging').getLogger(__name__)


def get_content_translation_table(lang='en'):
    table = component.queryUtility(IContentTranslationTable, name=lang)
    return table or _default_content_translation_table()


@interface.implementer(IWordTokenizerExpression)
def _default_word_tokenizer_expression():
    return default_word_tokenizer_expression


@interface.implementer(IWordTokenizerPattern)
def _default_word_tokenizer_pattern():
    return default_word_tokenizer_pattern


def tokenize_content(text, lang='en'):
    tokenizer = component.queryUtility(IContentTokenizer, name=lang)
    result = tokenizer.tokenize(text) if tokenizer is not None else ()
    return result
split_content = tokenize_content


def get_content(text=None, lang="en"):
    if not text or not isinstance(text, string_types):
        result = u''
    else:
        result = tokenize_content(text, lang)
        result = u' '.join(result)
    return result


def normalize(u, form='NFC'):
    """
    Convert to normalized unicode.
    Remove non-alpha chars and compress runs of spaces.
    """
    u = unicodedata.normalize(form, u)
    u = non_alpha_pattern.sub(u' ', u)
    u = space_pattern.sub(u' ', u)
    return u


@interface.implementer(IContentTokenizer)
class _ContentTokenizer(object):

    __slots__ = ()

    tokenizer = DefaultRegexpTokenizer(_default_word_tokenizer_expression(),
                                       flags=re.MULTILINE | re.DOTALL | re.UNICODE)

    @classmethod
    def tokenize(cls, content):
        if not content or not isinstance(content, string_types):
            result = ()
        else:
            plain_text = cls.to_plain_text(content)
            result = cls.tokenizer.tokenize(plain_text)
        return result

    @classmethod
    def to_plain_text(cls, content):
        return component.getAdapter(content,
                                    IPlainTextContentFragment,
                                    name='text')


@interface.implementer(IWordSimilarity)
class _BaseWordSimilarity(object):

    def rank(self, word, terms, reverse=True):
        return sorted(terms, key=lambda w: self.compute(word, w), reverse=reverse)


class _SequenceMatcherWordSimilarity(_BaseWordSimilarity):

    def compute(self, a, b):
        return difflib.SequenceMatcher(None, a, b).ratio()


class _LevenshteinWordSimilarity(_BaseWordSimilarity):

    def compute(self, a, b):
        return relative(a, b)


def rank_words(word, terms, reverse=True):
    ws = component.queryUtility(IWordSimilarity)
    result = ws.rank(word, terms, reverse) if ws is not None else 0
    return result


#: Default translation table
_default_trans_table = None


@interface.implementer(IContentTranslationTable)
def _default_content_translation_table():

    global _default_trans_table

    if _default_trans_table is None:
        name = resource_filename(__name__, "punctuation-en.txt")
        with open(name, 'r') as src:
            lines = src.readlines()

        _default_trans_table = {}
        for line in lines:
            line = line.replace('\n', '')
            splits = line.split('\t')
            repl = splits[4] or None if len(splits) >= 5 else None
            _default_trans_table[int(splits[0])] = text_(repl)

    return _default_trans_table


def clean_special_characters(source, replacement=u''):
    """
    remove regular expression special chars
    """
    if source:
        for c in special_regexp_chars:
            source = source.replace(c, replacement)
    return source
