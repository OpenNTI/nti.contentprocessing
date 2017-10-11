#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class NLTKConfiguringTestLayer(SharedConfiguringTestLayer):

    @classmethod
    def setUp(cls):
        cls.setUpPackages()
        import nltk
        nltk.download(['brown'], quiet=True, force=False)
