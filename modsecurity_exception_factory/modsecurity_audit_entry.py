#-*- coding: utf-8 -*-
#
# Created on Jan 2, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import new_contract, contract
from modsecurity_exception_factory.modsecurity_audit_entry_message import ModsecurityAuditEntryMessage
from synthetic import synthesizeMember, synthesizeConstructor

new_contract('ModsecurityAuditEntryMessage', ModsecurityAuditEntryMessage)

@synthesizeMember('hostName', contract = unicode)
@synthesizeMember('requestFileName', contract = unicode)
@synthesizeMember('messageList', contract = 'list(ModsecurityAuditEntryMessage)')
@synthesizeMember('inboundAnomalyScore', defaultValue = 0, contract = int)
@synthesizeConstructor()
class ModsecurityAuditEntry:
    def __init__(self):
        self._messageList = []
    
    @contract
    def appendMessage(self, message):
        """
    :type message: ModsecurityAuditEntryMessage
"""
        self._messageList.append(message)
