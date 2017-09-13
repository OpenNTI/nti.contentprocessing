#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import not_none
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from zope import component

from nti.contentprocessing.interfaces import IWatsonAPIKey

import nti.testing.base


ZCML_STRING = u"""
<configure	xmlns="http://namespaces.zope.org/zope"
			xmlns:i18n="http://namespaces.zope.org/i18n"
			xmlns:zcml="http://namespaces.zope.org/zcml"
			xmlns:watson="http://nextthought.com/ntp/watson">

	<include package="zope.component" file="meta.zcml" />
	<include package="zope.security" file="meta.zcml" />
	<include package="zope.component" />
	<include package="." file="meta.zcml" />

	<watson:registerWatsonAPIKey
			username="myusername"
			password="mypassword" />

</configure>
"""


class TestZcml(nti.testing.base.ConfiguringTestBase):

    def test_registration(self):
        self.configure_string(ZCML_STRING)
        watson_key = component.queryUtility(IWatsonAPIKey)
        assert_that(watson_key, is_(not_none()))
        assert_that(watson_key, validly_provides(IWatsonAPIKey))
        assert_that(watson_key, verifiably_provides(IWatsonAPIKey))
        assert_that(watson_key, has_property('username', "myusername"))
        assert_that(watson_key, has_property('password', "mypassword"))
