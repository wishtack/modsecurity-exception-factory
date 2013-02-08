#-*- coding: utf-8 -*-
#
# Created on Feb 6, 2013
#
# @author: rm4dillo
#
# $Id$
#

from modsecurity_exception_factory.correlation.correlation import Correlation
import unittest

class TestCorrelation(unittest.TestCase):

    def testMerge(self):
        """
After merging, the following correlation tree:

 a = a1
        b = b1
                c = c1
                        d = d1, d2, d3, d4
                c = c2
                        d = d1, d2, d3
                c = c4
                        d = d1, d2, d3
                c = c3
                        d = d1, d2, d3
        b = b2
                c = c1
                        d = d1, d2, d3
                c = c2
                        d = d1, d2, d3
        b = b3
                d = d1
                        c = c1, c2
                d = d2
                        c = c1, c2
                d = d3
                        c = c1, c2

...becomes: 


 a = a1
        b = b1
                d = d4, d2, d3, d1
                        c = c1
                d = d2, d3, d1
                        c = c3, c2, c4
        d = d2, d3, d1
                c = c2, c1
                        b = b2, b3

"""
        # a1 -> b1 -> c1
        c1 = Correlation('c', u"c1")
        c1.extendSubCorrelation([Correlation('d', u"d1"),
                                 Correlation('d', u"d2"),
                                 Correlation('d', u"d3"),
                                 Correlation('d', u"d4")])

        # a1 -> b1 -> c2
        c2 = Correlation('c', u"c2")
        c2.extendSubCorrelation([Correlation('d', u"d1"),
                                 Correlation('d', u"d2"),
                                 Correlation('d', u"d3")])

        # a1 -> b1 -> c4
        c4 = Correlation('c', u"c4")
        c4.extendSubCorrelation([Correlation('d', u"d1"),
                                 Correlation('d', u"d2"),
                                 Correlation('d', u"d3")])

        # a1 -> b1 -> c3
        c3 = Correlation('c', u"c3")
        c3.extendSubCorrelation([Correlation('d', u"d1"),
                                 Correlation('d', u"d2"),
                                 Correlation('d', u"d3")])

        # a1 -> b1   
        b1 = Correlation('b', u"b1")
        b1.extendSubCorrelation([c1, c2, c4, c3])

        # a1 -> b2 -> c1
        c1 = Correlation('c', u"c1")
        c1.extendSubCorrelation([Correlation('d', u"d1"),
                                 Correlation('d', u"d2"),
                                 Correlation('d', u"d3")])

        # a1 -> b2 -> c2
        c2 = Correlation('c', u"c2")
        c2.extendSubCorrelation([Correlation('d', u"d1"),
                                 Correlation('d', u"d2"),
                                 Correlation('d', u"d3")])

        # a1 -> b2
        b2 = Correlation('b', u"b2")
        b2.extendSubCorrelation([c1, c2])

        # a1 -> b3 -> d1
        d1 = Correlation('d', u"d1")
        d1.extendSubCorrelation([Correlation('c', u"c1"),
                                 Correlation('c', u"c2")])

        # a1 -> b3 -> d2
        d2 = Correlation('d', u"d2")
        d2.extendSubCorrelation([Correlation('c', u"c1"),
                                 Correlation('c', u"c2")])

        # a1 -> b3 -> d3
        d3 = Correlation('d', u"d3")
        d3.extendSubCorrelation([Correlation('c', u"c1"),
                                 Correlation('c', u"c2")])
        
        # a1 -> b3
        b3 = Correlation('b', u"b3")
        b3.extendSubCorrelation([d1, d2, d3])

        # a1
        a1 = Correlation('a', u"a1")
        a1.extendSubCorrelation([b1, b2, b3])

        self.assertEqual("""\
a = a1
        b = b1
                d = d1, d2, d3, d4
                        c = c1
                d = d1, d2, d3
                        c = c2, c3, c4
        d = d1, d2, d3
                c = c1, c2
                        b = b2, b3
""", self._correlationRepr(a1))

    def testMergeVariableDuplicate(self):
        pass

    def testMergeWithDifferentVariableNameList(self):
        pass

    def _correlationRepr(self, correlation, indent = u""):
        variableValueList = list(correlation._variableValueSet)
        variableValueList.sort()
        reprString = u"%s%s = %s\n" % (indent, correlation._variableName, u", ".join(variableValueList))
        for subCorrelation in correlation._subCorrelationList:
            reprString += self._correlationRepr(subCorrelation, indent + u"        ")
        return reprString