#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract, new_contract
from modsecurity_exception_factory.modsecurity_audit_entry import ModsecurityAuditEntry
from modsecurity_exception_factory.modsecurity_audit_entry_data_source.sql_base import SQLBase
from modsecurity_exception_factory.modsecurity_audit_entry_data_source.sql_modsecurity_audit_entry_message import \
    SQLModsecurityAuditEntryMessage
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import distinct

new_contract('ModsecurityAuditEntry', ModsecurityAuditEntry)
new_contract('SQLModsecurityAuditEntryMessage', SQLModsecurityAuditEntryMessage)

class ModsecurityAuditEntryDataSourceSQL:
    _DATA_INSERTION_BUFFER_SIZE = 100
    
    @contract
    def __init__(self, dataBaseUrl):
        """
    :type dataBaseUrl: unicode
"""
        self._dataBaseUrl = dataBaseUrl
        self._sqlEngine = create_engine(dataBaseUrl)
        self._sessionMaker = sessionmaker(bind = self._sqlEngine)
        self._columnNameList = None
        self._initialized = False

    def insertModsecurityAuditEntryIterable(self, modsecurityAuditEntryIterable):
        self._initializeDataBase()
        
        sqlModsecurityAuditEntryMessageBuffer = []
        
        for modsecurityAuditEntry in modsecurityAuditEntryIterable:
            hostName = modsecurityAuditEntry.hostName()
            requestFileName = modsecurityAuditEntry.requestFileName()
            for message in modsecurityAuditEntry.messageList():
                sqlMessage = SQLModsecurityAuditEntryMessage()
                sqlMessage.hostName = hostName
                sqlMessage.requestFileName = requestFileName
                sqlMessage.payloadContainer = message.payloadContainer()
                sqlMessage.ruleId = message.ruleId()
                
                # Insert message.
                self._insertModsecurityAuditEntryMessage(sqlModsecurityAuditEntryMessageBuffer, sqlMessage)
        
        self._flushModsecurityAuditEntryMessageBuffer(sqlModsecurityAuditEntryMessageBuffer)

    @contract
    def variableValueIterable(self, columnName):
        """
    :type columnName: str
"""
        if not self._columnExists(columnName):
            return
        
        try:
            session = self._sessionMaker()
            for row in session.query(distinct(getattr(SQLModsecurityAuditEntryMessage, columnName))):
                yield row[0]
        finally:
            session.close()

    def _initializeDataBase(self):
        if self._initialized:
            return

        SQLBase.metadata.create_all(self._sqlEngine)
        self._initialized = True

    def _columnExists(self, columnName):
        return SQLModsecurityAuditEntryMessage.__table__.columns.has_key(columnName)

    @contract
    def _insertModsecurityAuditEntryMessage(self, sqlModsecurityAuditEntryMessageBuffer, sqlModsecurityAuditEntryMessage):
        """
    :type sqlModsecurityAuditEntryMessageBuffer: list(SQLModsecurityAuditEntryMessage)
    :type sqlModsecurityAuditEntryMessage: SQLModsecurityAuditEntryMessage
"""
        if len(sqlModsecurityAuditEntryMessageBuffer) >= self._DATA_INSERTION_BUFFER_SIZE:
            self._flushModsecurityAuditEntryMessageBuffer(sqlModsecurityAuditEntryMessageBuffer)
        
        sqlModsecurityAuditEntryMessageBuffer.append(sqlModsecurityAuditEntryMessage)

    @contract
    def _flushModsecurityAuditEntryMessageBuffer(self, sqlModsecurityAuditEntryMessageBuffer):
        """
    :type sqlModsecurityAuditEntryMessageBuffer: list(SQLModsecurityAuditEntryMessage)
"""
        session = self._sessionMaker()
        try:
            session.add_all(sqlModsecurityAuditEntryMessageBuffer)
            session.commit()
            del sqlModsecurityAuditEntryMessageBuffer[:]
        finally:
            session.close()
