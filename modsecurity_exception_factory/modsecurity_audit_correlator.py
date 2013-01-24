#-*- coding: utf-8 -*-
#
# Created on Jan 9, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from modsecurity_exception_factory.correlation.correlation_engine import CorrelationEngine

class ModsecurityAuditCorrelator:
    
    def correlate(self, dataSource, minimumOccurrenceCountThreshold = 0):
        """Yields correlations as dict objects.
The dict keys are variables' names and the values are set objects containing variables' values. 
    :type dataSource: IModsecurityAuditDataSource
    :type minimumOccurrenceCountThreshold: int
"""
        variableNameList = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']
        
        for correlationDict in CorrelationEngine(variableNameList).correlate(dataSource,
                                                                             minimumOccurrenceCountThreshold):
            yield correlationDict
