#-*- coding: utf-8 -*-
#
# Created on Jan 2, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from modsecurity_exception_factory.modsecurity_audit_log_parser import ModsecurityAuditLogParser
from tests.common import MODSECURITY_AUDIT_LOG_SAMPLE_PATH
import io
import unittest

class TestModsecurityAuditLogParser(unittest.TestCase):

    def setUp(self):
        self._stream = io.open(MODSECURITY_AUDIT_LOG_SAMPLE_PATH, 'rt')
    
    def tearDown(self):
        self._stream.close()

    def testModsecurityAuditLogParser(self):
        parser = ModsecurityAuditLogParser()
        
        # Make a list out of generator.
        entryList = list(parser.parseStream(self._stream))
        
        # Checking entries count.
        self.assertEqual(238, len(entryList))
        
        # Checking host name.
        self.assertEqual(18, self._filterEntryListAndCountByPredicate(entryList, 'host_name', u"test.domain.com"))
        self.assertEqual(218, self._filterEntryListAndCountByPredicate(entryList, 'host_name', u"1.1.1.1"))
        self.assertEqual(2, self._filterEntryListAndCountByPredicate(entryList, 'host_name', None))

        # Checking inbound anomaly score.
        self.assertEqual(3, self._filterEntryListAndCountByPredicate(entryList,
                                                                     'request_file_name',
                                                                     u"/agilefant/ajax/iterationData.action"))
        
        self.assertEqual(3, self._filterEntryListAndCountByPredicate(entryList,
                                                                     'inbound_anomaly_score',
                                                                     0)) # The last incomplete entry + the two first custom ones.
        self.assertEqual(229, self._filterEntryListAndCountByPredicate(entryList,
                                                                       'inbound_anomaly_score',
                                                                       2))
        self.assertEqual(6, self._filterEntryListAndCountByPredicate(entryList,
                                                                     'inbound_anomaly_score',
                                                                     4))

        # Checking message list.        
        self.assertEqual(228, self._filterEntryListAndCountByMessage(entryList,
                                                                    [(u'REQUEST_HEADERS:Host', u'960017'),
                                                                     (u'TX:anomaly_score', u'981174'),
                                                                     (u'TX:inbound_anomaly_score', u'981203')]))
        
        self.assertEqual(6, self._filterEntryListAndCountByMessage(entryList,
                                                                   [(u'REQUEST_HEADERS:Host', u'960017'),
                                                                    (u'TX:sqli_select_statement_count', u'981317'),
                                                                    (u'TX:anomaly_score', u'981174'),
                                                                    (u'TX:inbound_anomaly_score', u'981203')]))
        
        self.assertEqual(1, self._filterEntryListAndCountByMessage(entryList,[]))

    def _filterEntryListAndCountByPredicate(self, entryList, predicateAccessorName, predicateValue):
        return self._filterEntryListAndCount(entryList,
                                             lambda e: getattr(e, predicateAccessorName)() == predicateValue)

    def _filterEntryListAndCountByMessage(self, entryList, payloadContainerRuleIdPairList):
        def filterFunction(entry):
            return [(message.payload_container(), message.rule_id()) for message in entry.message_list()] \
                == payloadContainerRuleIdPairList
        return self._filterEntryListAndCount(entryList, filterFunction)
    
    def _filterEntryListAndCount(self, entryList, filterFunction):
        return len(list(filter(filterFunction, entryList)))
