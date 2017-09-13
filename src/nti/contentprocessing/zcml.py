#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from functools import partial

from zope import interface

from zope.component.zcml import utility

from zope.configuration import fields

from nti.contentprocessing._compat import text_

from nti.contentprocessing.interfaces import IWatsonAPIKey

from nti.contentprocessing.watson import create_api_key


class IRegisterWatsonAPIKeyDirective(interface.Interface):
    """
    The arguments needed for registering a key
    """
    name = fields.TextLine(title=u"The name",
                           required=False)

    username = fields.TextLine(title=u"The username", required=True)

    password = fields.TextLine(title=u"The password", required=True)


def registerWatsonAPIKey(_context, username, password, name=''):
    """
    Register an watson key with the given alias
    """
    factory = partial(create_api_key, 
                      username=text_(username), 
                      password=text_(password))
    utility(_context, provides=IWatsonAPIKey, factory=factory, name=name)
