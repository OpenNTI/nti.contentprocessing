#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import close_to
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property

import fudge

import os
import unittest

import simplejson

from nti.contentprocessing.concepttagging import concept_tag

from nti.contentprocessing.concepttagging.watson import analyze
from nti.contentprocessing.concepttagging.watson import get_ranked_concepts

from nti.contentprocessing.tests import SharedConfiguringTestLayer


class TestConceptTagger(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @property
    def sample(self):
        name = os.path.join(os.path.dirname(__file__), 'sample.txt')
        with open(name, "r") as f:
            return f.read()

    @property
    def response(self):
        name = os.path.join(os.path.dirname(__file__), 'response.json')
        with open(name, "r") as fp:
            return simplejson.load(fp)

    @fudge.patch('nti.contentprocessing.concepttagging.watson.analyze')
    def test_watson_concepts(self, mock_an):
        mock_an.is_callable().with_args().returns(self.response)
        concepts = get_ranked_concepts(self.sample)
        assert_that(concepts, has_length(8))

        concept = concepts[0]
        assert_that(concept, is_not(none()))
        assert_that(concept,
                    has_property('text', is_('Federal Bureau of Investigation')))
        assert_that(concept,
                    has_property('relevance', is_(close_to(0.97, 0.01))))
        assert_that(concept,
                    has_property('resource',
                                 'http://dbpedia.org/resource/Federal_Bureau_of_Investigation'))

    @fudge.patch('nti.contentprocessing.concepttagging.watson.analyze')
    def test_concept_tag(self, mock_an):
        mock_an.is_callable().with_args().returns(self.response)
        assert_that(concept_tag(self.sample, 'invalid'),
                    is_(()))
        assert_that(concept_tag(self.sample, 'en'),
                    has_length(8))

    def test_analyze(self):
        client = fudge.Fake().provides('analyze').returns(None)
        assert_that(analyze(client, ''), is_(none()))

    @fudge.patch('nti.contentprocessing.concepttagging.watson.analyze')
    def test_coverage(self, mock_grc):
        mock_grc.is_callable().raises(TypeError())
        assert_that(get_ranked_concepts(self.sample), 
                    is_([]))
