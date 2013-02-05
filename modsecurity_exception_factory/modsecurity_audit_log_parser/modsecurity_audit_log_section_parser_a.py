#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .i_modsecurity_audit_log_section_parser import IModsecurityAuditLogSectionParser
from .modsecurity_audit_log_parser_state import ModsecurityAuditLogParserState
from contracts import contract, new_contract

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
