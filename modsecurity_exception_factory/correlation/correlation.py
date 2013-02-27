#-*- coding: utf-8 -*-
#
# Created on Feb 6, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract
from itertools import imap
import copy

class Correlation:
    """
A correlation is a tree-chained object. Each correlation object a.k.a. node, contains a variable name, a set of variable values
corresponding to the variable name and a list of children nodes called subcorrelations.
"""

    @contract
    def __init__(self,
                 variableName,
                 variableValueSet,
                 subCorrelationIterable = None,
                 itemCount = None,
                 merge = True):
        """
    :param merge: Internal use. It is set to False when the subCorrelationIterable must be kept as is.

    :type variableName: str
    :type variableValueSet: Iterable
    :type subCorrelationIterable: Iterable|None
    :type itemCount: int|None
    :type merge: bool
"""

        self._checkSubCorrelationIterableOrItemCount(subCorrelationIterable, itemCount)
        
        self._variableName = variableName
        self._variableValueSet = variableValueSet
        self._itemCount = itemCount
        self._subCorrelationList = []
        
        if subCorrelationIterable is not None:
            if merge:        
                for correlation in subCorrelationIterable:
                    self._addSubCorrelationAndTryToMerge(correlation)
            else:
                self._subCorrelationList = list(subCorrelationIterable)
        
    def itemCount(self):
        if self._itemCount is not None:
            return self._itemCount
        else:
            return sum(imap(lambda c: c.itemCount(), self._subCorrelationList))

    def _checkSubCorrelationIterableOrItemCount(self, subCorrelationIterable, itemCount):
        """
    :type subCorrelationIterable: Iterable|None
    :type itemCount: int|None
"""
        # This is a 'xor', itemCount and subCorrelationList can't be both None or both not None.
        if itemCount is None and subCorrelationIterable is None:
            raise TypeError(u"'itemCount' and 'subCorrelationIterable' can't be both None.")

    def _addSubCorrelationAndTryToMerge(self, newCorrelation):
        # First sub newCorrelation...
        if len(self._subCorrelationList) == 0:
            self._subCorrelationList.append(newCorrelation)
            return

        # Making a list of variables that can be merged between the last and the new newCorrelation.
        lastCorrelation = self._subCorrelationList[-1]
        lastCorrelationTrunkVariableDict = lastCorrelation._mergeableVariableDict()
        lastCorrelationSubCorrelationList = lastCorrelation._unmergeableSubCorrelationList()
        newCorrelationTrunkVariableDict = newCorrelation._mergeableVariableDict()
        newCorrelationSubCorrelationList = newCorrelation._unmergeableSubCorrelationList()
        
        
        # Common variables.
        commonVariableDict = {}
        for variableName, variableValueSet in lastCorrelationTrunkVariableDict.items():
            if newCorrelationTrunkVariableDict.get(variableName, None) == variableValueSet:
                commonVariableDict[variableName] = variableValueSet
        
        # List of distinct variables between the two correlations trunks.
        distinctVariableNameList = list(set(lastCorrelationTrunkVariableDict.keys())\
                                        .union(set(newCorrelationTrunkVariableDict.keys()))
                                        - set(commonVariableDict.keys()))

        # There's only one variable that differs, we merge the values from both correlations (last and new)...        
        if len(lastCorrelationSubCorrelationList) == 0 \
           and len(newCorrelationSubCorrelationList) == 0 \
           and len(distinctVariableNameList) == 1:
            variableName = distinctVariableNameList[0]
            variableValueSet = lastCorrelationTrunkVariableDict[variableName]\
                               .union(newCorrelationTrunkVariableDict[variableName])
            itemCount = lastCorrelation.itemCount() + newCorrelation.itemCount()
            subCorrelationList = self._variableDictToCorrelationTreeList({variableName: variableValueSet},
                                                                         itemCount = itemCount)
            
        # ...otherwise we make the branches (as they can't be merged)...
        else:
            # ...and we remove the common items from the trunk in order to keep only those that are distinct.
            for variableName in commonVariableDict:
                del lastCorrelationTrunkVariableDict[variableName]
                del newCorrelationTrunkVariableDict[variableName]
            
            subCorrelationList = []
            subCorrelationList += self._variableDictToCorrelationTreeList(lastCorrelationTrunkVariableDict,
                                                                          subCorrelationList = lastCorrelationSubCorrelationList,
                                                                          itemCount = lastCorrelation.itemCount())
            subCorrelationList += self._variableDictToCorrelationTreeList(newCorrelationTrunkVariableDict,
                                                                          subCorrelationList = newCorrelationSubCorrelationList,
                                                                          itemCount = newCorrelation.itemCount())

        # ...and we try to make one newCorrelation with common variables.
        # If there common variables, the returned list will contain only one newCorrelation.
        # Otherwise it will contain two correlations.
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
    def _variableDictToCorrelationTreeList(self, variableDict, subCorrelationList = None, itemCount = None):
        """
    This will make a correlation with every item from :param:variableDict and chain them
    (the first item will be the root correlation node and the last one will be the leaf correlation node).
    If :param:subCorrelationList is not None, the last correlation will use it as it's children.
    Returns a list containing the root correlation node but if there's no item in :param:variableDict,
    this will return :param:subCorrelationList.

    :type variableDict: dict(str:)
    :type subCorrelationList: list|None
    :type itemCount: int|None
"""
        correlation = None
        for variableName, variableValueSet in reversed(variableDict.items()):
            # We set correlate to 'False' otherwise we'll fall in a infinite loop.
            correlation = Correlation(variableName,
                                      variableValueSet = variableValueSet,
                                      itemCount = itemCount,
                                      subCorrelationIterable = subCorrelationList,
                                      merge = False)
            subCorrelationList = [correlation]

        if correlation is not None:
            return [correlation]
        else:
            return subCorrelationList

    def __repr__(self, indent = u""):
        variableValueList = list(self._variableValueSet)
        variableValueList.sort()
        variableValueListAsString = u", ".join([unicode(v) for v in variableValueList])
        reprString = u"{indent}{variableName} (count={itemCount}) = {variableValueList}\n"\
            .format(indent = indent,
                    itemCount = self.itemCount(),
                    variableName = self._variableName,
                    variableValueList = variableValueListAsString)
        for subCorrelation in self._subCorrelationList:
            reprString += subCorrelation.__repr__(indent + u"        ")
        return reprString
