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

new_contract('ModsecurityAuditLogParserState', ModsecurityAuditLogParserState)

class ModsecurityAuditLogSectionParserA(IModsecurityAuditLogSectionParser):

    @contract
    def parseLine(self, state):
        """
    :type state: ModsecurityAuditLogParserState
"""
        # The first line of the A section means that we reached a new entry.
        if state.currentSectionLineIndex() == 0:
            state.setReachedEntryStart(True)
