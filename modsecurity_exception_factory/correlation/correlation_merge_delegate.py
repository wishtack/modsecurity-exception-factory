#-*- coding: utf-8 -*-
#
# Created on Mar 11, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .correlation import Correlation
from contracts import contract, new_contract
from itertools import imap
from synthetic import synthesizeMember, synthesizeConstructor

new_contract('Correlation', Correlation)

@synthesizeMember('maximumValueCountThreshold', contract = 'int|None', readOnly = True)
@synthesizeConstructor()
class CorrelationMergeDelegate(object):
    """Takes care of merging correlations"""
    
    @contract
    def mergeCorrelationIterable(self, correlationIterable):
        """
        :type correlationIterable: Iterable
"""

        # Merge items.
        correlationIterable = self._mergeCorrelationIterable(correlationIterable)

        # Remove "big" nodes.
        if self._maximumValueCountThreshold is not None:
            correlationIterable = self._removeNodesWithTooManyValues(correlationIterable,
                                                                     self._maximumValueCountThreshold)

        return correlationIterable

    @contract
    def _mergeCorrelationIterable(self, correlationIterable):
        """
        :type correlationIterable: Iterable
"""
        lastCorrelation = None
        for correlation in correlationIterable:
            # 'mergedCorrelationList' might contain one value if the merge succeeds or if it's the first correlation,
            # otherwise if it's impossible to merge, this will return two values.
            mergedCorrelationList = self._tryToMerge(correlation, lastCorrelation)
            
            # Couldn't merge the two items, we yield the first one and we keep the last one in order to try to merge it
            # with the next yield.
            if len(mergedCorrelationList) > 1:
                yield mergedCorrelationList[0]
                
            lastCorrelation = mergedCorrelationList[-1]
        
        # We yield the last item (if the iterable was not empty).
        if lastCorrelation is not None:
            yield lastCorrelation

    @contract
    def _tryToMerge(self, correlation, lastCorrelation):
        """Tries to merge ``correlation`` and ``lastCorrelation`` and returns one :class:`Correlation <Correlation>`
        if the merge succeeds, or if ``lastCorrelation`` is None, otherwise this will simply return both values.

        :type correlation: Correlation
        :type lastCorrelation: Correlation|None
"""
        # First correlation....
        if lastCorrelation is None:
            return [correlation]

        # Making a list of variables that can be merged between the last and the new correlation.
        lastCorrelationTrunkVariableDict = lastCorrelation.mergeableVariableDict()
        lastCorrelationSubCorrelationList = lastCorrelation.unmergeableSubCorrelationList()
        newCorrelationTrunkVariableDict = correlation.mergeableVariableDict()
        newCorrelationSubCorrelationList = correlation.unmergeableSubCorrelationList()
        
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
            itemCount = lastCorrelation.itemCount() + correlation.itemCount()
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
                                                                          itemCount = lastCorrelation.itemCount(),
                                                                          subCorrelationList = lastCorrelationSubCorrelationList)
            subCorrelationList += self._variableDictToCorrelationTreeList(newCorrelationTrunkVariableDict,
                                                                          itemCount = correlation.itemCount(),
                                                                          subCorrelationList = newCorrelationSubCorrelationList)

        # ...and we try to make one correlation with common variables.
        # If there common variables, the returned list will contain only one correlation.
        # Otherwise it will contain two correlations.
        mergedCorrelationList = self._variableDictToCorrelationTreeList(commonVariableDict,
                                                                        sum(imap(lambda c: c.itemCount(), subCorrelationList)),
                                                                        subCorrelationList)
        return mergedCorrelationList

    @contract
    def _variableDictToCorrelationTreeList(self, variableDict, itemCount, subCorrelationList = []):
        """
        This will make a correlation with every item from :param:variableDict and chain them
        (the first item will be the root correlation node and the last one will be the leaf correlation node).
        If :param:subCorrelationList is not None, the last correlation will use it as it's children.
        Returns a list containing the root correlation node but if there's no item in :param:variableDict,
        this will return :param:subCorrelationList.
    
        :type variableDict: dict(str:)
        :type itemCount: int
        :type subCorrelationList: list
"""
        correlation = None
        for variableName, variableValueSet in reversed(variableDict.items()):
            # We set correlate to 'False' otherwise we'll fall in a infinite loop.
            correlation = Correlation(variableName,
                                      variableValueSet = variableValueSet,
                                      itemCount = itemCount,
                                      subCorrelationList = subCorrelationList)
            subCorrelationList = [correlation]

        if correlation is not None:
            return [correlation]
        else:
            return subCorrelationList

    @contract
    def _removeNodesWithTooManyValues(self, correlationIterable, maximumValueCountThreshold):
        """
        :type correlationIterable: Iterable
        :type maximumValueCountThreshold: int
"""
        for correlation in correlationIterable:
            if len(correlation.variableValueSet()) > maximumValueCountThreshold:
                for subCorrelation in correlation.subCorrelationList():
                    yield subCorrelation
            else:
                yield correlation
