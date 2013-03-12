#-*- coding: utf-8 -*-
#
# Created on Feb 6, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from collections import OrderedDict
from contracts import contract
from itertools import imap
from synthetic import synthesizeConstructor, synthesizeMember
import copy

@synthesizeMember('variableName', contract = str, readOnly = True)
@synthesizeMember('variableValueSet', contract = 'Iterable', readOnly = True)
@synthesizeMember('itemCount', contract = 'int', readOnly = True)
@synthesizeMember('subCorrelationList', default = [], contract = 'Iterable', readOnly = True)
@synthesizeConstructor()
class Correlation(object):
    """
A correlation is a tree-chained object. Each correlation object a.k.a. node, contains a variable name, a set of variable values
corresponding to the variable name and a list of children nodes called subcorrelations.
"""

    def __init__(self):
        self._checkSubCorrelationIterableOrItemCount(self._subCorrelationList, self._itemCount)
        
        # Converting iterables to list. 
        if not isinstance(self._subCorrelationList, list):
            self._subCorrelationList = list(self._subCorrelationList)
        
    def mergeableVariableDict(self):
        """
        :IMPORTANT: internal use. 

Example:
    a = a1
            b = b1, b2
                    c = c1
                        d = d2
                    d = d1
                        c = c2

Will return:

    OrderedDict([('a', set(['a1'])), ('b', set(['b1', 'b2']))])
"""
        variableDict = OrderedDict([(self._variableName, self._variableValueSet)])
        
        # We yield items recursively until there are no children left or there's more than one child.
        if len(self._subCorrelationList) == 1:
            variableDict.update(self._subCorrelationList[0].mergeableVariableDict())

        return variableDict
    
    def unmergeableSubCorrelationList(self):
        """
        :IMPORTANT: internal use. 

Example:
    a = a1
            b = b1, b2
                    c = c1
                        d = d2
                    d = d1
                        c = c2

Will return two correlation objects corresponding to the following structures:
    
    c = c1
        d = d2
and
    d = d1
        c = c2
"""
        subCorrelationListLength = len(self._subCorrelationList)
        
        # Node has no children.
        if subCorrelationListLength == 0:
            return []
        
        # Node has only one child, we ask the child.
        elif subCorrelationListLength == 1:
            return self._subCorrelationList[0].unmergeableSubCorrelationList()
        
        # Node has multiple children, those are the unmergeable correlations.
        else:
            return copy.copy(self._subCorrelationList)

    def __repr__(self):
        return self._toString()

    def _toString(self, indent = u""):
        variableValueList = list(self._variableValueSet)
        variableValueList.sort()
        variableValueListAsString = u", ".join([unicode(v) for v in variableValueList])
        reprString = u"{indent}{variableName} (count={itemCount}) = {variableValueList}\n"\
            .format(indent = indent,
                    itemCount = self.itemCount(),
                    variableName = self._variableName,
                    variableValueList = variableValueListAsString)
        for subCorrelation in self._subCorrelationList:
            reprString += subCorrelation._toString(indent + u"        ")
        return reprString        

    def _checkSubCorrelationIterableOrItemCount(self, subCorrelationIterable, itemCount):
        """
    :type subCorrelationIterable: Iterable|None
    :type itemCount: int|None
"""
        # This is a 'xor', itemCount and subCorrelationList can't be both None or both not None.
        if itemCount is None and subCorrelationIterable is None:
            raise TypeError(u"'itemCount' and 'subCorrelationIterable' can't be both None.")
