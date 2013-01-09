#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract
from contracts.main import new_contract
import Orange.data.filter
import copy
import itertools
import orange
import orngAssoc

new_contract('OrangeDataTable', Orange.data.Table)

class ImpossibleError(Exception):
    def __init__(self):
        super(self.__class__, self).__init__(u"Call the developers!")

class OrangeCorrelationEngine:
    
    _EMPTY_ATTRIBUTE_VALUE = '~'

    def __init__(self, variableNameList):
        self._variableNameList = variableNameList
    
    @contract
    def correlate(self, data, minimumOccurrenceCountThreshold = 0):
        """Yields correlations as dict objects.
The dict keys are variables' names and the values are set objects containing variables' values. 
    :type data: OrangeDataTable
    :type minimumOccurrenceCountThreshold: int
"""
        if len(data) == 0:
            return
        
        # Association.
        support = float(minimumOccurrenceCountThreshold) / len(data)
        ruleGroup = orange.AssociationRulesInducer(data, support = support, classification_rules = True)
        
        # Filter data.
        data = self._filterDataByRuleGroup(data, ruleGroup)
        data.remove_duplicates()

        # 'ruleGroup' contains the rules that we are looking for but some of them are too generic as they might
        # specify values for only few variables. We need an exhaustive list of possible correlations.
        #
        # Ex.:
        #     We get:
        #
        #        {'hostName': 'test.domain.com',
        #         'payloadContainer': 'ARGS:param'}
        #
        #     But we need something like in order to make the exceptions:
        #
        #        {'hostName': ['test.domain.com'],
        #         'payloadContainer': ['ARGS:param'],
        #         'requestFileName': ['/a.php', '/b.php'],
        #         'ruleId': ['111111', '222222']}
        #        {'hostName': ['test.domain.com'],
        #         'payloadContainer': ['ARGS:param'],
        #         'requestFileName': ['/c.php', '/d.php'],
        #         'ruleId': ['333333']}
        for variableSetDict in self._correlationDictIterable(data, set(self._variableNameList)):
            variableToRemoveBuffer = set()
            for variableTuple in variableSetDict:
                if isinstance(variableTuple, tuple):
                    for variable in variableTuple:
                        variableToRemoveBuffer.add(variable)
            
            for variable in variableToRemoveBuffer:
                del variableSetDict[variable]
            yield variableSetDict

    def _correlationDictIterable(self, data, variableNameSet):
        # This list contains correlation dicts that have to be merged.
        correlationDictToMergeList = []

        ruleGroup = orange.AssociationRulesInducer(data, support = 0, classification_rules = True)
        orngAssoc.sort(ruleGroup, ['support', 'n_left'])

        for rule in ruleGroup:
            # We only consider rules that use the attributes that have not been used yet. (i.e. in variableNameSet) 
            ruleVariableNameSet = self._ruleToVariableNameSet(data.domain, rule)
            if not ruleVariableNameSet.issubset(variableNameSet):
                continue
            
            # Select data that matches rule.
            matchingData = self._filterDataByRule(data, rule)

            # Data has already been consumed by other rules.
            if len(matchingData) == 0:
                continue
            else:
                # We remove the matched data from the data table.
                data = self._filterDataByRule(data, rule, negate = True)

            # Fill correlation dict with rule's variable values.
            correlationDict = self._makeCorrelationDictWithRule(data.domain, rule, variableNameSet)

            # List of variables that still have to be defined.
            remainingVariableNameSet = variableNameSet - ruleVariableNameSet
                        
            # No more variables to find, we don't have to go deeper...
            if len(remainingVariableNameSet) == 0:
                correlationDictToMergeList.append(correlationDict)

            # ... otherwise, we must continue...
            else:
                iterable = self._correlationDictIterable(matchingData, remainingVariableNameSet)
                firstSubCorrelationDict = None
                
                for index, subCorrelationDict in enumerate(iterable):
                    if index == 0:
                        firstSubCorrelationDict = subCorrelationDict
                        continue
                    
                    # More than one item has been yielded.
                    if index == 1:
                        yield self._unionCorrelationDict([correlationDict, firstSubCorrelationDict])
                        firstSubCorrelationDict = None

                    yield self._unionCorrelationDict([correlationDict, subCorrelationDict])
                
                # Only one item was yielded.
                if firstSubCorrelationDict is not None:
                    correlationDict = self._unionCorrelationDict([correlationDict, firstSubCorrelationDict])
                    correlationDictToMergeList.append(correlationDict)

        # Merging correlations that can be merged.
        for mergedCorrelationDict in self._mergeCorrelationDictList(correlationDictToMergeList):
            yield mergedCorrelationDict
        
        if len(data) > 0:
            raise ImpossibleError()

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

        if len(differentAttributeList) == 1:
            mergeableAttributeList = differentAttributeList
        else:
            mergeableAttributeList = list(filter(lambda attribute: \
                                                 len(correlationDictFirst[attribute]) \
                                                 == len(correlationDictSecond[attribute]) \
                                                 == 1,
                                                 self._correlationDictSimpleKeyIterable(differentAttributeList)))

        # When 'currentMergeAttributeList' is None, it means that there's no merging context yet...
        # ... and 'mergeableAttributeList == currentMergeAttributeList' means that everything is fine, we can merge.
        if currentMergeAttributeList is None or (mergeableAttributeList == currentMergeAttributeList):
            mergeableAttributeList.sort()
            return mergeableAttributeList
        else:
            return None
    
    def _mergeCorrelationDict(self, mergeAttributeList, correlationDictFirst, correlationDictSecond):
        # @todo remove hack
        if len(mergeAttributeList) == 1:
            mergedAttribute = mergeAttributeList[0]
        else:
            mergedAttribute = tuple(mergeAttributeList)

        # First, copy the first correlation dict and only keep common attributes...
        mergedCorrelationDict = copy.deepcopy(correlationDictFirst)
