#-*- coding: utf-8 -*-
#
# Created on Jan 24, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract, new_contract
from modsecurity_exception_factory.correlation.correlation_engine import \
    CorrelationEngine
from modsecurity_exception_factory.correlation.correlation_progress_listener_console import \
    CorrelationProgressListenerConsole
from modsecurity_exception_factory.modsecurity_audit_data_source import \
    IModsecurityAuditDataSource, ModsecurityAuditDataSourceSQL
from modsecurity_exception_factory.modsecurity_audit_log_parser import \
    ModsecurityAuditLogParser
from modsecurity_exception_factory.utils import Config
import argparse
import contracts
import io
import sys
from modsecurity_exception_factory.modsecurity_exception_writer import ModsecurityExcetionWriter

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
        
        # Try to parse config.
        config = Config(argumentObject.configFilePath)
        variableNameList = config.variableNameList()
        ignoredVariableDict = config.ignoredVariableDict()
        minimumOccurrenceCountThreshold = config.minimumOccurrenceCountThreshold()
        maximumValueCountThreshold = config.maximumValueCountThreshold()
        

        # Initialize data source object.
        dataSource = ModsecurityAuditDataSourceSQL(argumentObject.dataURL)
        
        # Parse log if given.
        if argumentObject.modsecurityAuditLogPath is not None:
            self._parseFile(argumentObject.modsecurityAuditLogPath, dataSource)

        # Preparing correlation engine.
        correlationEngine = CorrelationEngine(variableNameList,
                                              ignoredVariableDict,
                                              minimumOccurrenceCountThreshold,
                                              maximumValueCountThreshold)
        correlationEngine.addProgressListener(CorrelationProgressListenerConsole(sys.stderr))
        
        # Correlating and writing exceptions progressively using the power of Python generators.
        ModsecurityExcetionWriter(stream = sys.stdout).write(correlationEngine.correlate(dataSource))
    
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

    def _printCorrelation(self, correlation):
        encoding = sys.stdout.encoding
        if encoding is None:
            encoding = sys.getdefaultencoding()
        print(unicode(correlation).encode(encoding, errors = 'replace'))

def main():
    return CommandModsecurityExceptionFactory().main(sys.argv[1:])

if __name__ == '__main__':
    sys.exit(main())
