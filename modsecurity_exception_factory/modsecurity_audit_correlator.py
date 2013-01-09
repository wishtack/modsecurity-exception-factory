#-*- coding: utf-8 -*-
#
# Created on Jan 9, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from modsecurity_exception_factory.modsecurity_audit_data_source.modsecurity_audit_orange_data_table_factory import \
    ModsecurityAuditOrangeDataTableFactory
from modsecurity_exception_factory.orange_correlation_engine import OrangeCorrelationEngine

class ModsecurityAuditCorrelator:
    
    def correlate(self, dataSource, minimumOccurrenceCountThreshold = 0):
        """Yields correlations as dict objects.
The dict keys are variables' names and the values are set objects containing variables' values. 
    :type dataSource: IModsecurityAuditDataSource
    :type minimumOccurrenceCountThreshold: int
"""
        variableNameList = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']
        
        dataFactory = ModsecurityAuditOrangeDataTableFactory()
        data = dataFactory.entryMessageData(dataSource, variableNameList)
        
        for correlationDict in OrangeCorrelationEngine(variableNameList).correlate(data,
                                                                                   minimumOccurrenceCountThreshold):
            yield correlationDict
