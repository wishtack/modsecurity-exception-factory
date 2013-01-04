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

new_contract('ModsecurityAuditEntry', ModsecurityAuditEntry)

class ModsecurityAuditEntryDataSourceSQL:
    @contract
    def __init__(self, dataBaseUrl):
        """
    :type dataBaseUrl: unicode
"""
        self._dataBaseUrl = dataBaseUrl
        self._sqlEngine = create_engine(dataBaseUrl)
        self._sessionMaker = sessionmaker(bind = self._sqlEngine)
        self._initialized = False

    def insertModsecurityAuditEntryIterable(self, modsecurityAuditEntryIterable):
        self._initializeDataBase()
        
        for modsecurityAuditEntry in modsecurityAuditEntryIterable:
            hostName = modsecurityAuditEntry.hostName()
            requestFileName = modsecurityAuditEntry.requestFileName()            
            for message in modsecurityAuditEntry.messageList():                
                # Insert message.
                session = self._sessionMaker()
                sqlMessage = SQLModsecurityAuditEntryMessage()
                sqlMessage.hostName = hostName
                sqlMessage.requestFileName = requestFileName
                sqlMessage.payloadContainer = message.payloadContainer()
                sqlMessage.ruleId = message.ruleId()
                session.add(sqlMessage)
                session.commit()

    def _initializeDataBase(self):
        if self._initialized:
            return

        SQLBase.metadata.create_all(self._sqlEngine)
        self._initialized = True
