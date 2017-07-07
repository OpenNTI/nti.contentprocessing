#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.contentprocessing.monkey import patch
patch()

logger = __import__('logging').getLogger(__name__)

import re
import six
import sys

default_ngram_minsize = 2
default_ngram_maxsize = 20  # average word size in English is 5.10
default_word_tokenizer_expression = r"(?x)(?:[A-Z]\.)+ | \$?\d+(?:\.\d+)?%? | \w+(?:[-']\w+)*"

default_word_tokenizer_pattern = re.compile(default_word_tokenizer_expression,
                                            re.I | re.MULTILINE | re.DOTALL | re.UNICODE)

space_pattern = re.compile(r'\s+', re.UNICODE)

special_regexp_chars = (
    '.', '\\', '^', '$', '.', '|', '?', '*', '+', '(', ')', '[', '{'
)


def _makenon_alpha_re():
    non_alpha = [u'[^']
    for i in range(sys.maxunicode):
        c = six.unichr(i)
        if c.isalpha():
            non_alpha.append(c)
        non_alpha.append(u']')
    non_alpha = u"".join(non_alpha)
    return re.compile(non_alpha, re.UNICODE)

non_alpha_pattern = _makenon_alpha_re()
del _makenon_alpha_re
