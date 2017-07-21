#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Language detection interfaces

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.schema.field import TextLine


class ILanguage(interface.Interface):
    """
    represent a language
    """
    code = TextLine(title=u"language iso-639-1 code", required=True)

    name = TextLine(title=u"language name", required=False)


class IAlchemyLanguage(ILanguage):
    """
    represent a language
    """
    ISO_639_1 = TextLine(title=u"language iso-639-1 code", 
                         required=True)  # alias for code

    ISO_639_2 = TextLine(title=u"language iso-639-2 code", 
                         required=False)

    ISO_639_3 = TextLine(title=u"language iso-639-3 code", 
                         required=False)

    name = TextLine(title=u"language name", required=False)


class ILanguageDetector(interface.Interface):

    def __call___(content):
        """
        Return an ILanguage(s) associated with the specified content

        :param content: Text to process
        """
