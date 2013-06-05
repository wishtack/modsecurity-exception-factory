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

    _VARIABLE_NAME_LIST = ['host_name', 'request_file_name', 'payload_container', 'rule_id']

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
        self.assertEqual(723, cursor.execute(u"SELECT count(*) FROM messages").fetchone()[0])
        self.assertEqual((5, None, u'/agilefant/login.jsp', u'ARGS:a', u'111111'),
                         cursor.execute(u"SELECT * FROM messages LIMIT 4, 1").fetchone())
        self.assertEqual((9,
                          u"test.domain.com",
                          u"/agilefant/login.jsp",
                          u"ARGS:a",
                          u"111111"),
                         cursor.execute(u"SELECT * FROM messages LIMIT 8, 1").fetchone())

    def testModsecurityEntryMessageIterable(self):
        self.assertEqual(723, len(self._itemDictIterableOriginal))
        
        # Checking some items values.
        itemDictList = list(self._itemDictIterableOriginal)
        message = itemDictList[4]
        self.assertEqual(None, message['host_name'])
        self.assertEqual(u"/agilefant/login.jsp", message['request_file_name'])
        self.assertEqual(u"ARGS:a", message['payload_container'])
        self.assertEqual(u"111111", message['rule_id'])
        message = itemDictList[68]
        self.assertEqual(u"1.1.1.1", message['host_name'])
        self.assertEqual(u"/agilefant/static/js/jquery.jstree.js", message['request_file_name'])
        self.assertEqual(u"TX:anomaly_score", message['payload_container'])
        self.assertEqual(u"981174", message['rule_id'])
        message = itemDictList[100]
        self.assertEqual(u"1.1.1.1", message['host_name'])
        self.assertEqual(u"/agilefant/static/js/dynamics/controller/MenuController.js", message['request_file_name'])
        self.assertEqual(u"REQUEST_HEADERS:Host", message['payload_container'])
        self.assertEqual(u"960017", message['rule_id'])

    def testModsecurityEntryMessageIterableDistinct(self):
        itemDictDistinctIterable = self._itemDictIterableOriginal.distinct()

        self.assertEqual(545, len(itemDictDistinctIterable))
        self.assertEqual(723, len(self._itemDictIterableOriginal))
        
        # Checking some item values.
        itemDictDistinctList = list(itemDictDistinctIterable)
        message = itemDictDistinctList[4]
        self.assertEqual(None, message['host_name'])
        self.assertEqual(u"/agilefant/login.jsp", message['request_file_name'])
        self.assertEqual(u"ARGS:a", message['payload_container'])
        self.assertEqual(u"111111", message['rule_id'])
        message = itemDictDistinctList[68]
        self.assertEqual(u"1.1.1.1", message['host_name'])
        self.assertEqual(u"/agilefant/static/js/jquery.autoSuggest.minified.js", message['request_file_name'])
        self.assertEqual(u"TX:anomaly_score", message['payload_container'])
        self.assertEqual(u"981174", message['rule_id'])
        message = itemDictDistinctList[100]
        self.assertEqual(u"1.1.1.1", message['host_name'])
        self.assertEqual(u"/agilefant/static/js/utils/ArrayUtils.js", message['request_file_name'])
        self.assertEqual(u"REQUEST_HEADERS:Host", message['payload_container'])
        self.assertEqual(u"960017", message['rule_id'])

    def testMostFrequentAttribute(self):
        self.assertEqual({'host_name': u'1.1.1.1'},
                         self._itemDictIterableOriginal.mostFrequentVariableAndValue(['host_name', 'request_file_name', 'payload_container', 'rule_id']))

        self.assertEqual({'rule_id': u'960017'},
                         self._itemDictIterableOriginal.mostFrequentVariableAndValue(['rule_id']))

    def testFilterByVariable(self):
        # Filtering by request file name.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('host_name',
                                                                           u"test.domain.com")
        self.assertEqual(59, len(itemDictIterable))

    def testFilterByVariableMultiple(self):
        # Multiple filters.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('host_name',
                                                                           u"test.domain.com")
        itemDictIterable = itemDictIterable.filterByVariable('rule_id',
                                                             u"960017")
        self.assertEqual(18, len(itemDictIterable))
        
    def testFilterByVariableReverse(self):
        # Reverse filtering by host name and rule id.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('host_name',
                                                                           u"test.domain.com")
        itemDictIterable = itemDictIterable.filterByVariable('request_file_name',
                                                             u"/agilefant/static/js/jquery.hotkeys.js",
                                                             negate = True)
        self.assertEqual(56, len(itemDictIterable))

    def testFilterByVariableReverseMultiple(self):
        # Reverse filtering by host name and rule id.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('host_name',
                                                                           u"test.domain.com")
        itemDictIterable = itemDictIterable.filterByVariable('request_file_name',
                                                             u"/agilefant/static/js/jquery.hotkeys.js",
                                                             negate = True)
        itemDictIterable = itemDictIterable.filterByVariable('request_file_name',
                                                             u"/agilefant/static/js/backlogSelector.js",
                                                             negate = True)
        itemDictIterable = itemDictIterable.filterByVariable('rule_id',
                                                             u"981203",
                                                             negate = True)
        self.assertEqual(36, len(itemDictIterable))

    def testFilterByVariableNull(self):
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('host_name', None)
        self.assertEqual(8, len(itemDictIterable))

    def testFilterByVariableReverseNull(self):
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('host_name', None, negate = True)
        self.assertEqual(715, len(itemDictIterable))

    def testDistinctWithFilter(self):
        # Testing that 'distinct' works with filters.
        itemDictIterable = self._itemDictIterableOriginal.filterByVariable('host_name',
                                                                           u"test.domain.com")
        itemDictIterable = itemDictIterable.filterByVariable('request_file_name',
                                                             u"/agilefant/static/js/jquery.hotkeys.js",
                                                             negate = True)
        itemDictIterable = itemDictIterable.filterByVariable('request_file_name',
                                                             u"/agilefant/static/js/backlogSelector.js",
                                                             negate = True)
        itemDictIterable = itemDictIterable.filterByVariable('rule_id',
                                                             u"981203",
                                                             negate = True)
        itemDictIterableDistinct = itemDictIterable.distinct()
        self.assertEqual(32, len(itemDictIterableDistinct))

        # Checking that the original iterable has not been modified.
        self.assertEqual(36, len(itemDictIterable))
        
        # Checking that other methods work with filters.
        self.assertEqual({'host_name': u'test.domain.com'},
                         itemDictIterable.mostFrequentVariableAndValue(self._VARIABLE_NAME_LIST))
        # Testing iterator.
        self.assertEqual(36, len(list(itemDictIterable)))

    def testFilterByVariableMany(self):
        itemDictIterable = self._itemDictIterableOriginal

        for i in range(1000):
            itemDictIterable = itemDictIterable.filterByVariable('host_name',
                                                                 unicode(i),
                                                                 negate = True)
        self.assertEqual(723, len(itemDictIterable))

    def _fillUpDataSource(self):
        iterable = ModsecurityAuditLogParser().parseStream(self._stream)
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        dataSource.insertModsecurityAuditEntryIterable(iterable)
