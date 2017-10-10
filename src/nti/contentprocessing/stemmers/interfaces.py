#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface


class IStemmer(interface.Interface):

    def stem(token, lang='en'):
        """
        Return the stem from the specified token
        """
