#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
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

    def setUp(self):
        self._stream = io.open(MODSECURITY_AUDIT_LOG_SAMPLE_PATH, 'rt')
        cleanUp()
        self._fillUpDataSource()
    
    def tearDown(self):
        self._stream.close()
        cleanUp()

    def testInsertModsecurityAuditEntryIterable(self):
        cursor = sqlite3.connect(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH).cursor()
        self.assertEqual(715, cursor.execute(u"SELECT count(*) FROM messages").fetchone()[0])
        self.assertEqual((1,
                          u"test.domain.com",
                          u"/agilefant/login.jsp",
                          u"ARGS:a",
                          u"111111"),
                         cursor.execute(u"SELECT * FROM messages LIMIT 1").fetchone())

    def testModsecurityEntryMessageIterable(self):
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        itemDictIterable = dataSource.itemDictIterable(['hostName', 'requestFileName', 'payloadContainer', 'ruleId'])

        self.assertEqual(715, len(itemDictIterable))
        
        # Checking some items values.
        itemDictList = list(itemDictIterable)
        message = itemDictList[67]
        self.assertEqual(u"1.1.1.1", message['hostName'])
        self.assertEqual(u"/agilefant/static/js/jquery.autoSuggest.minified.js", message['requestFileName'])
        self.assertEqual(u"TX:inbound_anomaly_score", message['payloadContainer'])
        self.assertEqual(u"981203", message['ruleId'])
        message = itemDictList[99]
        self.assertEqual(u"1.1.1.1", message['hostName'])
        self.assertEqual(u"/agilefant/static/js/utils/ArrayUtils.js", message['requestFileName'])
        self.assertEqual(u"TX:anomaly_score", message['payloadContainer'])
        self.assertEqual(u"981174", message['ruleId'])

    def testModsecurityEntryMessageIterableDistinct(self):
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        itemDictIterable = dataSource.itemDictIterable(['hostName', 'requestFileName', 'payloadContainer', 'ruleId'])

        itemDictDistinctIterable = itemDictIterable.distinct()

        self.assertEqual(537, len(itemDictDistinctIterable))
        self.assertEqual(715, len(itemDictIterable))
        
        # Checking some item values.
        itemDictDistinctList = list(itemDictDistinctIterable)
        message = itemDictDistinctList[67]
        self.assertEqual(u"1.1.1.1", message['hostName'])
        self.assertEqual(u"/agilefant/static/js/jquery.tagcloud.min.js", message['requestFileName'])
        self.assertEqual(u"TX:inbound_anomaly_score", message['payloadContainer'])
        self.assertEqual(u"981203", message['ruleId'])
        message = itemDictDistinctList[99]
        self.assertEqual(u"1.1.1.1", message['hostName'])
        self.assertEqual(u"/agilefant/static/js/utils/Parsers.js", message['requestFileName'])
        self.assertEqual(u"TX:anomaly_score", message['payloadContainer'])
        self.assertEqual(u"981174", message['ruleId'])

    def testMostFrequentAttribute(self):
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        itemDictIterable = dataSource.itemDictIterable(['hostName', 'requestFileName', 'payloadContainer', 'ruleId'])


        self.assertEqual({'hostName': u'1.1.1.1'},
                         itemDictIterable.mostFrequentVariableAndValue(['hostName', 'requestFileName', 'payloadContainer', 'ruleId']))

        self.assertEqual({'ruleId': u'960017'},
                         itemDictIterable.mostFrequentVariableAndValue(['ruleId']))

    def testFilterByVariable(self):
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        variableNameList = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']
        itemDictIterableOriginal = dataSource.itemDictIterable(variableNameList)
        
        # Filtering by request file name.

        itemDictIterable = itemDictIterableOriginal.filterByVariable('hostName',
                                                                     u"test.domain.com")
        
        self.assertEqual(59, len(itemDictIterable))
        
        # Reverse filtering by host name and rule id.
        itemDictIterable = itemDictIterable.filterByVariable('requestFileName',
                                                             u"/agilefant/static/js/jquery.hotkeys.js",
                                                             negate = True)

        self.assertEqual(56, len(itemDictIterable))
        
        # Testing that 'distinct' works with filters.
        itemDictIterable = itemDictIterable.distinct()
        self.assertEqual(50, len(itemDictIterable))

        # Checking that the original iterable has not been modified.
        self.assertEqual(715, len(itemDictIterableOriginal))
        
        # Checking that other methods work with filters.
        self.assertEqual({'hostName': u'test.domain.com'},
                         itemDictIterable.mostFrequentVariableAndValue(variableNameList))
        # Testing iterator.
        self.assertEqual(50, len(list(itemDictIterable)))

    def testFilterByVariableMany(self):
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        variableNameList = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']
        itemDictIterable = dataSource.itemDictIterable(variableNameList)

        for i in range(10000):
            itemDictIterable = itemDictIterable.filterByVariable('hostName',
                                                                 unicode(i),
                                                                 negate = True)
        self.assertEqual(59, len(itemDictIterable))

    def _fillUpDataSource(self):
        iterable = ModsecurityAuditLogParser().parseStream(self._stream)
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        dataSource.insertModsecurityAuditEntryIterable(iterable)
