#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from Orange.data.sql import SQLReader, __PostgresQuirkFix as PostgresQuirkFix
from contracts import contract
from modsecurity_exception_factory.modsecurity_audit_entry_data_source.modsecurity_audit_entry_data_source_sql import \
    ModsecurityAuditEntryDataSourceSQL
from sqlalchemy.engine.url import make_url
import Orange.data
import Orange.feature
import itertools
import orange
import orngAssoc
import sqlite3

class ModsecurityAuditCorrelationEngine:
    
    _VARIABLE_FALSE_POSITIVE_NAME = 'falsePositive'
    _VARIABLE_FALSE_POSITIVE_TRUE = 'True'
    
    @contract
    def correlate(self, dataBaseUrl, modsecurityAuditCorrelationDataSource):
        """
    :type dataBaseUrl: unicode
"""

        variableNameList = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']
        data = self._makeData(dataBaseUrl, variableNameList)
        
        ruleSubsetList = []
        
        for leftAttributeCount in range(len(data.domain), 0, -1):
            support = 0
            if len(data) > 0:
                support = 10.0 / len(data)
            
            rules = orange.AssociationRulesInducer(data, support = support, classification_rules = True)
            rules = rules.filter(lambda rule: rule.n_left == leftAttributeCount)
            ruleSubsetList.append(rules)
            for rule in rules:
                attributeDict = {}
                for attribute in data.domain:
                    attributeName = attribute.name
                    attributeValue = rule.left[attribute].value
                    if attributeValue != '~':
                        attributeDict[attributeName] = attributeValue
                data = data.filter_ref(attributeDict, negate = True)
        
        parameterList = ['n_left', 'support']
        for ruleSubset in ruleSubsetList:
            orngAssoc.sort(ruleSubset, parameterList)
            orngAssoc.printRules(ruleSubset, parameterList)

    def _makeReader(self, dataBaseUrlString):
        reader = SQLReader()
        
        # @hack SQLReader's connect method doesn't parse sqlite urls correctly.
        # It only handle file names instead of pathes (it should concatenate "host" and "path".        
        url = make_url(dataBaseUrlString)
        if url.drivername == u"sqlite":
            reader.conn = sqlite3.connect(url.database)
            reader.quirks = PostgresQuirkFix(sqlite3)
        else:
            reader.connect(dataBaseUrlString)
        
        return reader

    def _makeDiscreteVariable(self, dataSource, variableName, additionalValueList = []):
        """
    :type dataSource: ModsecurityAuditEntryDataSourceSQL
    :type variableName: str
    :type additionalValueList: list(unicode)
"""
        # Creating data source.
        variable = Orange.feature.Discrete(variableName)
        for value in itertools.chain(dataSource.variableValueIterable(variableName), additionalValueList):
            variable.add_value(value.encode('utf-8'))      
        return variable 

    @contract
    def _makeData(self, dataBaseUrl, variableNameList):
        """
    :type dataBaseUrl: unicode
    :type variableNameList: list(str)
"""
        # Creating data source.
        dataSource = ModsecurityAuditEntryDataSourceSQL(dataBaseUrl)
        
        # Making variables out of data source content.
        variableList = []
        for variableName in variableNameList:
            variableList.append(self._makeDiscreteVariable(dataSource, variableName))
            
        # We add the 'falsePositive' variable.
        variableList.append(self._makeDiscreteVariable(dataSource,
                                                       self._VARIABLE_FALSE_POSITIVE_NAME,
                                                       [self._VARIABLE_FALSE_POSITIVE_TRUE]))
        
        # Creating the domain.
        domain = Orange.data.Domain(variableList)
        
        reader = self._makeReader(dataBaseUrl)
        reader.execute(u"SELECT %s, 'True' AS falsePositive FROM messages" % u", ".join(variableNameList),
                       domain = domain)
        
        return reader.data()
