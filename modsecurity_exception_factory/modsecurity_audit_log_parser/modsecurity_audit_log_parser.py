#-*- coding: utf-8 -*-
#
# Created on Jan 2, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract, new_contract
from modsecurity_exception_factory.modsecurity_audit_entry import ModsecurityAuditEntry
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_parser_state import \
    ModsecurityAuditLogParserState
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_section_parser_factory import \
    ModsecurityAuditEntrySectionParserFactory
import re

new_contract('ModsecurityAuditLogParserState', ModsecurityAuditLogParserState)

class ModsecurityAuditLogParser:

    def __init__(self):
        self._sectionParserFactory = ModsecurityAuditEntrySectionParserFactory()
        self._regexModsecurityAuditEntrySectionMarker = re.compile(r"^--[0-9a-z]{8}-(?P<sectionType>[A-Z])--$")
        self._regexModsecurityAuditEntrySectionStartMarker = re.compile(r"^--[0-9a-z]{8}-A--$")
    
    def parseStream(self, stream):
        """'stream' must be a generator that yields unicode data. 
"""
        
        # Initialize parser state.
        state = ModsecurityAuditLogParserState(currentSectionParser = self._sectionParserFactory.sectionParser())
        modsecurityAuditEntry = None
        
        for strLine in self._lineGenerator(stream):
            state.setCurrentLineString(strLine)
            
            # Parse the current line.
            self._parseLine(state)
            
            modsecurityAuditEntry = state.modsecurityAuditEntry()
            if state.reachedEntryStart():
                # Reached a new entry, we yield the current entry if available...
                if modsecurityAuditEntry is not None:
                    yield modsecurityAuditEntry
                
                # ... then we reset the 'reachedEntryStart' flag and the 'ModsecurityAuditEntry'.
                state.setModsecurityAuditEntry(ModsecurityAuditEntry())
                state.setReachedEntryStart(False)
        
        if modsecurityAuditEntry is not None:
            yield modsecurityAuditEntry

    @contract
    def _parseLine(self, state):
        """
    :type state: ModsecurityAuditLogParserState
"""
        strLine = state.currentLineString()
        
        # Change section parser when we reach a bloc marker. 
        matchResult = self._regexModsecurityAuditEntrySectionMarker.match(strLine)
        if matchResult is not None:
            sectionType = matchResult.groupdict()['sectionType']
            state.setCurrentSectionParser(self._sectionParserFactory.sectionParser(sectionType))
            state.setCurrentSectionLineIndex(0)
        
        # Ask section parser to parse the current line.
        state.currentSectionParser().parseLine(state)
        state.incrementCurrentSectionLineIndex()

    def _lineGenerator(self, stream):
        for strLine in stream:
            yield self._canonicalize(strLine)

    @contract
    def _canonicalize(self, strLine):
        """
    :type strLine: unicode
"""
        return strLine.strip()
