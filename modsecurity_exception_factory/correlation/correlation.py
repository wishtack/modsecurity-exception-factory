#-*- coding: utf-8 -*-
#
# Created on Feb 6, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract
from synthetic.decorators import synthesizeConstructor, synthesizeMember

@synthesizeConstructor()
class Correlation:

    @contract
    def __init__(self, variableName, variableValue = None, variableValueSet = None, subCorrelationList = None):
        """
    :type variableName: str
    :type variableValue: unicode|None
    :type variableValueSet: Iterable|None
    :type subCorrelationList: list|None
"""
        self._variableName = variableName
        
        if variableValueSet is None:
            self._variableValueSet = {variableValue}
        else:
            self._variableValueSet = variableValueSet
            
        if subCorrelationList is None:
            subCorrelationList = []
        self._subCorrelationList = subCorrelationList

    def extendSubCorrelation(self, correlationIterable):
        for correlation in correlationIterable:
            self.addSubCorrelation(correlation)

    def addSubCorrelation(self, correlation):
        # First sub correlation...
        if len(self._subCorrelationList) == 0:
            self._subCorrelationList.append(correlation)
            return

        # @todo ...checking that sub correlation have the same domain.

        # ...otherwise.
        lastCorrelation = self._subCorrelationList[-1]
        if not lastCorrelation._hasOnlyOneBranch() or not correlation._hasOnlyOneBranch():
            self._subCorrelationList.append(correlation)
            return
        
        # Listing similar and different variables.
        lastVariableDict = lastCorrelation._variableDict()
        currentVariableDict = correlation._variableDict()
        
        lastKeyList = list(lastVariableDict.keys())
        currentKeyList = list(currentVariableDict.keys())
        lastKeyList.sort()
        currentKeyList.sort()
        if lastKeyList != currentKeyList:
            raise Exception()
        
        similarVariableNameList = []
        differentVariableNameList = []
        for key in lastVariableDict.keys():
            if currentVariableDict[key] == lastVariableDict[key]:
                similarVariableNameList.append(key)
            else:
                differentVariableNameList.append(key)
        
        # Merging different variable (if there's only one)
        subCorrelationList = []
        if len(differentVariableNameList) == 1:
            key = differentVariableNameList[0]
            valueSet = currentVariableDict[key].union(lastVariableDict[key])
            subCorrelationList.append(Correlation(key,
                                                  variableValueSet = valueSet))

        elif len(differentVariableNameList) > 1:
            lastCorrelationChildrenList = []
            currentCorrelationChildrenList = []
            for key in differentVariableNameList:
                lastCorrelation = Correlation(key,
                                              variableValueSet = lastVariableDict[key],
                                              subCorrelationList = lastCorrelationChildrenList)
                lastCorrelationChildrenList = [lastCorrelation]

                currentCorrelation = Correlation(key,
                                                 variableValueSet = currentVariableDict[key],
                                                 subCorrelationList = currentCorrelationChildrenList)
                currentCorrelationChildrenList = [currentCorrelation]
            subCorrelationList =  lastCorrelationChildrenList + currentCorrelationChildrenList
        
        for key in similarVariableNameList:
            subCorrelationList = [Correlation(key,
                                              variableValueSet = currentVariableDict[key],
                                              subCorrelationList = subCorrelationList)]
        del self._subCorrelationList[-1]
        self._subCorrelationList.extend(subCorrelationList)

    def __repr__(self, indent = u""):
        variableValueList = list(self._variableValueSet)
        variableValueList.sort()
        variableValueListAsString = u", ".join([unicode(v) for v in variableValueList])
        reprString = u"%s%s = %s\n" % (indent, self._variableName, variableValueListAsString)
        for subCorrelation in self._subCorrelationList:
            reprString += subCorrelation.__repr__(indent + u"        ")
        return reprString

    def _hasOnlyOneBranch(self):
        subCorrelationCount = len(self._subCorrelationList)
        if subCorrelationCount == 0:
            return True
        elif subCorrelationCount > 1:
            return False
        else:
            return self._subCorrelationList[0]._hasOnlyOneBranch()

    def _variableDict(self):
        subCorrelationCount = len(self._subCorrelationList)
        if subCorrelationCount == 0:
            return {self._variableName: self._variableValueSet}
        elif subCorrelationCount > 1:
            raise Exception()
        else:
            variableDict = self._subCorrelationList[0]._variableDict()
            variableDict[self._variableName] = self._variableValueSet
            return variableDict
        