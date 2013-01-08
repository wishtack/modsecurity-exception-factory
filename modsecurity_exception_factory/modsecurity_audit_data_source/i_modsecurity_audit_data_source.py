#-*- coding: utf-8 -*-
#
# Created on Jan 8, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#
from abc import abstractmethod

class IModsecurityAuditDataSource:
    
    @abstractmethod
    def insertModsecurityAuditEntryIterable(self, modsecurityAuditEntryIterable):
        raise NotImplementedError()

    @abstractmethod
    def variableValueIterable(self, columnName):
        raise NotImplementedError()
    
    @abstractmethod
    def orangeDataReader(self):
        raise NotImplementedError()
