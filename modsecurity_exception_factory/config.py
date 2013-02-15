#-*- coding: utf-8 -*-
#
# Created on Feb 5, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract
import io
import yaml

class Config:

    _KEY_IGNORE_FILTER_LIST = 'ignore'
    _KEY_VARIABLE_NAME_LIST = 'variables'
    
    _DEFAULT_IGNORED_VARIABLE_DICT = {}
    _DEFAULT_VARIABLE_NAME_LIST = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']

    @contract
    def __init__(self, configFilePath = None):
        """
    :type configFilePath: unicode|None
"""
        self._configFilePath = configFilePath
        self._configDict = None

    def ignoredVariableDict(self):
        """
    :returns A dict of items to ignore. Each key is a variable name and each value is a list of values to ignore. 
"""
        configDict = self._loadConfigDict()        
        ignoredVariableDict = {}
        for name, valueList in configDict.get(self._KEY_IGNORE_FILTER_LIST, self._DEFAULT_IGNORED_VARIABLE_DICT).items():
            ignoredVariableDict[name] = [unicode(value) for value in valueList]
        return ignoredVariableDict

    def variableNameList(self):
        return self._loadConfigDict().get(self._KEY_VARIABLE_NAME_LIST, self._DEFAULT_VARIABLE_NAME_LIST)

    def _loadConfigDict(self):
        # Try to load the configuration.
        if self._configDict is None and self._configFilePath is not None:
            self._configDict = yaml.load(io.open(self._configFilePath, 'rt', errors = 'replace'))

        # File is empty.        
        if self._configDict is None:
            self._configDict = {}
        return self._configDict
