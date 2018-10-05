#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface

from nti.schema.field import Number
from nti.schema.field import ValidTextLine


class IConcept(interface.Interface):
    """
    Represent a concept
    """
    text = ValidTextLine(title=u"concept text", required=True)

    relevance = Number(title=u"concept relevance", required=False)

    resource = ValidTextLine(title=u"Resource name", required=False)


class IConceptTagger(interface.Interface):

    def __call___(content):
        """
        Return the IConcept(s) associated with the specified content

        :param content: Text to process
        """
