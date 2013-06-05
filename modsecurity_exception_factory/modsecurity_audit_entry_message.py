#-*- coding: utf-8 -*-
#
# Created on Jan 2, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from synthetic import synthesizeMember, synthesizeConstructor

@synthesizeMember('rule_id', contract = unicode, readOnly = True)
@synthesizeMember('payload_container', contract = unicode, readOnly = True)
@synthesizeConstructor()
class ModsecurityAuditEntryMessage:
    pass
