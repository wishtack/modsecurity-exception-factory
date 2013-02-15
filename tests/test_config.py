#-*- coding: utf-8 -*-
#
# Created on Feb 5, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .common import testFilePath
from modsecurity_exception_factory.config import Config
import unittest

class TestConfig(unittest.TestCase):

    _TEST_CONFIG_OK = testFilePath(u"data/test_config_ok.yaml")
    _TEST_CONFIG_EMPTY = testFilePath(u"data/test_config_empty.yaml")

    def testOK(self):
        config = Config(self._TEST_CONFIG_OK)
        self.assertEqual({'ruleId': [u"111111", u"222222", u"333333"],
                          'hostName': [u"1.1.1.1"]}, config.ignoredVariableDict())
        self.assertEqual(['aaa', 'bbb', 'ccc'],
                         config.variableNameList())

    def testEmpty(self):
        config = Config(self._TEST_CONFIG_EMPTY)
        self.assertEqual({}, config.ignoredVariableDict())
        self.assertEqual(['hostName', 'requestFileName', 'payloadContainer', 'ruleId'],
                         config.variableNameList())

    def testDefault(self):
        config = Config()
        self.assertEqual({}, config.ignoredVariableDict())
        self.assertEqual(['hostName', 'requestFileName', 'payloadContainer', 'ruleId'],
                         config.variableNameList())
