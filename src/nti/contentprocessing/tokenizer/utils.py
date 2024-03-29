#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

# Natural Language Toolkit: Internal utility functions
#
# Copyright (C) 2001-2016 NLTK Project
# Author: Steven Bird <stevenbird1@gmail.com>
#         Edward Loper <edloper@gmail.com>
#         Nitin Madnani <nmadnani@ets.org>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import re
import types

import six

if six.PY3:  # pragma: no cover
    def get_im_class(meth): return meth.__self__.__class__
else:
    def get_im_class(meth): return meth.im_class

logger = __import__('logging').getLogger(__name__)


def _mro(cls):
    r"""
    Return the method resolution order for ``cls`` -- i.e., a list
    containing ``cls`` and all its base classes, in the order in which
    they would be checked by ``getattr``.  For new-style classes, this
    is just cls.__mro__.  For classic classes, this can be obtained by
    a depth-first left-to-right traversal of ``__bases__``.
    """
    if isinstance(cls, type):
        return cls.__mro__
    else:
        result = [cls]
        for base in cls.__bases__:
            result.extend(_mro(base))
        return result
mro = _mro


def overridden(method):
    r"""
    :return: True if ``method`` overrides some method with the same
    name in a base class.  This is typically used when defining
    abstract base classes or interfaces, to allow subclasses to define
    either of two related methods:

            >>> class EaterI:
            ...     '''Subclass must define eat() or batch_eat().'''
            ...     def eat(self, food):
            ...         if overridden(self.batch_eat):
            ...             return self.batch_eat([food])[0]
            ...         else:
            ...             raise NotImplementedError()
            ...     def batch_eat(self, foods):
            ...         return [self.eat(food) for food in foods]

    :type method: instance method
    """
    # [xx] breaks on classic classes!
    if      isinstance(method, types.MethodType) \
        and get_im_class(method) is not None:
        name = method.__name__
        funcs = [cls.__dict__[name]
                 for cls in _mro(get_im_class(method))
                 if name in cls.__dict__]
        return len(funcs) > 1
    else:  # pragma: no cover
        raise TypeError('Expected an instance method.')


def string_span_tokenize(s, sep):
    r"""
    Return the offsets of the tokens in *s*, as a sequence of ``(start, end)``
    tuples, by splitting the string at each occurrence of *sep*.

            >>> from nltk.tokenize.util import string_span_tokenize
            >>> s = '''Good muffins cost $3.88\nin New York.  Please buy me
            ... two of them.\n\nThanks.'''
            >>> list(string_span_tokenize(s, " "))
            [(0, 4), (5, 12), (13, 17), (18, 26), (27, 30), (31, 36), (37, 37),
            (38, 44), (45, 48), (49, 55), (56, 58), (59, 73)]

    :param s: the string to be tokenized
    :type s: str
    :param sep: the token separator
    :type sep: str
    :rtype: iter(tuple(int, int))
    """
    if len(sep) == 0:
        raise ValueError("Token delimiter must not be empty")
    left = 0
    while True:
        try:
            right = s.index(sep, left)
            if right != 0:
                yield left, right
        except ValueError:
            if left != len(s):
                yield left, len(s)
            break
        left = right + len(sep)


def regexp_span_tokenize(s, regexp):
    r"""
    Return the offsets of the tokens in *s*, as a sequence of ``(start, end)``
    tuples, by splitting the string at each successive match of *regexp*.

            >>> from nltk.tokenize.util import regexp_span_tokenize
            >>> s = '''Good muffins cost $3.88\nin New York.  Please buy me
            ... two of them.\n\nThanks.'''
            >>> list(regexp_span_tokenize(s, r'\s'))
            [(0, 4), (5, 12), (13, 17), (18, 23), (24, 26), (27, 30), (31, 36),
            (38, 44), (45, 48), (49, 51), (52, 55), (56, 58), (59, 64), (66, 73)]

    :param s: the string to be tokenized
    :type s: str
    :param regexp: regular expression that matches token separators (must not be empty)
    :type regexp: str
    :rtype: iter(tuple(int, int))
    """
    left = 0
    for m in re.finditer(regexp, s):
        right, next_ = m.span()
        if right != left:
            yield left, right
        left = next_
    yield left, len(s)
