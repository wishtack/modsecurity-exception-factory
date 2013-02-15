#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .correlation import Correlation
from .i_correlation_progress_listener import ICorrelationProgressListener
from contracts import contract, new_contract
import copy

new_contract('ICorrelationProgressListener', ICorrelationProgressListener)

class ImpossibleError(Exception):
    def __init__(self):
        super(self.__class__, self).__init__(u"Call the developers!")

class CorrelationEngine:
    
    _EMPTY_ATTRIBUTE_VALUE = '~'

    @contract
    def __init__(self, variableNameList, ignoredVariableDict = {}):
        """
    :type variableNameList: list(str)
    :type ignoredVariableDict: dict(str:list(unicode))
"""
        self._variableNameList = variableNameList
        self._ignoredVariableDict = ignoredVariableDict
        self._progressListenerList = []
        self._count = 0
        self._totalCount = 0
    
    @contract
    def correlate(self, dataSource, minimumOccurrenceCountThreshold = 0):
        """
Yields :class:Correlation objects.
    :type minimumOccurrenceCountThreshold: int
"""
        itemDictIterable = dataSource.itemDictIterable(self._variableNameList)
        
        # Removing items matching 'ignoredVariableDict'.
        itemDictIterable = self._removeItemsMatchingIgnoredVariableDict(itemDictIterable)
        
        # Initialize counters.
        self._count = 0
        self._totalCount = len(itemDictIterable)
        for correlation in self._correlationIterable(itemDictIterable, self._variableNameList):
            yield correlation

    @contract
    def addProgressListener(self, progressListener):
        """
    :type progressListener: ICorrelationProgressListener
"""
        if progressListener not in self._progressListenerList:
            self._progressListenerList.append(progressListener)

    def _removeItemsMatchingIgnoredVariableDict(self, itemDictIterable):
        for variableName, variableValueList in self._ignoredVariableDict.items():
            for variableValue in variableValueList:
                itemDictIterable = itemDictIterable.filterByVariable(variableName, variableValue, negate = True)
        return itemDictIterable

    def _correlationIterable(self, itemDictIterable, variableNameList):
        # Merge all values when there's only one variable remaining.
        if len(variableNameList) == 1:
            # Variable name.
            variableName = variableNameList[0]
            # Values set.
            variableValueSet = set([d[variableName] for d in itemDictIterable])
            # Increment progress and inform listeners.
            self._incrementProgress(len(itemDictIterable))
            # Correlation leaf is ready.
            yield Correlation(variableName, variableValueSet = variableValueSet)
            return

        mostFrequentVariableNameAndValue = itemDictIterable.mostFrequentVariableAndValue(variableNameList)
        while mostFrequentVariableNameAndValue is not None:
            variableName, variableValue = list(mostFrequentVariableNameAndValue.items())[0]

            # Select data that matches rule.
            matchingItemDictIterable = itemDictIterable.filterByVariable(variableName, variableValue)
            itemDictIterable = itemDictIterable.filterByVariable(variableName, variableValue, negate = True)

            # Data has already been consumed by other rules.
            if len(matchingItemDictIterable) == 0:
                raise ImpossibleError()

            # List of variables that still have to be defined.
            remainingVariableNameList = copy.copy(variableNameList)
            remainingVariableNameList.remove(variableName)

            # ... otherwise, we must continue...
            correlation = Correlation(variableName, variableValue)
            correlation.extendSubCorrelation(self._correlationIterable(matchingItemDictIterable,
                                                                       remainingVariableNameList))
            yield correlation
            mostFrequentVariableNameAndValue = itemDictIterable.mostFrequentVariableAndValue(variableNameList)
        
        if len(itemDictIterable) > 0:
            raise ImpossibleError()

    def _mostFrequentVariableValueSet(self, itemDictIterable, variableNameList):
        correlationDict = {}
        mostFrequentVariableNameAndValue = itemDictIterable.distinct().mostFrequentVariableAndValue(variableNameList)
        if mostFrequentVariableNameAndValue is None:
            return None
        
        for variableName, variableValue in mostFrequentVariableNameAndValue.items():
            correlationDict[variableName] = set(variableValue)
        return correlationDict

    @contract
    def _incrementProgress(self, itemCount):
        """
    :type itemCount: int
"""
        self._count += itemCount
        for progressListener in self._progressListenerList:
            progressListener.progress(self._count, self._totalCount)
