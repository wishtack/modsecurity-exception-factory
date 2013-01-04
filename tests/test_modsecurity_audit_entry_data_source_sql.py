#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#
from modsecurity_exception_factory.modsecurity_audit_entry_data_source.modsecurity_audit_entry_data_source_sql import \
    ModsecurityAuditEntryDataSourceSQL
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_parser import \
    ModsecurityAuditLogParser
from tests.data import MODSECURITY_AUDIT_LOG_SAMPLE_PATH, MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL, \
    MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH
import io
import os
import sqlite3
import unittest

class TestModsecurityAuditEntryDataSourceSQL(unittest.TestCase):

    def setUp(self):
        self._stream = io.open(MODSECURITY_AUDIT_LOG_SAMPLE_PATH, 'rt')
        self._cleanUp()
    
    def tearDown(self):
        self._stream.close()
        self._cleanUp()

    def testInsertModsecurityAuditEntryIterable(self):
        iterable = ModsecurityAuditLogParser().parseStream(self._stream)
        dataSource = ModsecurityAuditEntryDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        dataSource.insertModsecurityAuditEntryIterable(iterable)
        
        cursor = sqlite3.connect(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH).cursor()
        self.assertEqual(711, cursor.execute(u"SELECT count(*) FROM messages").fetchone()[0])
        self.assertEqual((1,
                          u"test.domain.com",
                          u"/agilefant/login.jsp",
                          u"REQUEST_HEADERS:Host",
                          u"960017"),
                         cursor.execute(u"SELECT * FROM messages LIMIT 1").fetchone())

    def _cleanUp(self):
        if os.path.exists(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH):
            os.remove(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH)
