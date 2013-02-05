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

    @contract
    def __init__(self, configFilePath):
        """
    :type configFilePath: unicode
"""
        self._configFilePath = configFilePath
        self._configDict = None

    def ingoredVariableDict(self):
        """
    :returns A dict of items to ignore. Each key is a variable name and each value is a list of values to ignore. 
"""
        configDict = self._loadConfigDict()        
        ignoredVariableDict = {}
        for name, valueList in configDict.get(self._KEY_IGNORE_FILTER_LIST, {}).items():
            ignoredVariableDict[name] = [unicode(value) for value in valueList]
        return ignoredVariableDict

    def _loadConfigDict(self):
        # Try to load the configuration.
        if self._configDict is None:
            self._configDict = yaml.load(io.open(self._configFilePath, 'rt', errors = 'replace'))

        # File is empty.        
        if self._configDict is None:
            self._configDict = {}
        return self._configDict