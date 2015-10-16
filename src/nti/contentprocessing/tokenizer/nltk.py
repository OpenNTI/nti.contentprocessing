#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
import sre_parse
import sre_compile
import sre_constants

from nltk.tokenize import RegexpTokenizer

def compile_regexp_to_noncapturing(pattern, flags=0):
	"""
	Compile the regexp pattern after switching all grouping parentheses
	in the given regexp pattern to non-capturing groups.

	:type pattern: str
	:rtype: str

	Natural Language Toolkit: Internal utility functions
	Copyright (C) 2001-2015 NLTK Project
	"""
	def convert_regexp_to_noncapturing_parsed(parsed_pattern):
		res_data = []
		for key, value in parsed_pattern.data:
			if key == sre_constants.SUBPATTERN:
				_, subpattern = value
				value = (None, convert_regexp_to_noncapturing_parsed(subpattern))
			elif key == sre_constants.GROUPREF:
				msg = 'Regular expressions with back-references are not supported: {0}'.format(pattern)
				raise ValueError(msg)
			res_data.append((key, value))
		parsed_pattern.data = res_data
		parsed_pattern.pattern.groups = 1
		parsed_pattern.pattern.groupdict = {}
		return parsed_pattern

	parsed = convert_regexp_to_noncapturing_parsed(sre_parse.parse(pattern))
	return sre_compile.compile(parsed, flags=flags)

class DefaultRegexpTokenizer(RegexpTokenizer):

	def _check_regexp(self):
		"""
		Natural Language Toolkit: Internal utility functions
		Copyright (C) 2001-2015 NLTK Project
		"""
		if self._regexp is None:
			try:
				# Remove capturing parentheses -- if the regexp contains any
				# capturing parentheses, then the behavior of re.findall and
				# re.split will change.
				self._regexp = compile_regexp_to_noncapturing(self._pattern, self._flags)
			except re.error as e:
				raise ValueError('Error in regular expression %r: %s' % (self._pattern, e))
