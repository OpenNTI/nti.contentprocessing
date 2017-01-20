#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from functools import total_ordering

from zope import interface

from nti.contentprocessing.keyword.interfaces import IContentKeyWord

from nti.contentprocessing.representation import WithRepr

from nti.schema.eqhash import EqHash


@WithRepr
@EqHash('token',)
@total_ordering
@interface.implementer(IContentKeyWord)
class ContentKeyWord(object):

    __slots__ = ('token', 'relevance')

    def __init__(self, token=None, relevance=None):
        self.token = token
        self.relevance = relevance

    def __lt__(self, other):
        try:
            return self.relevance < other.relevance
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.relevance > other.relevance
        except AttributeError:
            return NotImplemented
