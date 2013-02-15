#-*- coding: utf-8 -*-
#
# Created on Jan 24, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract, new_contract
from modsecurity_exception_factory.config import Config
from modsecurity_exception_factory.modsecurity_audit_correlator import \
    ModsecurityAuditCorrelator
from modsecurity_exception_factory.modsecurity_audit_data_source import \
    IModsecurityAuditDataSource, ModsecurityAuditDataSourceSQL
from modsecurity_exception_factory.modsecurity_audit_log_parser import \
    ModsecurityAuditLogParser
import argparse
import contracts
import io
import sys

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
                                    help = u"Modsecurity audit log file path or '-' to read from standard input.")
        argumentParser.add_argument(u"-d",
                                    u"--data-url",
                                    dest = 'dataURL',
                                    type = unicode,
                                    required = True,
                                    default = None,
                                    help = u"Example: 'sqlite:////tmp/modsecurity-exception-factory.db'")
        argumentParser.add_argument(u"-c",
                                    u"--config-file",
                                    dest = 'configFilePath',
                                    type = unicode,
                                    default = None)
    
        argumentObject = argumentParser.parse_args(argumentList)

        # Parse config if given.
        config = None
        if argumentObject.configFilePath is not None:
            config = Config(argumentObject.configFilePath)
        
        ignoredVariableDict = {}
        if config is not None:
            ignoredVariableDict = config.ingoredVariableDict()

        # Initialize data source object.
        dataSource = ModsecurityAuditDataSourceSQL(argumentObject.dataURL)
        
        # Parse log if given.
        if argumentObject.modsecurityAuditLogPath is not None:
            self._parseFile(argumentObject.modsecurityAuditLogPath, dataSource)

        # Correlate.
        for correlation in ModsecurityAuditCorrelator().correlate(dataSource, ignoredVariableDict):
            print(correlation)
    
        return 0

    @contract
    def _parseFile(self, modsecurityAuditLogPath, dataSource):
        """
    :type modsecurityAuditLogPath: unicode
    :type dataSource: IModsecurityAuditDataSource
"""
        with self._stream(modsecurityAuditLogPath) as modsecAuditLogStream:
            iterable = ModsecurityAuditLogParser().parseStream(modsecAuditLogStream)
            dataSource.insertModsecurityAuditEntryIterable(iterable)
    
    def _stream(self, modsecurityAuditLogPath):
        if modsecurityAuditLogPath == "-":
            modsecurityAuditLogPath = sys.stdin.fileno()
        
        return io.open(modsecurityAuditLogPath, 'rt', errors = 'replace')

def main():
    return CommandModsecurityExceptionFactory().main(sys.argv[1:])

if __name__ == '__main__':
    sys.exit(main())
