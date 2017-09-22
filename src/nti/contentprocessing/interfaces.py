#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface
from zope import deferredimport

from zope.mimetype.interfaces import mimeTypeConstraint

from nti.contentfragments.schema import PlainText
from nti.contentfragments.schema import PlainTextLine

from nti.schema.field import Int
from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import TextLine
from nti.schema.field import ListOrTuple


class IContentTranslationTable(interface.Interface):
    """
    marker interface for content translationt table
    """


class IContentTokenizer(interface.Interface):

    def tokenize(data):
        """
        tokenize the specifeid text data
        """


class INgramComputer(interface.Interface):

    minsize = Int(title=u"Min ngram size.", required=True)
    maxsize = Int(title=u"Max ngram size", required=False)

    def compute(text):
        """
        compute the ngrams for the specified text
        """


class IWordSimilarity(interface.Interface):

    def compute(a, b):
        """
        compute a similarity ratio for the specified words
        """

    def rank(word, terms, reverse=True):
        """
        return the specified terms based on the distance to the specified word
        """


class IWordTokenizerExpression(interface.Interface):
    """
    marker interface for word tokenizer regular expression
    """


class IWordTokenizerPattern(interface.Interface):
    """
    marker interface for word tokenizer regular expression pattern
    """


class IWatsonAPIKey(interface.Interface):
    username = interface.Attribute("The username")
    password = interface.Attribute("The password")

# Metadata extraction


class IImageMetadata(interface.Interface):
    """
    Holds information about a particular image.
    """

    url = TextLine(title=u"The URL to resolve the image")

    width = Number(title=u"The width in pixels of the image",
                   required=False)

    height = Number(title=u"The height in pixels of the image",
                    required=False)


class IContentMetadata(interface.Interface):
    """
    Metadata extracted from existing content.
    Each of the attributes is filled in based on the best
    possible extraction and each may be missing or empty.
    """

    title = PlainTextLine(title=u"The title of the content",
                          required=False,
                          default=u'')

    description = PlainText(title=u"A short description of the content",
                            required=False,
                            default=u'')

    creator = PlainTextLine(title=u"A description of the creator",
                            description=u"Possibly one or more names or even an organization.",
                            required=False,
                            default=u'')

    images = ListOrTuple(Object(IImageMetadata),
                         title=u"Any images associated with this content, typically thumbnails",
                         default=())

    contentMimeType = TextLine(title=u"The Mime Type of the content",
                               constraint=mimeTypeConstraint,
                               required=False)

    contentLocation = TextLine(title=u"The canonical URL of the content",
                               description=(u"After metadata extraction, we may have obtained"
                                            u" a canonical URL for the content, different from"
                                            u" the source location. For permanent storage and use"
                                            u" this is the value to use, not the source location."),
                               required=False)

    sourceLocation = TextLine(title=u"The location of the source content",
                              description=(u"The unprocessed, original location of the content"
                                           u" used to find the metadata. May be a local file"
                                           u" path or a URL."),
                              required=False)

    sourcePath = TextLine(title=u"A local file path to the content",
                          description=(u"If the content was a local file, or"
                                       u" had to be downloaded to a temporary file"
                                       u" that was preserved following metadata processing,"
                                       u" this will be the path to that file."),
                          required=False)


class IContentMetadataExtractorArgs(interface.Interface):
    """
    Arguments for extracting content metadata.
    """

    stream = interface.Attribute("A file-like object for reading the content")
    bidirectionalstream = interface.Attribute("A file-like object for reading the content, supports seeking")
    bytes = interface.Attribute("Raw bytes of the content.")
    text = interface.Attribute("Decoded text of the content.")


class IContentMetadataExtractor(interface.Interface):
    """
    Intended to be registered as named utilities with the name of the mimetype
    they handle.
    """

    def extract_metadata(args):
        """
        Called with an :class:`IContentMetadataExtractorArgs`.

        :return: An :class:`IContentMetadata`
        """


class IContentMetadataURLHandler(interface.Interface):
    """
    Intended to be registered as named utilities having the name of
    a URL scheme.
    """

    def __call__(url):
        """
        Called with a string giving the URL.

        :return: An :class:`IContentMetadata`.
        """


class IStopWords(interface.Interface):

    def stopwords(language):
        """
        return stop word for the specified language
        """

    def available_languages():
        """
        available languages
        """

deferredimport.initialize()
deferredimport.deprecatedFrom(
    "Moved to nti.contentfragments.interfaces",
    "nti.contentfragments.interfaces",
    "IPunctuationCharPattern",
    "IPunctuationCharExpression",
    "IPunctuationCharPatternPlus",
    "IPunctuationCharExpressionPlus")
