#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from functools import partial

from zope import interface

from zope.component.zcml import utility

from zope.schema import TextLine

from nti.contentprocessing._compat import text_

from nti.contentprocessing.interfaces import IWatsonAPIKey

from nti.contentprocessing.watson import create_api_key

logger = __import__('logging').getLogger(__name__)


class IRegisterWatsonAPIKeyDirective(interface.Interface):
    """
    The arguments needed for registering a key
    """
    name = TextLine(title=u"The name",
                    required=False)

    username = TextLine(title=u"The username", required=True)

    password = TextLine(title=u"The password", required=True)


def registerWatsonAPIKey(_context, username, password, name=''):
    """
    Register an watson key with the given alias
    """
    factory = partial(create_api_key,
                      username=text_(username),
                      password=text_(password))
    utility(_context, provides=IWatsonAPIKey, factory=factory, name=name)
