ModSecurity Exception Generator
###############################

**ModSecurity Exception Generator** is a tool that generates **ModSecurity** exception rules by automatically analyzing ModSecurity audit logs. This is very useful and almost essential to avoid false positives and rejecting legitimate clients.

Installation
************

.. code-block:: shell
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

.. code-block:: shell
    modsecurity-exception-generator \
        -i /path/to/modsec_audit.log \
        -d "sqlite:////tmp/service.db" \
    > modsecurity_crs_15_exceptions.conf

.. code-block:: shell
    zcat modsec_audit.log.*.gz \
    | modsecurity-exception-generator \
        -i - \
        -d "sqlite:////tmp/service.db" \
    > modsecurity_crs_15_exceptions.conf

WARNING
*******

 Exceptions must be loaded BEFORE the rules that they are applied to.