#        for attribute in mergeAttributeList:
#            if attribute in mergedCorrelationDict:
#                del mergedCorrelationDict[attribute]

        # ... we make the merged attribute value list if it does not exist yet...
        if mergedAttribute not in mergedCorrelationDict:
            mergedCorrelationDict[mergedAttribute] = set()
        mergedAttributeValueSet = mergedCorrelationDict[mergedAttribute]
         
        # ... if there's only one attribute to merge, then copy values...
        if len(mergeAttributeList) == 1:
            for correlationDict in [correlationDictFirst, correlationDictSecond]:
                mergedAttributeValueSet.update(correlationDict[mergedAttribute])
        
        # ... and finally we merge the common attributes.
        else:
            for correlationDict in [correlationDictFirst, correlationDictSecond]:
                valueAsList = []
                for attribute in mergeAttributeList:
                    if len(correlationDict[attribute]) != 1:
                        raise ImpossibleError()
                    valueAsList.append(list(correlationDict[attribute])[0])
                valueAsTuple = tuple(valueAsList)
                mergedAttributeValueSet.add(valueAsTuple)

        return mergedCorrelationDict

    def _differentAttributeList(self, correlationDictFirst, correlationDictSecond):
        if self._attributeSet(correlationDictFirst) != self._attributeSet(correlationDictSecond):
            raise ImpossibleError()
        
        differentAttributeSet = set()
        for key in self._correlationDictSimpleKeyIterable(correlationDictFirst):
            if correlationDictFirst[key] != correlationDictSecond[key]:
                differentAttributeSet.add(key)
        return list(differentAttributeSet)

    def _correlationDictSimpleKeyIterable(self, correlationDict):
        return filter(lambda key: isinstance(key, str), correlationDict)

    def _attributeSet(self, correlationDict):
        # Ignoring merged attributes tuples.
        return set(filter(lambda key: isinstance(key, str), correlationDict.keys()))

    def _ruleToVariableDict(self, domain, rule):
        attributeDict = {}
        for attribute in domain:
            attributeName = attribute.name
            attributeValue = rule.left[attribute].value
            if attributeValue != self._EMPTY_ATTRIBUTE_VALUE:
                attributeDict[attributeName] = attributeValue
        return attributeDict

    def _ruleToVariableNameSet(self, domain, rule):
        return set(self._ruleToVariableDict(domain, rule).keys())
    
    def _filterDataByRule(self, data, rule, negate = False):
        valueFilter = self._ruleToFilter(data.domain, rule)
        return valueFilter(data, negate = negate)

    def _filterDataByRuleGroup(self, data, ruleGroup):
        valueFilterList = [self._ruleToFilter(data.domain, rule) for rule in ruleGroup]
        disjunctionFilter = Orange.data.filter.Disjunction(valueFilterList)
        return disjunctionFilter(data)

    def _ruleToFilter(self, domain, rule):
        valueFilter = Orange.data.filter.Values()
        valueFilter.domain = domain
        for attributeName, attributeValue in self._ruleToVariableDict(domain, rule).items():
            attribute = domain[attributeName]
            valueSubFilter = Orange.data.filter.ValueFilterDiscrete(position = domain.features.index(attribute),
                                                               values = [Orange.data.Value(attribute,
                                                                                           attributeValue)])
            valueFilter.conditions.append(valueSubFilter)
        return valueFilter

    def _fillCorrelationDictWithRule(self, correlationDict, domain, rule):
        for name, value in self._ruleToVariableDict(domain, rule).items():
            valueSet = correlationDict.get(name, set())
            valueSet.add(value)
            correlationDict[name] = valueSet            

    def _makeCorrelationDictWithRule(self, domain, rule, variableNameSet):
        correlationDict = {}
        ruleDict = self._ruleToVariableDict(domain, rule)
        for name in variableNameSet:
            correlationDict[name] = set()
            if name in ruleDict:
                correlationDict[name].add(ruleDict[name])
        return correlationDict

    def _unionCorrelationDict(self, correlationDictList):
        resultCorrelationDict = {}
        
        for correlationDict in correlationDictList:
            for attribute, valueSet in correlationDict.items():
                valueSet = correlationDict[attribute]
                resultValueSet = resultCorrelationDict.get(attribute, set())
                resultValueSet.update(valueSet)
                resultCorrelationDict[attribute] = resultValueSet
        return resultCorrelationDict
