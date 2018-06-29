#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,non-parent-init-called

def _patch_html5lib():
    try:
        import html5lib
        from html5lib._inputstream import HTMLBinaryInputStream
    
        class _HTMLBinaryInputStream(HTMLBinaryInputStream):
    
            def __init__(self, *args, **kwargs):
                if 'encoding' in kwargs:
                    encoding = kwargs.pop('encoding', None)
                    kwargs['override_encoding'] = encoding
                HTMLBinaryInputStream.__init__(self, *args, **kwargs)
    
        html5lib._inputstream.HTMLBinaryInputStream = _HTMLBinaryInputStream
    except ImportError:
        import warnings
        warnings.warn('Cannot patch html5lib HTMLBinaryInputStream',
                      DeprecationWarning, stacklevel=1)
_patch_html5lib()
del _patch_html5lib


def patch():
    pass
