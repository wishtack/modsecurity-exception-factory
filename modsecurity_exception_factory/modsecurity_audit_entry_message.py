#-*- coding: utf-8 -*-
#
# Created on Jan 2, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from synthetic import synthesizeMember, synthesizeConstructor

@synthesizeMember('ruleId', contract = unicode, readOnly = True)
@synthesizeMember('payloadContainer', contract = unicode, readOnly = True)
@synthesizeConstructor()
class ModsecurityAuditEntryMessage:
    pass
