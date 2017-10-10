#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# All the patching uses private things so turn that warning off
# pylint: disable=W0212


def _patch_html5lib():
    import html5lib
    from html5lib._inputstream import HTMLBinaryInputStream

    class _HTMLBinaryInputStream(HTMLBinaryInputStream):

        def __init__(self, *args, **kwargs):
            if 'encoding' in kwargs:
                encoding = kwargs.pop('encoding', None)
                kwargs['override_encoding'] = encoding
            HTMLBinaryInputStream.__init__(self, *args, **kwargs)

    html5lib._inputstream.HTMLBinaryInputStream = _HTMLBinaryInputStream
_patch_html5lib()
del _patch_html5lib


def patch():
    pass
