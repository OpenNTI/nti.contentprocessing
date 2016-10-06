#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import shutil
import tempfile
import subprocess

from simplejson.compat import StringIO

from zope import interface

from nti.contentprocessing.taggers.interfaces import IStanfordTagger

LANG_MODELS = {
	'':'english-left3words-distsim.tagger',
	'en': 'english-left3words-distsim.tagger'
}

def stanford_postagger(path=None):
	path = path or os.path.join(os.getenv('DATASERVER_DIR'), 'bin')
	path = os.path.join(os.path.expanduser(path), 'stanford_postagger')
	return path

def is_available(path=None):
	path = stanford_postagger(path)
	return os.path.exists(path)

class StanfordPostagger(object):
	
	lang = ''

	def _save_source(self, source):
		tmp_path = tempfile.mkdtemp()
		tmp_path = os.path.join(tmp_path, 'source.txt')
		with open(tmp_path, "wb") as f:
			if isinstance(source, (list, tuple)): # tokens
				f.write(' '.join(source))
			else:
				f.write(source)
		return tmp_path

	@staticmethod
	def parse_tags(source):
		result = []
		if not hasattr(source, "read"):
			source = StringIO(source)
			source.seek(0)
		for line in source:
			splits = line.strip().split('\t')
			if splits and len(splits) == 2 and splits[1].isupper():
				result.append(tuple(splits))
		return result
	
	def tag(self, source):
		if not is_available():
			return ()
		tmp_path = None
		try:
			model = LANG_MODELS.get(self.lang)
			tmp_path = self._save_source(source)
			process = [stanford_postagger(), model, tmp_path]
			logger.debug("Executing %s", process)
			tags_str = subprocess.check_output(process, stderr=None).strip()
			return self.parse_tags(tags_str)
		except Exception:
			logger.exception("Cannot get POS tags from using Stanford POS tagger")
			return ()
		finally:
			shutil.rmtree(tmp_path, True)

@interface.implementer(IStanfordTagger)
class EnglishStanfordPostagger(StanfordPostagger):	
	lang = 'en'
