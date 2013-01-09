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
from modsecurity_exception_factory.modsecurity_audit_data_source.i_modsecurity_audit_data_source import \
    IModsecurityAuditDataSource
from modsecurity_exception_factory.modsecurity_audit_data_source.modsecurity_audit_orange_data_table_factory import \
    ModsecurityAuditOrangeDataTableFactory
import Orange.data.filter
import datetime
import orange
import orngAssoc

new_contract('IModsecurityAuditDataSource', IModsecurityAuditDataSource)
new_contract('OrangeDataTable', Orange.data.Table)

class ImpossibleError(Exception):
    pass

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
        for variableSetDict in self._exhaustiveVariableSetDictIterable(data, self._variableNameList):
            yield variableSetDict

    def _exhaustiveVariableSetDictIterable(self, data, variableNameList, variableSetDict = None):
        # Initializing local variables.
        if variableSetDict is None:
            variableSetDict = {}
        
        # Recursion end.
        isLeaf = len(variableNameList) <= 1
        
        ruleGroup = orange.AssociationRulesInducer(data, support = 0, classification_rules = True)
        orngAssoc.sort(ruleGroup, ['support', 'n_left'])

        for rule in ruleGroup:
            ruleVariableSetDict = variableSetDict.copy()
            
            # We only consider rules that use the attributes that have not been used yet. (i.e. in variableNameList) 
            ruleVariableNameList = self._ruleToVariableNameList(data.domain, rule)
            if not set(ruleVariableNameList).issubset(set(variableNameList)):
                continue
            
            # Select data that matches rule.
            matchingData = self._filterDataByRule(data, rule)

            # Data has already been consumed by other rules.
            if len(matchingData) == 0:
                continue
            else:
                # We remove the matched data from the data table.
                data = self._filterDataByRule(data, rule, negate = True)

            # Adding rule'a attributes the attribute dict.
            for name, value in self._ruleToVariableDict(data.domain, rule).items():
                if name not in variableSetDict:
                    ruleVariableSetDict[name] = set()
                    
                ruleVariableSetDict[name].add(value)

            # This is a "leaf", we regroup the last variable's values from all the rules.
            if isLeaf:
                variableSetDict = ruleVariableSetDict
                continue
            
            # List of variables that still have to be defined.
            remainingVariableNameList = filter(lambda v: v not in ruleVariableNameList, variableNameList)
            # We must continue...
            if len(remainingVariableNameList) > 0:                
                for completeVariableSetDict in self._exhaustiveVariableSetDictIterable(matchingData,
                                                                   remainingVariableNameList,
                                                                   ruleVariableSetDict.copy()):
                    yield completeVariableSetDict
            # No more variables to find, we don't have to go deeper.
            else:
                yield ruleVariableSetDict

        # Avoids double yields.
        if isLeaf:
            yield variableSetDict
        
        if len(data) > 0:
            raise ImpossibleError(u"Call the developers!")

    def _ruleToVariableDict(self, domain, rule):
        attributeDict = {}
        for attribute in domain:
            attributeName = attribute.name
            attributeValue = rule.left[attribute].value
            if attributeValue != self._EMPTY_ATTRIBUTE_VALUE:
                attributeDict[attributeName] = attributeValue
        return attributeDict

    def _ruleToVariableNameList(self, domain, rule):
        return list(self._ruleToVariableDict(domain, rule).keys())
    
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
