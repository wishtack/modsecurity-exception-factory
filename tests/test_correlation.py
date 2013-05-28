#-*- coding: utf-8 -*-
#
# Created on May 28, 2013
#
# @author: Younes JAAIDI <yjaaidi@shookalabs.com>
#
# $Id$
#

from modsecurity_exception_factory.correlation.correlation import Correlation

import unittest

class TestCorrelation(unittest.TestCase):

    def setUp(self):
        # a (count=400) = a1
        #         b (count=50) = b1
        #                 c (count=50) = c1
        #                         d (count=50) = d1, d2, d3, d4
        #                 d (count=150) = d1, d2, d3
        #                         c (count=150) = c2, c3, c4
        #         c (count=100) = c1, c2
        #                 d (count=100) = d1, d2, d3
        #                         b (count=100) = b2, b3
        
        self._correlation_dict = {'variable_name': 'a',
                                  'variable_value_list': [u"a1"],
                                  'item_count': 400,
                                  'sub_correlation_list': [
                                      {'variable_name': 'b',
                                       'variable_value_list': [u"b1"],
                                       'item_count': 50,
                                       'sub_correlation_list': [
                                           {'variable_name': 'c',
                                            'variable_value_list': [u"c1"],
                                            'item_count': 50,
                                            'sub_correlation_list': [
                                                {'variable_name': 'd',
                                                 'variable_value_list': [u"d1", u"d2", u"d3", u"d4"],
                                                 'item_count': 50}
                                            ]},
                                           {'variable_name': 'd',
                                            'variable_value_list': [u"d1", u"d2", u"d3"],
                                            'item_count': 150,
                                            'sub_correlation_list': [
                                                {'variable_name': 'c',
                                                 'variable_value_list': [u"c2", u"c3", u"c4"],
                                                 'item_count': 150}
                                            ]}
                                       ]},
                                      {'variable_name': 'c',
                                       'variable_value_list': [u"c1", u"c2"],
                                       'item_count': 100,
                                       'sub_correlation_list': [
                                           {'variable_name': 'd',
                                            'variable_value_list': [u"d1", u"d2", u"d3"],
                                            'item_count': 100,
                                            'sub_correlation_list': [
                                                {'variable_name': 'b',
                                                 'variable_value_list': [u"b2", u"b3"],
                                                 'item_count': 100}
                                            ]}
                                       ]}
                                  ]}

    def test_correlation_parse_dict(self):
        correlation = Correlation.load_from_dict(self._correlation_dict)

        self.assertEqual('a', correlation.variable_name())
        self.assertEqual({u"a1"}, correlation.variable_value_set())
        self.assertEqual(400, correlation.item_count())
        self.assertEqual(2, len(correlation.sub_correlation_list()))
        
        sub_correlation = correlation.sub_correlation_list()[1]
        self.assertEqual('c', sub_correlation.variable_name())
        self.assertEqual({u"c1", u"c2"}, sub_correlation.variable_value_set())
        self.assertEqual(100, sub_correlation.item_count())
        self.assertEqual(1, len(sub_correlation.sub_correlation_list()))

    def test_correlation_to_dict(self):
        # Loading...
        correlation = Correlation.load_from_dict(self._correlation_dict)
        
        # ...then dumping...
        self.assertEqual(self._correlation_dict, correlation.to_dict())
