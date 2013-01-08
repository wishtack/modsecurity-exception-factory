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
from modsecurity_exception_factory.orange_data_table_factory import OrangeDataTableFactory
from synthetic.decorators import synthesizeMember, synthesizeConstructor
import datetime
import itertools
import orange
import orngAssoc

new_contract('IModsecurityAuditDataSource', IModsecurityAuditDataSource)

@synthesizeMember('childrenResultList')
@synthesizeMember('attributeDict')
@synthesizeConstructor()
class Result:
    def __init__(self):
        self._attributeDict = {}
        self._childrenList = []
    
    def addChild(self, result):
        self._childrenList.append(result)
    
    def __str__(self):
        print(self._attributeDict)
        for child in self._childrenList:
            print("\t%s", child)

class ModsecurityAuditCorrelationEngine:
    
    _EMPTY_ATTRIBUTE_VALUE = '~'
    
    @contract
    def correlate(self, dataSource, minimumOccurrenceCountThreshold = 0):
        """
    :type dataSource: IModsecurityAuditDataSource
    :type minimumOccurrenceCountThreshold: int
"""

        variableNameList = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']
        
        print("%s data loaded" % datetime.datetime.now())
        data = OrangeDataTableFactory().data(dataSource, variableNameList)
        if len(data) == 0:
            return
        
        support = float(minimumOccurrenceCountThreshold) / len(data)

        print("%s association" % datetime.datetime.now())
        resultList = self._induce(data, variableNameList, support)
        for result in resultList:
            print(result)
        
#        ruleIterable = orange.AssociationRulesInducer(data, support = support, classification_rules = True)
#        
#        orngAssoc.sort(ruleIterable, ['support', 'n_left'])
#        
##        ruleIterableList = []
##        ruleIterableList.append(ruleIterable.filter(lambda rule: rule.n_left != len(variableNameList)))
##        ruleIterableList.append(ruleIterable.filter(lambda rule: rule.n_left == len(variableNameList)))
#                
#        for rule in ruleIterable:
#            dataSet = set()
#            for item in self._matchingData(data, rule):
#                significantVariableNameList = filter(lambda v: v not in self._ruleToAttributeNameList(data.domain, rule),
#                                                     variableNameList)
#                dataSet.add(tuple([(variableName, item[variableName].value) for variableName in significantVariableNameList]))
#
#            data = self._nonMatchingData(data, rule)
#
#            if len(dataSet) > 0:
#                print("%d: %s" % (len(dataSet), self._ruleToAttributeDict(data.domain, rule)))
#                for item in dataSet:
#                    print(dict(item))

    def _induce(self, data, variableNameList, support = 0):
        resultList = []
        
        ruleIterable = orange.AssociationRulesInducer(data, support = support, classification_rules = True)
        orngAssoc.sort(ruleIterable, ['support', 'n_left'])
        
        for rule in ruleIterable:
            subsetVariableNameList = filter(lambda v: v not in self._ruleToAttributeNameList(data.domain, rule), variableNameList)
            childrenResultList = []
            if len(subsetVariableNameList) > 0:
                childrenResultList = self._induce(self._matchingData(data, rule), subsetVariableNameList)

            result = Result(attributeDict = self._ruleToAttributeDict(data.domain, rule),
                            childrenResultList = childrenResultList)
            resultList.append(result)
            
            data = self._nonMatchingData(data, rule)
        return resultList

    def _ruleToAttributeDict(self, domain, rule):
        attributeDict = {}
        for attribute in domain:
            attributeName = attribute.name
            attributeValue = rule.left[attribute].value
            if attributeValue != self._EMPTY_ATTRIBUTE_VALUE:
                attributeDict[attributeName] = attributeValue
        return attributeDict

    def _ruleToAttributeNameList(self, domain, rule):
        return list(self._ruleToAttributeDict(domain, rule).keys())
    
    def _ruleToAttributeSet(self, domain, rule):
        attributeDict = self._ruleToAttributeDict(domain, rule)
        return set([(k, v) for k, v in attributeDict.items()])

    def _matchingData(self, data, rule):
        return self._filterData(data, rule)
    
    def _nonMatchingData(self, data, rule):
        return self._filterData(data, rule, True)
    
    def _filterData(self, data, rule, negate = False):
        attributeDict = self._ruleToAttributeDict(data.domain, rule)
        return data.filter_ref(attributeDict, negate = negate)
