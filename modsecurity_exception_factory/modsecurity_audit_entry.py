#-*- coding: utf-8 -*-
#
# Created on Jan 2, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .modsecurity_audit_entry_message import ModsecurityAuditEntryMessage
from contracts import new_contract, contract
from synthetic import synthesize_member, synthesize_constructor

new_contract('ModsecurityAuditEntryMessage', ModsecurityAuditEntryMessage)

@synthesize_member('host_name', contract = 'unicode|None')
@synthesize_member('request_file_name', contract = 'unicode|None')
@synthesize_member('message_list', contract = 'list(ModsecurityAuditEntryMessage)|None')
@synthesize_member('inbound_anomaly_score', default = 0, contract = 'int|None')
@synthesize_constructor()
class ModsecurityAuditEntry:
    def __init__(self):
        self._message_list = []
    
    @contract
    def appendMessage(self, message):
        """
    :type message: ModsecurityAuditEntryMessage
"""
        self._message_list.append(message)
