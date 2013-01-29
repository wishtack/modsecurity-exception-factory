#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract
import copy
import itertools

class ImpossibleError(Exception):
    def __init__(self):
        super(self.__class__, self).__init__(u"Call the developers!")

class CorrelationEngine:
    
    _EMPTY_ATTRIBUTE_VALUE = '~'

    def __init__(self, variableNameList):
        self._variableNameList = variableNameList
    
    @contract
    def correlate(self, dataSource, minimumOccurrenceCountThreshold = 0):
        """Yields correlations as dict objects.
The dict keys are variables' names and the values are set objects containing variables' values.
    :type minimumOccurrenceCountThreshold: int
"""
        itemDictIterable = dataSource.itemDictIterable(self._variableNameList)
        for variableSetDict in self._correlationDictIterable(itemDictIterable, set(self._variableNameList)):
            yield variableSetDict

    def _correlationDictIterable(self, itemDictIterable, variableNameSet):
        # This list contains correlation dicts that have to be merged.
        correlationDictToMergeList = []

        # Merge all values when there's only one variable remaining.
        if len(variableNameSet) == 1:
            yield self._makeCorrelationDictWithOneVariable(itemDictIterable, variableNameSet)
            return

        iterationFunction = lambda: itemDictIterable.mostFrequentVariableAndValue(list(variableNameSet))
        for mostFrequentVariableNameAndValue in iter(iterationFunction, None):
            variableName, variableValue = list(mostFrequentVariableNameAndValue.items())[0]

            # Select data that matches rule.
            matchingItemDictIterable = itemDictIterable.filterByVariable(variableName, variableValue)

            # We remove the matched data from the data table.
            itemDictIterable = itemDictIterable.filterByVariable(variableName,
                                                                 variableValue,
                                                                 negate = True)

            # Data has already been consumed by other rules.
            if len(matchingItemDictIterable) == 0:
                raise ImpossibleError()

            # List of variables that still have to be defined.
            remainingVariableNameSet = variableNameSet - set([variableName])

            # ... otherwise, we must continue...
            subCorrelationDictIterable = self._correlationDictIterable(matchingItemDictIterable, remainingVariableNameSet)
            
            for subCorrelationDict in subCorrelationDictIterable:
                # Add current variable to sub correlation dictionary. 
                subCorrelationDict[variableName] = set([variableValue])
                correlationDictToMergeList.append(subCorrelationDict)

        # Merging correlations that can be merged.
        for mergedCorrelationDict in self._mergeCorrelationDictList(correlationDictToMergeList):
            yield mergedCorrelationDict
        
        if len(itemDictIterable) > 0:
            raise ImpossibleError()

    def _mostFrequentVariableValueSet(self, itemDictIterable, variableNameSet):
        correlationDict = {}
        mostFrequentVariableNameAndValue = itemDictIterable.mostFrequentVariableAndValue(list(variableNameSet))
        if mostFrequentVariableNameAndValue is None:
            return None
        
        for variableName, variableValue in mostFrequentVariableNameAndValue.items():
            correlationDict[variableName] = set(variableValue)
        return correlationDict

    def _makeCorrelationDictWithOneVariable(self, itemDictIterable, variableNameSet):
        variableName = list(variableNameSet)[0]
        variableValueSet = set()
        
        for itemDict in itemDictIterable:
            variableValueSet.add(itemDict[variableName])
        
        return {variableName: variableValueSet}

    def _mergeCorrelationDictList(self, correlationDictList):

        def dictAsKey(correlationDict):
            resultDict = {}
            for key, valueSet in correlationDict.items():
                if isinstance(key, str):
                    resultDict[key] = ",".join(valueSet)
            return resultDict

        def keyListAsKey(correlationDict):
            return list(correlationDict.keys())
            
        correlationDictList.sort(key = dictAsKey)
        for _, group in itertools.groupby(correlationDictList, key = keyListAsKey):
            # @todo merge multiple attributes.
            mergedCorrelationDict = None
            
            # Set of attributes that are used to make the current correlation merge.
            mergeAttributeList = None
            
            for correlationDict in group:
                if mergedCorrelationDict is None:
                    mergedCorrelationDict = copy.deepcopy(correlationDict)
                    continue

                mergeAttributeList = self._makeMergeAttributeList(mergeAttributeList, mergedCorrelationDict, correlationDict)
                if mergeAttributeList is not None:
                    mergedCorrelationDict = self._mergeCorrelationDict(mergeAttributeList,
                                                                       mergedCorrelationDict,
                                                                       correlationDict)
                else:
                    yield mergedCorrelationDict
                    mergeAttributeList = None
                    mergedCorrelationDict = copy.deepcopy(correlationDict)

            if mergedCorrelationDict is not None:
                yield mergedCorrelationDict

    def _makeMergeAttributeList(self, currentMergeAttributeList, correlationDictFirst, correlationDictSecond):
        """Return the set of attributes to merge or None if impossible to merge."""
        # Compare currently merged correlation and the new one.
        differentAttributeList = self._differentAttributeList(correlationDictFirst, correlationDictSecond)    
            
        if len(differentAttributeList) == 0:
            raise ImpossibleError()

        mergeAttributeList = differentAttributeList
        mergeAttributeList.sort()
        
        # If we have many different attributes we only merge them if they don't have multiple values.
        if (len(mergeAttributeList) > 1) \
            and any(map(lambda attribute: \
                               len(correlationDictFirst.get(attribute, set())) > 1 \
                               or len(correlationDictSecond.get(attribute, set())) > 1,
                      mergeAttributeList)):
            mergeAttributeList = None

        # When 'currentMergeAttributeList' is None, it means that there's no merging context yet...
        # ... and 'mergeAttributeList == curentMergeAttributeList' means that everything is fine, we are still in the same context, we can merge.
        if (currentMergeAttributeList is not None) and (mergeAttributeList != currentMergeAttributeList):
            mergeAttributeList = None

        return mergeAttributeList
    
    def _mergeCorrelationDict(self, mergeAttributeList, correlationDictFirst, correlationDictSecond):
        # @todo remove hack
        if len(mergeAttributeList) == 1:
            mergedAttribute = mergeAttributeList[0]
        else:
            mergedAttribute = tuple(mergeAttributeList)

        # First, copy the first correlation dict and only keep common attributes...
        mergedCorrelationDict = {}
        for attribute in correlationDictFirst:
            if attribute not in mergeAttributeList:
                mergedCorrelationDict[attribute] = correlationDictFirst[attribute].copy()

        # ... we make the merged attribute value list if it does not exist yet...
        mergedAttributeValueSet = mergedCorrelationDict.get(mergedAttribute, set())
        mergedCorrelationDict[mergedAttribute] = mergedAttributeValueSet
         
        # ... if there's only one attribute to merge, then copy values...
        if len(mergeAttributeList) == 1:
            for correlationDict in [correlationDictFirst, correlationDictSecond]:
                mergedAttributeValueSet.update(correlationDict[mergedAttribute])
        
        # ... and finally we merge the common attributes.
        else:
            for correlationDict in [correlationDictFirst, correlationDictSecond]:
                valueAsList = []
                for attribute in mergeAttributeList:
                    if attribute in correlationDict:
                        valueSet = correlationDict[attribute]
                        if len(valueSet) != 1:
                            raise ImpossibleError()
                        valueAsList.append(list(valueSet)[0])
                
                if len(valueAsList) > 0:
                    valueAsTuple = tuple(valueAsList)
                    mergedAttributeValueSet.add(valueAsTuple)

        return mergedCorrelationDict

    def _differentAttributeList(self, correlationDictFirst, correlationDictSecond):
        differentAttributeSet = set()
        for key in self._correlationDictSimpleKeyIterable(correlationDictSecond):
            if correlationDictFirst.get(key, None) != correlationDictSecond[key]:
                differentAttributeSet.add(key)

        return list(differentAttributeSet)

    def _correlationDictSimpleKeyIterable(self, correlationDict):
        return filter(lambda key: isinstance(key, str), correlationDict)

    def _attributeSet(self, correlationDict):
        # Ignoring merged attributes tuples.
        return set(filter(lambda key: isinstance(key, str), correlationDict.keys()))

    def _unionCorrelationDict(self, correlationDictList):
        resultCorrelationDict = {}
        
        for correlationDict in correlationDictList:
            for attribute, valueSet in correlationDict.items():
                valueSet = correlationDict[attribute]
                resultValueSet = resultCorrelationDict.get(attribute, set())
                resultValueSet.update(valueSet)
                resultCorrelationDict[attribute] = resultValueSet
        return resultCorrelationDict
