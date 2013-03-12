#-*- coding: utf-8 -*-
#
# Created on Feb 6, 2013
#
# @author: rm4dillo
#
# $Id$
#

from modsecurity_exception_factory.correlation.correlation import Correlation
from modsecurity_exception_factory.correlation.correlation_merge_delegate import CorrelationMergeDelegate
import unittest

class TestCorrelationMergeDelegate(unittest.TestCase):

    def testMergeCorrelationIterable(self):
        # After merging, the following correlation tree:
        # 
        #  a = a1
        #         b = b1
        #                 c = c1
        #                         d = d1, d2, d3, d4
        #                 c = c2
        #                         d = d1, d2, d3
        #                 c = c4
        #                         d = d1, d2, d3
        #                 c = c3
        #                         d = d1, d2, d3
        #         b = b2
        #                 c = c1
        #                         d = d1, d2, d3
        #                 c = c2
        #                         d = d1, d2, d3
        #         b = b3
        #                 d = d1
        #                         c = c1, c2
        #                 d = d2
        #                         c = c1, c2
        #                 d = d3
        #                         c = c1, c2
        #         b = b4
        #                 c = c5
        #                         d = d5
        #                 c = c6
        #                         d = d6
        #         d = d7
        #                 c = c7
        #                         b = b4
        # 
        # ...becomes: 
        # 
        # 
        #  a = a1
        #         b = b1
        #                 d = d4, d2, d3, d1
        #                         c = c1
        #                 d = d2, d3, d1
        #                         c = c3, c2, c4
        #         d = d2, d3, d1
        #                 c = c2, c1
        #                         b = b2, b3
        #         b = b4
        #                 c = c5
        #                         d = d5
        #                 c = c6
        #                         d = d6
        #                 c = c7
        #                         d = d7

        merger = CorrelationMergeDelegate()

        # a1 -> b1 -> c1
        c1 = Correlation('c',
                         {u"c1"},
                         itemCount = 50, # This can be greater than the sum as some sub correlations might have been dropped by filters.
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('d', {u"d1"}, itemCount = 10),
                                                                               Correlation('d', {u"d2"}, itemCount = 10),
                                                                               Correlation('d', {u"d3"}, itemCount = 10),
                                                                               Correlation('d', {u"d4"}, itemCount = 10)]))

        # a1 -> b1 -> c2
        c2 = Correlation('c',
                         {u"c2"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('d', {u"d1"}, itemCount = 10),
                                                                               Correlation('d', {u"d2"}, itemCount = 10),
                                                                               Correlation('d', {u"d3"}, itemCount = 10)]))

        # a1 -> b1 -> c4
        c4 = Correlation('c',
                         {u"c4"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('d', {u"d1"}, itemCount = 10),
                                                                               Correlation('d', {u"d2"}, itemCount = 10),  
                                                                               Correlation('d', {u"d3"}, itemCount = 10)]))

        # a1 -> b1 -> c3
        c3 = Correlation('c',
                         {u"c3"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('d', {u"d1"}, itemCount = 10),
                                                                               Correlation('d', {u"d2"}, itemCount = 10),
                                                                               Correlation('d', {u"d3"}, itemCount = 10)]))

        # a1 -> b1   
        b1 = Correlation('b',
                         {u"b1"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([c1, c2, c4, c3]))

        # a1 -> b2 -> c1
        c1 = Correlation('c',
                         {u"c1"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('d', {u"d1"}, itemCount = 10),
                                                                               Correlation('d', {u"d2"}, itemCount = 10),
                                                                               Correlation('d', {u"d3"}, itemCount = 10)]))

        # a1 -> b2 -> c2
        c2 = Correlation('c',
                         {u"c2"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('d', {u"d1"}, itemCount = 10),
                                                                               Correlation('d', {u"d2"}, itemCount = 10),
                                                                               Correlation('d', {u"d3"}, itemCount = 10)]))

        # a1 -> b2
        b2 = Correlation('b',
                         {u"b2"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([c1, c2]))

        # a1 -> b3 -> d1
        d1 = Correlation('d',
                         {u"d1"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('c', {u"c1"}, itemCount = 10),
                                                                               Correlation('c', {u"c2"}, itemCount = 10)]))

        # a1 -> b3 -> d2
        d2 = Correlation('d',
                         {u"d2"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('c', {u"c1"}, itemCount = 10),
                                                                               Correlation('c', {u"c2"}, itemCount = 10)]))

        # a1 -> b3 -> d3
        d3 = Correlation('d',
                         {u"d3"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([Correlation('c', {u"c1"}, itemCount = 10),
                                                                               Correlation('c', {u"c2"}, itemCount = 10)]))
        
        # a1 -> b3
        b3 = Correlation('b',
                         {u"b3"},
                         itemCount = 50,
                         subCorrelationList = merger.mergeCorrelationIterable([d1, d2, d3]))

        # a1 -> b4 -> c5 -> d5
        d5 = Correlation('d', {u"d5"}, itemCount = 10)

        # a1 -> b4 -> c5
        c5 = Correlation('c', {u"c5"}, itemCount = 10, subCorrelationList = merger.mergeCorrelationIterable([d5]))

        # a1 -> b4 -> c6 -> d6
        d6 = Correlation('d', {u"d6"}, itemCount = 10)

        # a1 -> b4 -> c6
        c6 = Correlation('c', {u"c6"}, itemCount = 10, subCorrelationList = merger.mergeCorrelationIterable([d6]))

        # a1 -> b4
        b4 = Correlation('b', {u"b4"}, itemCount = 30, subCorrelationList = merger.mergeCorrelationIterable([c5, c6]))

        # a1 -> d7 -> c7 -> b4
        b4_2 = Correlation('b', {u"b4"}, itemCount = 10)
        
        # a1 -> d7 -> c7
        c7 = Correlation('c', {u"c7"}, itemCount = 10, subCorrelationList = merger.mergeCorrelationIterable([b4_2]))
        
        # a1 -> d7
        d7 = Correlation('d', {u"d7"}, itemCount = 10, subCorrelationList = merger.mergeCorrelationIterable([c7]))
        
        # a1
        a1 = Correlation('a', {u"a1"}, itemCount = 400, subCorrelationList = merger.mergeCorrelationIterable([b1, b2, b3, b4, d7]))
        
        self.assertEqual("""\
a (count=400) = a1
        b (count=50) = b1
                c (count=50) = c1
                        d (count=50) = d1, d2, d3, d4
                d (count=150) = d1, d2, d3
                        c (count=150) = c2, c3, c4
        c (count=100) = c1, c2
                d (count=100) = d1, d2, d3
                        b (count=100) = b2, b3
        b (count=30) = b4
                c (count=10) = c5
                        d (count=10) = d5
                c (count=10) = c6
                        d (count=10) = d6
                d (count=10) = d7
                        c (count=10) = c7
""", repr(a1))

    def testMergeVariableDuplicate(self):
        pass

    def testMergeWithDifferentVariableNameList(self):
        pass
