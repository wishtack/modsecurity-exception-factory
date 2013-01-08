#-*- coding: utf-8 -*-
#
# Created on Jan 8, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import new_contract, contract
from modsecurity_exception_factory.modsecurity_audit_data_source.i_modsecurity_audit_data_source import \
    IModsecurityAuditDataSource
import Orange.data
import Orange.feature
import itertools

new_contract('IModsecurityAuditDataSource', IModsecurityAuditDataSource)

class OrangeDataTableFactory:
    
    _VARIABLE_FALSE_POSITIVE_NAME = 'falsePositive'
    _VARIABLE_FALSE_POSITIVE_TRUE = u"True"

    @contract
    def data(self, dataSource, variableNameList):
        """Makes data table for Orange data-mining library.
    :type dataSource: IModsecurityAuditDataSource
    :type variableNameList: list(str)
"""
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
        
        reader = dataSource.orangeDataReader()
        reader.execute(u"SELECT %(variables)s, '%(falsePositiveValue)s' AS %(falsePositiveColumnName)s FROM messages" %
                       {'variables': u", ".join(variableNameList),
                        'falsePositiveValue': self._VARIABLE_FALSE_POSITIVE_TRUE,
                        'falsePositiveColumnName': self._VARIABLE_FALSE_POSITIVE_NAME},
                       domain = domain)

        return reader.data()

    @contract
    def _makeDiscreteVariable(self, dataSource, variableName, additionalValueList = []):
        """
    :type dataSource: IModsecurityAuditDataSource
    :type variableName: str
    :type additionalValueList: list(unicode)
"""
        # Creating data source.
        variable = Orange.feature.Discrete(variableName)
        for value in itertools.chain(dataSource.variableValueIterable(variableName), additionalValueList):
            if value is None:
                continue
            variable.add_value(value.encode('utf-8'))
        return variable
