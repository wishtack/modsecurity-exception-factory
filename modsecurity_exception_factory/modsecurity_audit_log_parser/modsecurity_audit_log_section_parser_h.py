#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from ..modsecurity_audit_entry_message import ModsecurityAuditEntryMessage
from .i_modsecurity_audit_log_section_parser import IModsecurityAuditLogSectionParser
from .modsecurity_audit_log_parser_state import ModsecurityAuditLogParserState
from contracts import contract, new_contract
import re

new_contract('ModsecurityAuditLogParserState', ModsecurityAuditLogParserState)

class ModsecurityAuditLogSectionParserH(IModsecurityAuditLogSectionParser):    
    def __init__(self):
        self._regexMessage = re.compile(r"^Message: .* (?:at|against) (?P<payload_container>[^. ]+).* \[id \"(?P<rule_id>\d+)\"\]")
        self._regexMessageInboundAnomalyScore = re.compile(r"Total Score: (?P<inbound_anomaly_score>\d+)\b")
    
    @contract
    def parseLine(self, state):
        """
    :type state: ModsecurityAuditLogParserState
"""
        modsecurityAuditEntry = state.modsecurityAuditEntry()
        if modsecurityAuditEntry is None:
            return
        
        strLine = state.currentLineString()
        self._parseMessage(modsecurityAuditEntry, strLine)
        
    def _parseMessage(self, modsecurityAuditEntry, strLine):
        matchResult = self._regexMessage.match(strLine)
        if matchResult is None:
            return
        message = ModsecurityAuditEntryMessage(**matchResult.groupdict())
        modsecurityAuditEntry.appendMessage(message)
        
        self._parseMessageInboundAnomalyScore(modsecurityAuditEntry, strLine, message)
    
    def _parseMessageInboundAnomalyScore(self, modsecurityAuditEntry, strLine, message):
        # Inbound anomaly score extraction from rules 981174 and 981176.
        if message.rule_id() not in ["981174", "981176"]:
            return
        
        scoreSearchResult = self._regexMessageInboundAnomalyScore.search(strLine)
        if scoreSearchResult is None:
            return
        
        modsecurityAuditEntry.set_inbound_anomaly_score(int(scoreSearchResult.groupdict()['inbound_anomaly_score']))
