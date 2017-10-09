#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from nti.schema.field import Int
from nti.schema.field import Number
from nti.schema.field import ListOrTuple
from nti.schema.field import ValidTextLine


class IContentKeyWord(interface.Interface):
    """
    represent a key word found in a content
    """
    token = ValidTextLine(title=u"word token", required=True)

    relevance = Number(title=u"word relevance", required=False)


class ITermExtractKeyWord(IContentKeyWord):
    """
    represent a key word found in a content
    """
    frequency = Int(title=u"word frequency", required=False)

    strength = Int(title=u"word strength", required=False)

    terms = ListOrTuple(value_type=ValidTextLine(title=u"Term"),
                        title=u"terms associated with token", required=False)


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
