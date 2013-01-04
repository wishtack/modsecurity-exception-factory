#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#
from modsecurity_exception_factory.modsecurity_audit_entry import ModsecurityAuditEntry
from modsecurity_exception_factory.modsecurity_audit_log_parser.i_modsecurity_audit_log_section_parser import \
    IModsecurityAuditLogSectionParser
from synthetic.decorators import synthesizeMember, synthesizeConstructor

@synthesizeMember('currentLineString', contract = unicode)
@synthesizeMember('currentSectionLineIndex', contract = int, defaultValue = 0)
@synthesizeMember('currentSectionParser', contract = IModsecurityAuditLogSectionParser)
@synthesizeMember('modsecurityAuditEntry', contract = ModsecurityAuditEntry)
@synthesizeMember('reachedEntryStart', contract = bool)
@synthesizeConstructor()
class ModsecurityAuditLogParserState:
    def incrementCurrentSectionLineIndex(self):
        self._currentSectionLineIndex += 1
