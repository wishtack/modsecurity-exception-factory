#-*- coding: utf-8 -*-
#
# Created on May 28, 2013
#
# @author: Younes JAAIDI <yjaaidi@shookalabs.com>
#
# $Id$
#

from modsecurity_exception_factory.correlation.correlation_serializer_yaml import \
    CorrelationSerializerYaml
from StringIO import StringIO
import unittest

class TestCorrelation(unittest.TestCase):

    def setUp(self):
        # a (count=400) = 0123456
        #         b (count=50) = b1
        #                 c (count=50) = c1
        #                         d (count=50) = d1, d2, d3, d4
        #                 d (count=150) = d1, d2, d3
        #                         c (count=150) = c2, c3, c4
        #         c (count=100) = c1, c2
        #                 d (count=100) = d1, d2, d3
        #                         b (count=100) = b2, b3
        # b (count=300) = b1, b2
        
        self._correlation_yaml_data = u"""\
variable_name: a
item_count: 400
variable_value_list:
- '0123456'
sub_correlation_list:
- variable_name: b
  item_count: 50
  variable_value_list:
  - b1
  sub_correlation_list:
  - variable_name: c
    item_count: 50
    variable_value_list:
    - c1
    sub_correlation_list:
    - variable_name: d
      item_count: 50
      variable_value_list:
      - d1
      - d2
      - d3
      - d4
  - variable_name: d
    item_count: 150
    variable_value_list:
    - d1
    - d2
    - d3
    sub_correlation_list:
    - variable_name: c
      item_count: 150
      variable_value_list:
      - c2
      - c3
      - c4
- variable_name: c
  item_count: 100
  variable_value_list:
  - c1
  - c2
  sub_correlation_list:
  - variable_name: d
    item_count: 100
    variable_value_list:
    - d1
    - d2
    - d3
    sub_correlation_list:
    - variable_name: b
      item_count: 100
      variable_value_list:
      - b2
      - b3
---
variable_name: b
item_count: 300
variable_value_list:
- b1
- b2
"""

    def test_load(self):
        correlation_list = list(CorrelationSerializerYaml().load(StringIO(self._correlation_yaml_data)))

        self.assertEqual(2, len(correlation_list))
        
        # Checking first item.
        correlation = correlation_list[0]
        
        self.assertEqual('a', correlation.variable_name())
        self.assertEqual({u"0123456"}, correlation.variable_value_set())
        self.assertEqual(400, correlation.item_count())
        self.assertEqual(2, len(correlation.sub_correlation_list()))
        
        sub_correlation = correlation.sub_correlation_list()[1]
        self.assertEqual('c', sub_correlation.variable_name())
        self.assertEqual({u"c1", u"c2"}, sub_correlation.variable_value_set())
        self.assertEqual(100, sub_correlation.item_count())
        self.assertEqual(1, len(sub_correlation.sub_correlation_list()))
        
        # Checking second item.
        correlation = correlation_list[1]
        
        self.assertEqual('b', correlation.variable_name())
        self.assertEqual({u"b1", u"b2"}, correlation.variable_value_set())
        self.assertEqual(300, correlation.item_count())
        self.assertEqual(0, len(correlation.sub_correlation_list()))

    def test_write(self):
        # Load...
        correlation_iterable = CorrelationSerializerYaml().load(StringIO(self._correlation_yaml_data))
                
        # ...then dump...
        output = StringIO()
        CorrelationSerializerYaml().write(correlation_iterable, output)
        self.assertEqual(self._correlation_yaml_data, output.getvalue())
