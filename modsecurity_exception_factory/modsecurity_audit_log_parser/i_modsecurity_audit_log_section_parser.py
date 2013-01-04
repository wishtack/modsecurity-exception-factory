#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#
from abc import abstractmethod

class IModsecurityAuditLogSectionParser:
    
    @abstractmethod
    def parseLine(self, state):
        raise NotImplementedError()
