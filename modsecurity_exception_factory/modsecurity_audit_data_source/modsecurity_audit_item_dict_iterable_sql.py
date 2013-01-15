#-*- coding: utf-8 -*-
#
# Created on Jan 15, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract, new_contract
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_modsecurity_audit_entry_message import \
    SQLModsecurityAuditEntryMessage
from sqlalchemy.orm.session import sessionmaker

new_contract('sessionmaker', sessionmaker)

class ModsecurityAuditItemDictIterableSQL:

    @contract
    def __init__(self, sessionMaker, variableNameList):
        """
    :type sessionMaker: sessionmaker
    :type variableNameList: list(str)
"""
        self._sessionMaker = sessionMaker
        self._variableNameList = variableNameList
        
    def __iter__(self):
        return _ModsecurityAuditItemDictIteratorSQL(self._generator())

    def __len__(self):
        try:
            session = self._sessionMaker()
            return self._query(session).count()
        finally:
            session.close()

    def _generator(self):
        try:
            session = self._sessionMaker()
            for sqlItem in self._query(session):
                itemDict = {}
                for variableName in self._variableNameList:
                    itemDict[variableName] = getattr(sqlItem, variableName)
                yield itemDict
        finally:
            session.close()
    
    def _query(self, session):
        return session.query(SQLModsecurityAuditEntryMessage)

class _ModsecurityAuditItemDictIteratorSQL:

    def __init__(self, generator):
        self._generator = generator

    def __iter__(self):
        return self

    def next(self):
        return self._generator.next()
