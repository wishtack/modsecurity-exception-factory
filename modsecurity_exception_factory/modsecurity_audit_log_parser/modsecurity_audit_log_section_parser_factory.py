#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#
from contracts import contract
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_section_parser_a import \
    ModsecurityAuditLogSectionParserA
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_section_parser_b import \
    ModsecurityAuditLogSectionParserB
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_section_parser_h import \
    ModsecurityAuditLogSectionParserH
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_section_parser_unknown import \
    ModsecurityAuditLogSectionParserUnknown

class ModsecurityAuditEntrySectionParserFactory:
    
    def __init__(self):
        self._sectionParserDefault = ModsecurityAuditLogSectionParserUnknown()
        self._sectionParserDict = {u'A': ModsecurityAuditLogSectionParserA(),
                                   u'B': ModsecurityAuditLogSectionParserB(),
                                   u'H': ModsecurityAuditLogSectionParserH()}
    
    @contract
    def sectionParser(self, strSectionType = None):
        """If 'strSectionType' is None, this will return the default parser.
    :type strSectionType: unicode|None
"""
        return self._sectionParserDict.get(strSectionType, self._sectionParserDefault)
