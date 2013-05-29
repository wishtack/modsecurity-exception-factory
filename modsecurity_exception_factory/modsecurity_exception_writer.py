#-*- coding: utf-8 -*-
#
# Created on May 29, 2013
#
# @author: Younes JAAIDI <yjaaidi@shookalabs.com>
#
# $Id$
#

from contracts import contract
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_modsecurity_audit_entry_message import \
    SQLModsecurityAuditEntryMessage
from synthetic.decorators import synthesize_member, synthesize_constructor
import copy
import re

class UnknownVariable(Exception):

    def __init__(self, variable_name):
        super(self).__init__(u"Unknown variable name: '{variable_name}'".format(variable_name = variable_name))

@synthesize_member('marker_id', default = 1, read_only = True)
@synthesize_member('stream')
@synthesize_constructor()
class ModsecurityExcetionWriter(object):

    # Variables are splitted in two types, 'conditional' and 'action'.
    # Conditional variables are used in "SecRule variable_name '@rx...'" kind of rules.
    # Action variables are the variables who are used in "SecAction ...removeTargetById" kind of rules.

    # Dictionary that maps model variables to ModSecurity rules variables.
    _CONDITIONAL_VARIABLE_DICT = {SQLModsecurityAuditEntryMessage.host_name.name: u"HOSTNAME",
                                  SQLModsecurityAuditEntryMessage.request_file_name.name: u"REQUEST_FILENAME"}
    
    _ACTION_VARIABLE_LIST = [SQLModsecurityAuditEntryMessage.rule_id.name,
                             SQLModsecurityAuditEntryMessage.payload_container.name]
                           

    @synthesize_member('depth', default = 0)
    @synthesize_member('value_list_dict', contract = 'dict(str:list(str))', default = {})
    @synthesize_constructor()
    class _Context(object):
        
        def increment_depth(self):
            self._depth += 1
        
        @contract
        def extend_value_list(self, variable_name, value_list):
            """
            :type variable_name: str
            :type value_list: list(unicode)
            """
            self._value_list_dict.setdefault(variable_name, [])
            self._value_list_dict[variable_name].extend(value_list)

    @contract
    def write(self, correlation_iterable):
        """
        :type correlation_iterable: Iterable
"""
        # New context.
        context = ModsecurityExcetionWriter._Context()
        
        self._write_correlation_list(context, correlation_iterable)
        
    def _write_correlation_list(self, context, correlation_list):
        # Is not empty.
        if correlation_list:
            for sub_correlation in correlation_list:
                self._write_correlation(context, sub_correlation)

        # It's empty, so we'll write stuff from the context if any.
        else:
            self._write_leaf(context)
    
    def _write_correlation(self, context, correlation):
        marker_id = None # No marker to write.
        variable_name = correlation.variable_name()

        # Adding variable values to context if it's an action variable        
        if variable_name in self._ACTION_VARIABLE_LIST:
            context.extend_value_list(variable_name, list(correlation.variable_value_set()))
            self._write_correlation_list(copy.deepcopy(context), correlation.sub_correlation_list())
        
        # Conditional rule.
        elif variable_name in self._CONDITIONAL_VARIABLE_DICT.keys():
            self._write_conditional_rule(context, correlation)
            
            # Remember current marker id because the global marker id will be incremented below and during recursion through sub correlations.
            marker_id = self._marker_id
            
            # Incrementing marker id and depth.
            self._marker_id += 1
            child_context = copy.deepcopy(context)
            child_context.increment_depth()
            self._write_correlation_list(child_context, correlation.sub_correlation_list())
            
            # Writing the marker.
            self._write_marker(context, marker_id)
        
        # Unknown variable.
        else:
            raise UnknownVariable(variable_name = variable_name)
    
    def _write_conditional_rule(self, context, correlation):
        self._write_directive(context, u"# Hit Count: {item_count}".format(item_count = correlation.item_count()))

        # Writing the 'SecRule' condition that skips to marker if variable is not matching.
        variable_value_list = sorted(list(correlation.variable_value_set()))
        variable_value_regex = u"|".join([re.escape(variable_value) for variable_value in variable_value_list])
        directive = u"""SecRule {variable_name} "!@rx ^({variable_value_regex})$" "t:none,nolog,pass,skipAfter:{marker_id}\""""\
            .format(variable_name = self._CONDITIONAL_VARIABLE_DICT[correlation.variable_name()],
                    variable_value_regex = variable_value_regex,
                    marker_id = self.marker_id(),
                    item_count = correlation.item_count())
        self._write_directive(context, directive)

    def _write_marker(self, context, marker_id):
        # Writing the marker.
        self._write_directive(context, u"SecMarker {marker_id}\n".format(marker_id = marker_id))
    
    def _write_leaf(self, context):
        value_list_dict = context.value_list_dict()
        payload_container_list = value_list_dict.get(SQLModsecurityAuditEntryMessage.payload_container.name)
        rule_id_list = value_list_dict.get(SQLModsecurityAuditEntryMessage.rule_id.name)
        
        if payload_container_list:
            directive = u"""SecAction "t:none,nolog,pass,ctl:'ruleRemoveById={rule_id_list_string}'\""""\
                .format(rule_id_list_string = u",".join(unicode(r) for r in rule_id_list))
            self._write_directive(context, directive)
        
        else:
            for rule_id in rule_id_list:
                directive = u"""SecAction "t:none,nolog,pass,ctl:'ruleRemoveTargetById={rule_id};{payload_container_list_string}'\""""\
                    .format(rule_id = rule_id, payload_container_list_string = u",".join(payload_container_list))
                self._write_directive(context, directive)

    def _write_directive(self, context, directive):
        indentation = context.depth() * u"    "
        self.stream().write(u"{indentation}{directive}\n"\
                            .format(indentation = indentation, directive = directive))
