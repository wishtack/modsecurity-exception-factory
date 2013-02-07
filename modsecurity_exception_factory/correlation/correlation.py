#-*- coding: utf-8 -*-
#
# Created on Feb 6, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from synthetic.decorators import synthesizeConstructor, synthesizeMember

@synthesizeConstructor()
class Correlation:

    def __init__(self, variableName, variableValue):
        """
    :type variableName: str
    :type variableValue: unicode
"""
        self._variableName = variableName
        self._variableValueSet = set([variableValue])
        self._subCorrelationList = []

    def extendSubCorrelation(self, correlationIterable):
        for correlation in correlationIterable:
            self.addSubCorrelation(correlation)

    def addSubCorrelation(self, correlation):
        self._subCorrelationList.append(correlation)
