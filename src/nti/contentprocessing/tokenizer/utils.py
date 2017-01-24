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

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
import sys
import types
import sre_parse
import sre_compile
import sre_constants

PY3 = sys.version_info[0] == 3
if PY3:
    get_im_class = lambda meth: meth.__self__.__class__
else:
    get_im_class = lambda meth: meth.im_class


def _mro(cls):
    """
    Return the method resolution order for ``cls`` -- i.e., a list
    containing ``cls`` and all its base classes, in the order in which
    they would be checked by ``getattr``.  For new-style classes, this
    is just cls.__mro__.  For classic classes, this can be obtained by
    a depth-first left-to-right traversal of ``__bases__``.
    """
    if isinstance(cls, type):
        return cls.__mro__
    else:
        mro = [cls]
        for base in cls.__bases__:
            mro.extend(_mro(base))
        return mro


def overridden(method):
    """
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
    else:
        raise TypeError('Expected an instance method.')


def add_metaclass(metaclass):
    """
    Class decorator for creating a class with a metaclass.
    """

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


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


def compile_regexp_to_noncapturing(pattern, flags=0):
    """
    Compile the regexp pattern after switching all grouping parentheses
    in the given regexp pattern to non-capturing groups.

    :type pattern: str
    :rtype: str
    """
    def convert_regexp_to_noncapturing_parsed(parsed_pattern):
        res_data = []
        for key, value in parsed_pattern.data:
            if key == sre_constants.SUBPATTERN:
                _, subpattern = value
                value = (
                    None, convert_regexp_to_noncapturing_parsed(subpattern))
            elif key == sre_constants.GROUPREF:
                msg = 'Regular expressions with back-references are not supported: %r' % pattern
                raise ValueError(msg)
            res_data.append((key, value))
        parsed_pattern.data = res_data
        parsed_pattern.pattern.groups = 1
        parsed_pattern.pattern.groupdict = {}
        return parsed_pattern

    parsed = convert_regexp_to_noncapturing_parsed(sre_parse.parse(pattern))
    return sre_compile.compile(parsed, flags=flags)
