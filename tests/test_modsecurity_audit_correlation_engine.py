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
from tests.common import MODSECURITY_AUDIT_LOG_SAMPLE_PATH, cleanUp, MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL
import io
import unittest
from modsecurity_exception_factory.modsecurity_audit_correlation_engine import ModsecurityAuditCorrelationEngine

class TestModsecurityAuditCorrelationEngine(unittest.TestCase):

    def setUp(self):
        self._stream = io.open(MODSECURITY_AUDIT_LOG_SAMPLE_PATH, 'rt')
        cleanUp()
    
    def tearDown(self):
        self._stream.close()
#        cleanUp()

    def testCorrelate(self):
        # Fillup database.
        iterable = ModsecurityAuditLogParser().parseStream(self._stream)
        dataSource = ModsecurityAuditEntryDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        dataSource.insertModsecurityAuditEntryIterable(list(iterable)[:10])
        
        ModsecurityAuditCorrelationEngine().correlate(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL, None)
        