ModSecurity Exception Generator
###############################

**ModSecurity Exception Generator** is a tool that generates ModSecurity exception rules by automatically analyzing ModSecurity audit logs.

Usage
*****

.. code-block:: shell
    zcat modsec_audit.log.*.gz \
    | modsecurity-exception-generator \
        -i - \
        -d "sqlite:////tmp/service.db" \
    > modsecurity_01_service_exceptions.conf

WARNING
*******

Exceptions must be loaded BEFORE the rules that they are applied to.

