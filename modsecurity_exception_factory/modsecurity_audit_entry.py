#-*- coding: utf-8 -*-
#
# Created on Jan 2, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import new_contract, contract
from modsecurity_exception_factory.modsecurity_audit_entry_message import ModsecurityAuditEntryMessage
from synthetic import synthesizeMember, synthesizeConstructor

new_contract('ModsecurityAuditEntryMessage', ModsecurityAuditEntryMessage)

@synthesizeMember('hostName', contract = 'unicode|None')
@synthesizeMember('requestFileName', contract = 'unicode|None')
@synthesizeMember('messageList', contract = 'list(ModsecurityAuditEntryMessage)|None')
@synthesizeMember('inboundAnomalyScore', contract = 'int|None', defaultValue = 0)
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
