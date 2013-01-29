#-*- coding: utf-8 -*-
#
# Created on Jan 15, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from abc import abstractmethod

class IItemDataSource:

    @abstractmethod
    def itemDictIterable(self, variableNameList):
        raise NotImplementedError()
