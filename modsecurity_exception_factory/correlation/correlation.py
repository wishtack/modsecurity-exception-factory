#-*- coding: utf-8 -*-
#
# Created on Feb 6, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from collections import OrderedDict
from synthetic import synthesize_constructor, synthesize_member
import copy

@synthesize_member('variable_name', contract = str, read_only = True)
@synthesize_member('variable_value_set', contract = 'Iterable', read_only = True)
@synthesize_member('item_count', contract = 'int', read_only = True)
@synthesize_member('sub_correlation_list', default = [], contract = 'Iterable', read_only = True)
@synthesize_constructor()
class Correlation(object):
    """
A correlation is a tree-chained object. Each correlation object a.k.a. node, contains a variable name, a set of variable values
corresponding to the variable name and a list of children nodes called subcorrelations.
"""

    def __init__(self):
        self._check_sub_correlation_iterable_or_item_count(self._sub_correlation_list, self._item_count)
        
        # Converting iterables to list. 
        if not isinstance(self._sub_correlation_list, list):
            self._sub_correlation_list = list(self._sub_correlation_list)

    @classmethod
    def load_from_dict(cls, correlation_dict):
        kwargs = {}
        
        # Keeping those items as is.
        for key in ['variable_name', 'item_count']:
            kwargs[key] = correlation_dict[key]
        
        # Converting value list to set.
        kwargs['variable_value_set'] = set(unicode(variable_value) for variable_value in correlation_dict['variable_value_list'])

        # Converting sub correlation list dicts to `Correlation` objects list.
        sub_correlation_list = []
        for sub_correlation_dict in correlation_dict.get('sub_correlation_list', []):
            sub_correlation_list.append(Correlation.load_from_dict(sub_correlation_dict))

        kwargs['sub_correlation_list'] = sub_correlation_list

        return Correlation(**kwargs)

    def mergeable_variable_dict(self):
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
        variable_dict = OrderedDict([(self._variable_name, self._variable_value_set)])
        
        # We yield items recursively until there are no children left or there's more than one child.
        if len(self._sub_correlation_list) == 1:
            variable_dict.update(self._sub_correlation_list[0].mergeable_variable_dict())

        return variable_dict
    
    def unmergeable_sub_correlation_list(self):
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
        sub_correlation_list_length = len(self._sub_correlation_list)
        
        # Node has no children.
        if sub_correlation_list_length == 0:
            return []
        
        # Node has only one child, we ask the child.
        elif sub_correlation_list_length == 1:
            return self._sub_correlation_list[0].unmergeable_sub_correlation_list()
        
        # Node has multiple children, those are the unmergeable correlations.
        else:
            return copy.copy(self._sub_correlation_list)

    def __repr__(self):
        return self._to_string()

    def _sorted_variable_value_list(self):
        return sorted([value.encode('utf-8') for value in self._variable_value_set])

    def _to_string(self, indent = u""):
        variable_value_list = list(self._variable_value_set)
        variable_value_list.sort()
        variable_value_list_as_string = u", ".join([unicode(v) for v in variable_value_list])
        repr_string = u"{indent}{variable_name} (count={item_count}) = {variable_value_list}\n" \
                      .format(indent = indent,
                              item_count = self.item_count(),
                              variable_name = self._variable_name,
                              variable_value_list = variable_value_list_as_string)
        for sub_correlation in self._sub_correlation_list:
            repr_string += sub_correlation._to_string(indent + u"        ")
        return repr_string

    def _check_sub_correlation_iterable_or_item_count(self, sub_correlation_iterable, item_count):
        """
    :type sub_correlation_iterable: Iterable|None
    :type item_count: int|None
"""
        # This is a 'xor', item_count and subCorrelationList can't be both None or both not None.
        if item_count is None and sub_correlation_iterable is None:
            raise TypeError(u"'item_count' and 'sub_correlation_iterable' can't be both None.")
