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

class ConfigurationError(Exception):
    pass

class ItemNotFoundError(ConfigurationError):
    
    def __init__(self, key):
        super(ConfigurationError, self).__init__(u"Item '%s' not found." % key)

class Config:

    _KEY_IGNORE_FILTER_LIST = 'ignore'
    _KEY_VARIABLE_NAME_LIST = 'variables'
    _KEY_MINIMUM_OCCURRENCE_COUNT_THRESHOLD = 'minimum_occurrence_count_threshold'
    _KEY_MAXIMUM_VALUE_COUNT_THRESHOLD = 'maximum_value_count_threshold'

    @contract
    def __init__(self, configFilePath = None):
        """
    :type configFilePath: unicode|None
"""
        self._configFilePath = configFilePath
        self._configDict = None
        self._configDefaultDict = {self._KEY_IGNORE_FILTER_LIST: {},
                                   self._KEY_VARIABLE_NAME_LIST: ['hostName',
                                                                  'requestFileName',
                                                                  'payloadContainer',
                                                                  'ruleId'],
                                   self._KEY_MINIMUM_OCCURRENCE_COUNT_THRESHOLD: 0,
                                   self._KEY_MAXIMUM_VALUE_COUNT_THRESHOLD: None}

    def ignoredVariableDict(self):
        """
    :returns A dict of items to ignore. Each key is a variable name and each value is a list of values to ignore. 
"""
        ignoredVariableDict = {}
        for name, valueList in self._loadConfigDict()[self._KEY_IGNORE_FILTER_LIST].items():
            ignoredVariableDict[name] = [unicode(value) for value in valueList]
        return ignoredVariableDict

    def variableNameList(self):
        return self._loadConfigDict()[self._KEY_VARIABLE_NAME_LIST]

    def minimumOccurrenceCountThreshold(self):
        return self._loadConfigDict()[self._KEY_MINIMUM_OCCURRENCE_COUNT_THRESHOLD]

    def maximumValueCountThreshold(self):
        return self._loadConfigDict()[self._KEY_MAXIMUM_VALUE_COUNT_THRESHOLD]

    def _loadConfigDict(self):
        if self._configDict is not None:
            return self._configDict
        
        # Default config.
        configDict = self._configDefaultDict.copy()
        
        # Try to load the configuration.        
        if self._configFilePath is not None:
            configFileDict = yaml.load(io.open(self._configFilePath, 'rt', errors = 'replace'))
            if configFileDict is not None:
                configDict.update(configFileDict)

        self._configDict = configDict
        return self._configDict
