#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract
from .i_modsecurity_audit_log_section_parser import IModsecurityAuditLogSectionParser

class ModsecurityAuditLogSectionParserUnknown(IModsecurityAuditLogSectionParser):
    @contract
    def parseLine(self, state):
        """
    :type state: ModsecurityAuditLogParserState
"""
        pass
