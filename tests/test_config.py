#-*- coding: utf-8 -*-
#
# Created on Feb 5, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .common import makeTestFilePath
from modsecurity_exception_factory.utils import Config
import unittest

class TestConfig(unittest.TestCase):

    _TEST_CONFIG_OK = makeTestFilePath(u"data/test_config_ok.yaml")
    _TEST_CONFIG_EMPTY = makeTestFilePath(u"data/test_config_empty.yaml")

    def testOK(self):
        config = Config(self._TEST_CONFIG_OK)
        self.assertEqual({'rule_id': [u"111111", u"222222", u"333333"],
                          'host_name': [u"1.1.1.1"]}, config.ignoredVariableDict())
        self.assertEqual(['aaa', 'bbb', 'ccc'],
                         config.variableNameList())
        self.assertEqual(10, config.minimumOccurrenceCountThreshold())
        self.assertEqual(20, config.maximumValueCountThreshold())

    def testEmpty(self):
        config = Config(self._TEST_CONFIG_EMPTY)
        self.assertEqual({}, config.ignoredVariableDict())
        self.assertEqual(['host_name', 'request_file_name', 'payload_container', 'rule_id'],
                         config.variableNameList())
        self.assertEqual(0, config.minimumOccurrenceCountThreshold())
        self.assertEqual(None, config.maximumValueCountThreshold())

    def testDefault(self):
        config = Config()
        self.assertEqual({}, config.ignoredVariableDict())
        self.assertEqual(['host_name', 'request_file_name', 'payload_container', 'rule_id'],
                         config.variableNameList())
        self.assertEqual(0, config.minimumOccurrenceCountThreshold())
        self.assertEqual(None, config.maximumValueCountThreshold())
