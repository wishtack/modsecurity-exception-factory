#-*- coding: utf-8 -*-
#
# Created on Jan 15, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#
from abc import abstractmethod

class IItemIterable:

    @abstractmethod
    def __len__(self):
        raise NotImplementedError()

    @abstractmethod
    def mostFrequentVariableAndValue(self, variableNameList):
        raise NotImplementedError()

    @abstractmethod
    def distinct(self):
        raise NotImplementedError()

    @abstractmethod
    def filter(self, conditionDict, negate = False):
        raise NotImplementedError()
