#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from modsecurity_exception_factory.modsecurity_audit_data_source.modsecurity_audit_data_source_sql import \
    ModsecurityAuditDataSourceSQL
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_parser import \
    ModsecurityAuditLogParser
from tests.common import cleanUp, MODSECURITY_AUDIT_LOG_SAMPLE_PATH, MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL, \
    MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH
import io
import sqlite3
import unittest

class TestModsecurityAuditDataSourceSQL(unittest.TestCase):

    _VARIABLE_NAME_LIST = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']

    def setUp(self):
        cleanUp()
        self._stream = io.open(MODSECURITY_AUDIT_LOG_SAMPLE_PATH, 'rt')
        self._fillUpDataSource()
        
        self._dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        self._itemDictIterableOriginal = self._dataSource.itemDictIterable(self._VARIABLE_NAME_LIST)
    
    def tearDown(self):
        self._stream.close()
        cleanUp()

    def testInsertModsecurityAuditEntryIterable(self):
        cursor = sqlite3.connect(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH).cursor()
        self.assertEqual(722, cursor.execute(u"SELECT count(*) FROM messages").fetchone()[0])
        self.assertEqual((1, None, u'/agilefant/login.jsp', u'ARGS:a', u'111111'),
                         cursor.execute(u"SELECT * FROM messages LIMIT 0, 1").fetchone())
        self.assertEqual((8,
                          u"test.domain.com",
                          u"/agilefant/login.jsp",
                          u"ARGS:a",
                          u"111111"),
                         cursor.execute(u"SELECT * FROM messages LIMIT 7, 1").fetchone())

    def testModsecurityEntryMessageIterable(self):
        self.assertEqual(722, len(self._itemDictIterableOriginal))
        
        # Checking some items values.
        itemDictList = list(self._itemDictIterableOriginal)
        message = itemDictList[67]
        self.assertEqual(u"1.1.1.1", message['hostName'])
        self.assertEqual(u"/agilefant/static/js/jquery.jstree.js", message['requestFileName'])
        self.assertEqual(u"TX:anomaly_score", message['payloadContainer'])
        self.assertEqual(u"981174", message['ruleId'])
        message = itemDictList[99]
        self.assertEqual(u"1.1.1.1", message['hostName'])
        self.assertEqual(u"/agilefant/static/js/dynamics/controller/MenuController.js", message['requestFileName'])
        self.assertEqual(u"REQUEST_HEADERS:Host", message['payloadContainer'])
        self.assertEqual(u"960017", message['ruleId'])

    def testModsecurityEntryMessageIterableDistinct(self):
        itemDictDistinctIterable = self._itemDictIterableOriginal.distinct()

        self.assertEqual(544, len(itemDictDistinctIterable))
        self.assertEqual(722, len(self._itemDictIterableOriginal))
        
        # Checking some item values.
        itemDictDistinctList = list(itemDictDistinctIterable)
        message = itemDictDistinctList[67]
        self.assertEqual(u"1.1.1.1", message['hostName'])
        self.assertEqual(u"/agilefant/static/js/jquery.autoSuggest.minified.js", message['requestFileName'])
        self.assertEqual(u"TX:anomaly_score", message['payloadContainer'])
        self.assertEqual(u"981174", message['ruleId'])
        message = itemDictDistinctList[99]
        self.assertEqual(u"1.1.1.1", message['hostName'])
        self.assertEqual(u"/agilefant/static/js/utils/ArrayUtils.js", message['requestFileName'])
        self.assertEqual(u"REQUEST_HEADERS:Host", message['payloadContainer'])
        self.assertEqual(u"960017", message['ruleId'])

    def testMostFrequentAttribute(self):
        self.assertEqual({'hostName': u'1.1.1.1'},
                         self._itemDictIterableOriginal.mostFrequentVariableAndValue(['hostName', 'requestFileName', 'payloadContainer', 'ruleId']))

        self.assertEqual({'ruleId': u'960017'},
                         self._itemDictIterableOriginal.mostFrequentVariableAndValue(['ruleId']))

    def testFilterByVariable(self):
        # Filtering by request file name.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('hostName',
                                                                           u"test.domain.com")
        self.assertEqual(59, len(itemDictIterable))

    def testFilterByVariableMultiple(self):
        # Multiple filters.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('hostName',
                                                                           u"test.domain.com")
        itemDictIterable = itemDictIterable.filterByVariable('ruleId',
                                                             u"960017")
        self.assertEqual(18, len(itemDictIterable))
        
    def testFilterByVariableReverse(self):
        # Reverse filtering by host name and rule id.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('hostName',
                                                                           u"test.domain.com")
        itemDictIterable = itemDictIterable.filterByVariable('requestFileName',
                                                             u"/agilefant/static/js/jquery.hotkeys.js",
                                                             negate = True)
        self.assertEqual(56, len(itemDictIterable))

    def testFilterByVariableReverseMultiple(self):
        # Reverse filtering by host name and rule id.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('hostName',
                                                                           u"test.domain.com")
        itemDictIterable = itemDictIterable.filterByVariable('requestFileName',
                                                             u"/agilefant/static/js/jquery.hotkeys.js",
                                                             negate = True)
        itemDictIterable = itemDictIterable.filterByVariable('requestFileName',
                                                             u"/agilefant/static/js/backlogSelector.js",
                                                             negate = True)
        itemDictIterable = itemDictIterable.filterByVariable('ruleId',
                                                             u"981203",
                                                             negate = True)
        self.assertEqual(36, len(itemDictIterable))

    def testDistinctWithFilter(self):
        # Testing that 'distinct' works with filters.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('hostName',
                                                                           u"test.domain.com")
        itemDictIterable = itemDictIterable.filterByVariable('requestFileName',
                                                             u"/agilefant/static/js/jquery.hotkeys.js",
                                                             negate = True)
        itemDictIterable = itemDictIterable.filterByVariable('requestFileName',
                                                             u"/agilefant/static/js/backlogSelector.js",
                                                             negate = True)
        itemDictIterable = itemDictIterable.filterByVariable('ruleId',
                                                             u"981203",
                                                             negate = True)
        itemDictIterableDistinct = itemDictIterable.distinct()
        self.assertEqual(32, len(itemDictIterableDistinct))

        # Checking that the original iterable has not been modified.
        self.assertEqual(36, len(itemDictIterable))
        
        # Checking that other methods work with filters.
        self.assertEqual({'hostName': u'test.domain.com'},
                         itemDictIterable.mostFrequentVariableAndValue(self._VARIABLE_NAME_LIST))
        # Testing iterator.
        self.assertEqual(36, len(list(itemDictIterable)))

    def testFilterByVariableMany(self):
        itemDictIterable = self._itemDictIterableOriginal

        for i in range(1000):
            itemDictIterable = itemDictIterable.filterByVariable('hostName',
                                                                 unicode(i),
                                                                 negate = True)
        self.assertEqual(715, len(itemDictIterable))

    def _fillUpDataSource(self):
        iterable = ModsecurityAuditLogParser().parseStream(self._stream)
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        dataSource.insertModsecurityAuditEntryIterable(iterable)
