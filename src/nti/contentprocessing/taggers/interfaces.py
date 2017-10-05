#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

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
