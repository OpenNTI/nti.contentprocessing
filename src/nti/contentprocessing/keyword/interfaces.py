#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.schema.field import Int
from nti.schema.field import Number
from nti.schema.field import ListOrTuple
from nti.schema.field import ValidTextLine


class IContentKeyWord(interface.Interface):
    """
    represent a key word found in a content
    """
    token = ValidTextLine(title="word token", required=True)
    relevance = Number(title="word relevance", required=False)


class ITermExtractKeyWord(IContentKeyWord):
    """
    represent a key word found in a content
    """
    frequency = Int(title="word frequency", required=False)
    strength = Int(title="word strength", required=False)
    terms = ListOrTuple(value_type=ValidTextLine(title="Term"),
                        title="terms associated with token", required=False)


class ITermExtractFilter(interface.Interface):
    """
    Defines a key word extractor filter
    """

    def __call__(word, occur, strength):
        """
        filter specified key word

        :param word: word to filter
        :param occur: word frequency
        :param strength: word strength
        """


class IBaseyWordExtractor(interface.Interface):

    def __call___(content, *args, **kwargs):
        """
        Return the keywords associated with the specified content

        :param content: Text to process
        """


class IKeyWordExtractor(IBaseyWordExtractor):
    pass


class ITermExtractKeyWordExtractor(interface.Interface):
    pass
