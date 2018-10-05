#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Language detection interfaces

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface

from nti.schema.field import Number
from nti.schema.field import TextLine


class ILanguage(interface.Interface):
    """
    represent a language
    """
    code = TextLine(title=u"language iso-639-1 code", required=True)

    name = TextLine(title=u"language name", required=False)


class IWatsonLanguage(ILanguage):
    """
    represent a language
    """
    confidence = Number(title=u"detection confidence",
                        required=False,
                        default=0)


class ILanguageDetector(interface.Interface):

    def __call___(content):
        """
        Return an ILanguage(s) associated with the specified content

        :param content: Text to process
        """
