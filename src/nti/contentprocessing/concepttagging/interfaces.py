#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import ListOrTuple
from nti.schema.field import ValidTextLine


class IConceptSource(interface.Interface):
    """
    Represent a concept source entry (e.g. linked data) 
    """
    source = ValidTextLine(title=u"source name", required=True)
    uri = ValidTextLine(title=u"source uri", required=True)


class IConcept(interface.Interface):
    """
    Represent a concept
    """
    text = ValidTextLine(title=u"concept text", required=True)
    relevance = Number(title=u"concept relevance", required=False)
    sources = ListOrTuple(title=u"Concept sources", min_length=0,
                          value_type=Object(IConceptSource, title=u"The source"))


class IConceptTagger(interface.Interface):

    def __call___(content):
        """
        Return the IConcept(s) associated with the specified content

        :param content: Text to process
        """
