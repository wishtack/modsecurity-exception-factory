#-*- coding: utf-8 -*-
#
# Created on Jan 9, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .correlation import CorrelationEngine

class ModsecurityAuditCorrelator:
    
    def correlate(self, dataSource, ignoredVariableDict = {}, minimumOccurrenceCountThreshold = 0):
        """Yields correlations as dict objects.
The dict keys are variables' names and the values are set objects containing variables' values. 
    :type dataSource: IModsecurityAuditDataSource
    :type ignoredVariableDict: dict(str:list(unicode))
    :type minimumOccurrenceCountThreshold: int
"""
        variableNameList = ['requestFileName', 'payloadContainer', 'ruleId']
        
        for correlationDict in CorrelationEngine(variableNameList, ignoredVariableDict).correlate(dataSource,
                                                                                                  minimumOccurrenceCountThreshold):
            yield correlationDict
