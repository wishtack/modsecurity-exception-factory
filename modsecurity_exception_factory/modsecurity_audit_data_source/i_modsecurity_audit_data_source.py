#-*- coding: utf-8 -*-
#
# Created on Jan 8, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from abc import abstractmethod
from modsecurity_exception_factory.correlation.i_item_data_source import \
    IItemDataSource

class IModsecurityAuditDataSource(IItemDataSource):
    
    @abstractmethod
    def insertModsecurityAuditEntryIterable(self, modsecurityAuditEntryIterable):
        raise NotImplementedError()

    @abstractmethod
    def variableValueIterable(self, columnName):
        raise NotImplementedError()

    @abstractmethod
    def itemDictIterable(self, variableNameList):
        raise NotImplementedError()

    @abstractmethod
    def orangeDataReader(self):
        raise NotImplementedError()
