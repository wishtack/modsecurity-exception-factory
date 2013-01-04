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
from sqlalchemy.engine.url import make_url
import Orange.data
import Orange.feature
import orange
import orngAssoc
import sqlite3

class ModsecurityAuditCorrelationEngine:

    
    @contract
    def correlate(self, dataBaseUrl, modsecurityAuditCorrelationDataSource):
        """
    :type dataBaseUrl: unicode
"""

        variableNameList = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId', 'falsePositive']
        variableList = [Orange.feature.Discrete(variableName) for variableName in variableNameList]
        domain = Orange.data.Domain(variableList,
                       class_var = 'falsePositive')

        reader = self._makeReader(dataBaseUrl)
        reader.execute(u"SELECT hostName, requestFileName, payloadContainer, ruleId, 'True' AS falsePositive FROM messages",
                       domain = domain)
        
        data = reader.data()
        
        ruleSubsetList = []
        
        for leftAttributeCount in range(len(data.domain),0,-1):
            support = 0
            if len(data) > 0:
                support = 27.0 / len(data)
            
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
