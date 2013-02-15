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
import copy

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

        # Making a list of variables that can be merged between the last and the new correlation.
        previousCorrelation = self._subCorrelationList[-1]
        previousCorrelationTrunkVariableDict = previousCorrelation._mergeableVariableDict()
        previousCorrelationSubCorrelationList = previousCorrelation._unmergeableSubCorrelationList()
        lastCorrelationTrunkVariableDict = correlation._mergeableVariableDict()
        lastCorrelationSubCorrelationList = correlation._unmergeableSubCorrelationList()
        
        
        # Common variables.
        commonVariableDict = {}
        for variableName, variableValueSet in previousCorrelationTrunkVariableDict.items():
            if lastCorrelationTrunkVariableDict.get(variableName, None) == variableValueSet:
                commonVariableDict[variableName] = variableValueSet
        
        # List of distinct variables between the two correlations trunks.
        distinctVariableNameList = list(set(previousCorrelationTrunkVariableDict.keys())\
                                        .union(set(lastCorrelationTrunkVariableDict.keys()))
                                        - set(commonVariableDict.keys()))

        # There's only one variable that differs, we merge the values.        
        if len(previousCorrelationSubCorrelationList) == 0 \
           and len(lastCorrelationSubCorrelationList) == 0 \
           and len(distinctVariableNameList) == 1:
            variableName = distinctVariableNameList[0]
            variableValueSet = previousCorrelationTrunkVariableDict[variableName]\
                               .union(lastCorrelationTrunkVariableDict[variableName])
            subCorrelationList = self._variableDictToCorrelationTreeList({variableName: variableValueSet})
            
        # Otherwise we add the branches.
        else:
            for variableName in commonVariableDict:
                del previousCorrelationTrunkVariableDict[variableName]
                del lastCorrelationTrunkVariableDict[variableName]
            
            subCorrelationList = []
            subCorrelationList += self._variableDictToCorrelationTreeList(previousCorrelationTrunkVariableDict,
                                                                          subCorrelationList = previousCorrelationSubCorrelationList)
            subCorrelationList += self._variableDictToCorrelationTreeList(lastCorrelationTrunkVariableDict,
                                                                          subCorrelationList = lastCorrelationSubCorrelationList)

        # Make correlation with common variables.
        subCorrelationList = self._variableDictToCorrelationTreeList(commonVariableDict, subCorrelationList)
        del self._subCorrelationList[-1]
        self._subCorrelationList.extend(subCorrelationList)

    def _mergeableVariableDict(self):
        """
Example:
    a = a1
            b = b1, b2
                    c = c1
                        d = d2
                    d = d1
                        c = c2

Will return:

    {'a': 'a1', 'b': set(['b1', 'b2'])}
"""
        mergeableVariableDict = {self._variableName: self._variableValueSet}
        
        # We fillup the dictionary recursively until there are no children or there's more than one child.
        if len(self._subCorrelationList) == 1:
            childMergeableVariableDict = self._subCorrelationList[0]._mergeableVariableDict()
            mergeableVariableDict.update(childMergeableVariableDict)
        return mergeableVariableDict
    
    def _unmergeableSubCorrelationList(self):
        """
Example:
    a = a1
            b = b1, b2
                    c = c1
                        d = d2
                    d = d1
                        c = c2

Will return two correlation objects corresponding to the following structures:
    
    c = c1
        d = d2
and
    d = d1
        c = c2
"""
        subCorrelationListLength = len(self._subCorrelationList)
        
        # Node has no children.
        if subCorrelationListLength == 0:
            return []
        
        # Node has only one child, we ask the child.
        elif subCorrelationListLength == 1:
            return self._subCorrelationList[0]._unmergeableSubCorrelationList()
        
        # Node has multiple children, those are the unmergeable correlations.
        else:
            return copy.copy(self._subCorrelationList)

    @contract
    def _variableDictToCorrelationTreeList(self, variableDict, subCorrelationList = None):
        """
    :type variableDict: dict(str:)
"""
        correlation = None
        for variableName, variableValueSet in reversed(variableDict.items()):
            correlation = Correlation(variableName,
                                      variableValueSet = variableValueSet,
                                      subCorrelationList = subCorrelationList)
            subCorrelationList = [correlation]

        if correlation is not None:
            return [correlation]
        else:
            return subCorrelationList

    def __repr__(self, indent = u""):
        variableValueList = list(self._variableValueSet)
        variableValueList.sort()
        variableValueListAsString = u", ".join([unicode(v) for v in variableValueList])
        reprString = u"%s%s = %s\n" % (indent, self._variableName, variableValueListAsString)
        for subCorrelation in self._subCorrelationList:
            reprString += subCorrelation.__repr__(indent + u"        ")
        return reprString
