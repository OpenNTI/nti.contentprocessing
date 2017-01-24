#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
POS tagger interfaces

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface


class ITagger(interface.Interface):
    """
    Defines a POS tagger
    """

    def tag(tokens):
        """
        tag the specified tokens
        """


class INLTKTagger(ITagger):
    """
    Defines an NTLK POS tagger
    """


class IStanfordTagger(ITagger):
    """
    Defines an Standford POS tagger
    """
