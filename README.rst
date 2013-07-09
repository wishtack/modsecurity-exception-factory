ModSecurity Exception Generator
###############################

**ModSecurity Exception Generator** is a tool that generates **ModSecurity** exception rules by automatically analyzing ModSecurity audit logs. This is very useful and almost essential to avoid false positives and rejecting legitimate clients.

Installation
************

.. code-block:: bash

 pip install modsecurity-exception-generator

Usage
*****

Command options
===============

-d
--
 SQL URL of the data store where the **ModSecurity** audit log parsed data will be stored and loaded from.

 *Example: 'sqlite:////tmp/modsecurity-exception-factory.db'.*

-i [Optional]
-------------
 Path to the ModSecurity audit log file to parse.

 One can use '-' as a value for this parameter to read the audit log data from standard input.

-c [Optional]
-------------
 Path of the optional configuration file. 

Basic examples
==============

.. code-block:: bash
    
    modsecurity-exception-generator \
        -i /path/to/modsec_audit.log \
        -d "sqlite:////tmp/service.db" \
    > modsecurity_crs_15_exceptions.conf

.. code-block:: bash
    
    zcat modsec_audit.log.*.gz \
    | modsecurity-exception-generator \
        -i - \
        -d "sqlite:////tmp/service.db" \
    > modsecurity_crs_15_exceptions.conf

WARNING
*******

 The produced exceptions must be loaded BEFORE the rules they are applied to.

Removing superfluous exceptions
===============================

Generating exceptions by simply running the '**modsecurity-exception-generator**' program, as in the basic examples, might generate some superfluous exception rules. Thus we need some advanced options to obtain smarter results. That's where the YAML configuration file given using the '**-c**' option comes in handy.

The YAML configuration file supports the following directives:

ignore
------

Indicates which logs most be ignored by the exception generator.

example
^^^^^^^

To ignore any log message produced by the rule with the id 981176.

.. code-block::
     
     ignore:
        rule_id: [981176]

This can also be applied to other variables like '**host_name**' *(targeted host name)*, '**request_filename**' *(targeted url)* or '**payload_container**' *(the variable that matched the rule)*.

minimum_occurrence_count_threshold
----------------------------------

Ignore exceptions that affect less than **minimum_occurence_count_threshold** log message occurrences.

maximum_value_count_threshold
-----------------------------

Sometimes, exceptions rules can have conditions with too many values like the following example.

.. code-block::
    
    SecRule REQUEST_FILENAME "@rx ^(/foo_bar|/blabla|/test_2/|...)$" ...

This condition can be ignored by setting **maximum_value_count_threshold** to a value lesser than the number of values in the regular expression.

Configuration example for the Core Rule Set
===========================================

.. code-block::
    
    ignore:
        rule_id: [981174, 981176, 981203, 981200, 981201, 981202, 981203, 981204, 981205, 981220]
    
    minimum_occurrence_count_threshold: 1000
