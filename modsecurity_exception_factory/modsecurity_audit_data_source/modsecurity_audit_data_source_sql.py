#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from ..modsecurity_audit_entry import ModsecurityAuditEntry
from .i_modsecurity_audit_data_source import IModsecurityAuditDataSource
from .modsecurity_audit_item_dict_iterable_sql import ModsecurityAuditItemDictIterableSQL
from .sql_base import SQLBase
from .sql_modsecurity_audit_entry_message import SQLModsecurityAuditEntryMessage
from contextlib import closing
from contracts import contract, new_contract
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

new_contract('ModsecurityAuditEntry', ModsecurityAuditEntry)
new_contract('SQLModsecurityAuditEntryMessage', SQLModsecurityAuditEntryMessage)

class ModsecurityAuditDataSourceSQL(IModsecurityAuditDataSource):
    _DATA_INSERTION_BUFFER_SIZE = 100
    
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
        
        sqlModsecurityAuditEntryMessageBuffer = []
        
        for modsecurityAuditEntry in modsecurityAuditEntryIterable:
            hostName = modsecurityAuditEntry.host_name()
            requestFileName = modsecurityAuditEntry.request_file_name()
            for message in modsecurityAuditEntry.message_list():
                sqlMessage = SQLModsecurityAuditEntryMessage()
                sqlMessage.host_name = hostName
                sqlMessage.request_file_name = requestFileName
                sqlMessage.payload_container = message.payload_container()
                sqlMessage.rule_id = message.rule_id()
                
                # Insert message.
                self._insertModsecurityAuditEntryMessage(sqlModsecurityAuditEntryMessageBuffer, sqlMessage)
        
        self._flushModsecurityAuditEntryMessageBuffer(sqlModsecurityAuditEntryMessageBuffer)

    @contract
    def itemDictIterable(self, variableNameList):
        """
    :type variableNameList: list(str)
"""
        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker, variableNameList)

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
        sqlModsecurityAuditEntryMessageBuffer.append(sqlModsecurityAuditEntryMessage)

        if len(sqlModsecurityAuditEntryMessageBuffer) >= self._DATA_INSERTION_BUFFER_SIZE:
            self._flushModsecurityAuditEntryMessageBuffer(sqlModsecurityAuditEntryMessageBuffer)

    @contract
    def _flushModsecurityAuditEntryMessageBuffer(self, sqlModsecurityAuditEntryMessageBuffer):
        """
    :type sqlModsecurityAuditEntryMessageBuffer: list(SQLModsecurityAuditEntryMessage)
"""
        with closing(self._sessionMaker()) as session:
            session.add_all(sqlModsecurityAuditEntryMessageBuffer)
            session.commit()
        del sqlModsecurityAuditEntryMessageBuffer[:]
