#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenXerox lang detector

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import requests

from zope import interface

from nti.contentprocessing._compat import text_

from nti.contentprocessing.langdetection.model import Language

from nti.contentprocessing.langdetection.interfaces import ILanguageDetector

OPEN_XEROX_URL = 'https://services.open.xerox.com/RestOp/LanguageIdentifier/GetLanguageForString'

logger = __import__('logging').getLogger(__name__)


@interface.implementer(ILanguageDetector)
class _OpenXeroxLanguageDetector(object):

    __slots__ = ()

    @staticmethod
    def detect(content):
        result = None
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            "Accept": "text/plain"
        }
        params = {'document': text_(content)}
        try:
            r = requests.post(OPEN_XEROX_URL, data=params, headers=headers)
            data = r.json()
            if r.status_code == 200 and data:
                result = Language(code=text_(data))
            else:
                logger.error("%s is an invalid status response code; %s",
                             r.status_code, data)
        except Exception:  # pylint: disable=broad-except
            result = None
            logger.exception('Error while detecting language using OpenXerox')

        return result

    def __call__(self, content, **unused_kwargs):
        return self.detect(content)
