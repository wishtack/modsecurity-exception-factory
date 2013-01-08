#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from modsecurity_exception_factory.modsecurity_audit_correlation_engine import ModsecurityAuditCorrelationEngine
from modsecurity_exception_factory.modsecurity_audit_data_source.modsecurity_audit_data_source_sql import \
    ModsecurityAuditDataSourceSQL
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_parser import \
    ModsecurityAuditLogParser
from tests.common import MODSECURITY_AUDIT_LOG_SAMPLE_PATH, cleanUp, MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL
import datetime
import io
import unittest

class TestModsecurityAuditCorrelationEngine(unittest.TestCase):

    def setUp(self):
        self._stream = io.open("data/modsec_audit.log", 'rt', errors = 'replace')
        cleanUp()
    
    def tearDown(self):
        self._stream.close()
        cleanUp()

    def testCorrelate(self):
        # Fillup database.
        iterable = ModsecurityAuditLogParser().parseStream(self._stream)
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        print("%s loading data" % datetime.datetime.now())
        
        dataSource.insertModsecurityAuditEntryIterable(iterable)

        ModsecurityAuditCorrelationEngine().correlate(dataSource)
