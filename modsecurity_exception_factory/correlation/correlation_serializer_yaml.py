#-*- coding: utf-8 -*-
#
# Created on May 29, 2013
#
# @author: Younes JAAIDI <yjaaidi@shookalabs.com>
#
# $Id$
#

from .correlation import Correlation
from contracts import contract
import yaml

class CorrelationSerializerYaml(object):

    def load(self, stream):
        for correlation_dict in yaml.load_all(stream):
            yield Correlation.load_from_dict(correlation_dict)

    @contract
    def write(self, correlation_iterable, stream):
        """
        :type correlation_iterable: Iterable
"""
        yaml.add_representer(Correlation, CorrelationSerializerYaml._correlation_yaml_representer)

        yaml.dump_all(correlation_iterable, stream = stream, default_flow_style = False)

    @classmethod
    def _correlation_yaml_representer(cls, dumper, correlation):
        data = [('variable_name', correlation.variable_name()),
                ('item_count', correlation.item_count()),
                ('variable_value_list', sorted(value.encode() for value in correlation.variable_value_set()))]

        sub_correlation_list = correlation.sub_correlation_list()
        if sub_correlation_list:
            data.append(('sub_correlation_list', sub_correlation_list))

        return dumper.represent_mapping(u'tag:yaml.org,2002:map', data)
