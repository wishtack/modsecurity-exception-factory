#-*- coding: utf-8 -*-
#
# Created on Jan 8, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#
from synthetic.decorators import synthesizeMember


@synthesizeMember('hostNameList', 'list(unicode)')
@synthesizeMember('requestNameList', 'list(unicode)')
@synthesizeMember('payloadContainerList', 'list(unicode)')
@synthesizeMember('ruleIdList', 'list(unicode)')
class ModsecurityExcetion:
    pass
