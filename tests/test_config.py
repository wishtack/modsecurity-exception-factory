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

    _TEST_CONFIG_OK = testFilePath(u"data/test.yaml")
    _TEST_CONFIG_EMPTY = testFilePath(u"data/empty.yaml")

    def testIgnoredVariableDict(self):
        config = Config(self._TEST_CONFIG_OK)
        self.assertEqual({'ruleId': [u"111111", u"222222", u"333333"],
                          'hostName': [u"1.1.1.1"]}, config.ingoredVariableDict())

    def testIgnoredVariableDictEmpty(self):
        config = Config(self._TEST_CONFIG_EMPTY)
        self.assertEqual({}, config.ingoredVariableDict())
