#-*- coding: utf-8 -*-
#
# Created on Jan 24, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract
from contracts.main import new_contract
from modsecurity_exception_factory.modsecurity_audit_correlator import ModsecurityAuditCorrelator
from modsecurity_exception_factory.modsecurity_audit_data_source.i_modsecurity_audit_data_source import \
    IModsecurityAuditDataSource
from modsecurity_exception_factory.modsecurity_audit_data_source.modsecurity_audit_data_source_sql import \
    ModsecurityAuditDataSourceSQL
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_parser import \
    ModsecurityAuditLogParser
from pprint import pprint
import argparse
import io
import sys

import contracts

new_contract('IModsecurityAuditDataSource', IModsecurityAuditDataSource)

class CommandModsecurityExceptionFactory:
    
    def main(self, argumentList):
        # Disabling contracts solves some performance issues.
        contracts.disable_all()

        argumentParser = argparse.ArgumentParser(description = u"Make ModSecurity exceptions.")
        argumentParser.add_argument(u"-i",
                                    u"--input",
                                    metavar = u"MODSEC_AUDIT_LOG_FILE",
                                    dest = 'modsecurityAuditLogPath',
                                    type = unicode,
                                    default = None,
                                    help = u"Modsecurity audit log file path.")
        argumentParser.add_argument(u"-d",
                                    u"--data-url",
                                    dest = 'dataURL',
                                    type = unicode,
                                    required = True,
                                    default = None,
                                    help = u"Exemple: 'sqlite:////tmp/modsecurity-exception-factory.db'")
    
        argumentObject = argumentParser.parse_args(argumentList)
            
        # Initialize data source object.
        dataSource = ModsecurityAuditDataSourceSQL(argumentObject.dataURL)
        
        # Parse log if given.
        if argumentObject.modsecurityAuditLogPath is not None:
            self._parseFile(argumentObject.modsecurityAuditLogPath, dataSource)

        # Correlate.
        correlationList = list(ModsecurityAuditCorrelator().correlate(dataSource))
        pprint(correlationList)
    
        return 0

    @contract
    def _parseFile(self, modsecurityAuditLogPath, dataSource):
        """
    :type modsecurityAuditLogPath: unicode
    :type dataSource: IModsecurityAuditDataSource
"""
        with io.open(modsecurityAuditLogPath, 'rt', errors = 'replace') as modsecAuditLogStream:
            iterable = ModsecurityAuditLogParser().parseStream(modsecAuditLogStream)
            dataSource.insertModsecurityAuditEntryIterable(iterable)

def main():
    return CommandModsecurityExceptionFactory().main(sys.argv[1:])

if __name__ == '__main__':
    sys.exit(main())
