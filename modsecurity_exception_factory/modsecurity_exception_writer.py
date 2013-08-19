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

@synthesize_member('stream')
@synthesize_member('rule_id', default = 10000)
@synthesize_member('marker_id', default = 1, read_only = True)
@synthesize_member('marker_prefix', default = u"EXCEPTION_")
@synthesize_constructor()
class ModsecurityExceptionWriter(object):

    # Variables are splitted in two types, 'conditional' and 'action'.
    # Conditional variables are used in "SecRule variable_name '@rx...'" kind of rules.
    # Action variables are the variables who are used in "SecAction ...removeTargetById" kind of rules.

    # Dictionary that maps model variables to ModSecurity rules variables.
    _CONDITIONAL_VARIABLE_DICT = {SQLModsecurityAuditEntryMessage.host_name.name: u"SERVER_NAME",
                                  SQLModsecurityAuditEntryMessage.request_file_name.name: u"REQUEST_FILENAME"}
    
    _ACTION_VARIABLE_LIST = [SQLModsecurityAuditEntryMessage.rule_id.name,
                             SQLModsecurityAuditEntryMessage.payload_container.name]
                           

    @synthesize_member('depth', default = 0)
    @synthesize_member('value_list_dict', contract = 'dict(str:list(unicode))', default = {})
    @synthesize_member('item_count', default = None)
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
        context = ModsecurityExceptionWriter._Context()
        
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
        variable_name = correlation.variable_name()
        marker_id = None # Will be set only if correlation produces a conditional rule with valid values.

        # @hack: ignoring 'None' values.
        variable_value_list = sorted(value for value in correlation.variable_value_set() if value is not None)

        child_context = copy.deepcopy(context)
        
        # Unknown variable.
        if variable_name not in self._ACTION_VARIABLE_LIST + self._CONDITIONAL_VARIABLE_DICT.keys():
            raise UnknownVariable(variable_name = variable_name)
        
        # Adding variable values to context if it's an action variable        
        if variable_name in self._ACTION_VARIABLE_LIST:
            child_context.extend_value_list(variable_name, variable_value_list)
            child_context.set_item_count(correlation.item_count())
        
        # Conditional rule.
        if variable_name in self._CONDITIONAL_VARIABLE_DICT.keys() and variable_value_list:
            self._write_conditional_rule(context,
                                         variable_name,
                                         variable_value_list,
                                         correlation.item_count())
        
            # Remember current marker id because the global marker id will be incremented below and during recursion through sub correlations.
            marker_id = self._marker_id
            
            # Incrementing marker id and depth.
            self._marker_id += 1
            
            child_context.increment_depth()

        # In both situations (action or conditional), write sub correlations.
        self._write_correlation_list(child_context, correlation.sub_correlation_list())
            
        if marker_id is not None:
            # Writing the marker.
            self._write_marker(context, marker_id)
    
    def _write_conditional_rule(self, context, variable_name, variable_value_list, item_count):
        self._write_hit_count_comment_line(context, item_count)
        
        # Writing the 'SecRule' condition that skips to marker if variable is not matching.
        variable_value_regex = u"|".join([re.escape(variable_value) for variable_value in variable_value_list])
        directive = u"""SecRule {variable_name} "!@rx ^({variable_value_regex})$" "id:{rule_id},t:none,nolog,pass,skipAfter:{marker}\""""\
            .format(rule_id = self._generate_rule_id(),
                    variable_name = self._CONDITIONAL_VARIABLE_DICT[variable_name],
                    variable_value_regex = variable_value_regex,
                    marker = self._make_marker(self.marker_id()),
                    item_count = item_count)
        self._write_directive(context, directive)

    def _write_leaf(self, context):
        value_list_dict = context.value_list_dict()
        payload_container_list = value_list_dict.get(SQLModsecurityAuditEntryMessage.payload_container.name)
        rule_id_list = value_list_dict.get(SQLModsecurityAuditEntryMessage.rule_id.name)
        
        self._write_hit_count_comment_line(context, context.item_count())
        
        # No rule id, nothing to do.
        if not rule_id_list:
            return
        
        if not payload_container_list:
            directive = u"""SecAction "id:{rule_id},t:none,nolog,pass,ctl:'ruleRemoveById={rule_id_list_string}'\""""\
                .format(rule_id = self._generate_rule_id(),
                        rule_id_list_string = u",".join(unicode(r) for r in rule_id_list))
            self._write_directive(context, directive)
        
        else:
            for rule_id_to_modify in rule_id_list:
                directive = u"""SecAction "id:{rule_id},t:none,nolog,pass,ctl:'ruleRemoveTargetById={rule_id_to_modify};{payload_container_list_string}'\""""\
                    .format(rule_id = self._generate_rule_id(),
                            rule_id_to_modify = rule_id_to_modify,
                            payload_container_list_string = u",".join(payload_container_list))
                self._write_directive(context, directive)

    def _write_directive(self, context, directive):
        indentation = context.depth() * u"    "
        self.stream().write(u"{indentation}{directive}\n"\
                            .format(indentation = indentation, directive = directive)\
                            .encode('utf-8'))

    def _write_hit_count_comment_line(self, context, item_count):
        self._write_directive(context, u"")
        self._write_directive(context, u"# Hit Count: {item_count}".format(item_count = item_count))

    def _write_marker(self, context, marker_id):
        # Writing the marker.
        self._write_directive(context, u"")
        self._write_directive(context, u"SecMarker {marker}".format(marker = self._make_marker(marker_id)))
    
    def _generate_rule_id(self):
        rule_id = self._rule_id
        self._rule_id += 1
        return rule_id

    def _make_marker(self, marker_id):
        return u"{marker_prefix}{marker_id}".format(marker_prefix = self._marker_prefix,
                                                    marker_id = marker_id)
