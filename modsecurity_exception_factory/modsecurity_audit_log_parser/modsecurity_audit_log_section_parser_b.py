#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract, new_contract
from modsecurity_exception_factory.modsecurity_audit_log_parser.i_modsecurity_audit_log_section_parser import \
    IModsecurityAuditLogSectionParser
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_parser_state import \
    ModsecurityAuditLogParserState
import re

new_contract('ModsecurityAuditLogParserState', ModsecurityAuditLogParserState)

class ModsecurityAuditLogSectionParserB(IModsecurityAuditLogSectionParser):
    def __init__(self):
        self._regexHostHeader = re.compile(r"^Host: *(?P<hostName>[^:/]*)")

    @contract
    def parseLine(self, state):
        """
    :type state: ModsecurityAuditLogParserState
"""
        modsecurityAuditEntry = state.modsecurityAuditEntry()
        if modsecurityAuditEntry is None:
            return
                
        lineIndex = state.currentSectionLineIndex()
        strLine = state.currentLineString()
        if lineIndex == 1: self._parseRequestLine(modsecurityAuditEntry, strLine)
        
        # otherwise.
        matchResult = self._regexHostHeader.match(strLine)
        if matchResult is not None:
            modsecurityAuditEntry.setHostName(matchResult.groupdict()['hostName'])

    def _parseRequestLine(self, modsecurityAuditEntry, strLine):
        partList = strLine.split(u" ")
        if len(partList) < 3:
            # LOG WARNING:
            return
        
        uri = partList[1]
        
        # Retrieve request file name from uri.
        requestFileName = uri.split(u"?")[0].strip()
        
        modsecurityAuditEntry.setRequestFileName(requestFileName)
