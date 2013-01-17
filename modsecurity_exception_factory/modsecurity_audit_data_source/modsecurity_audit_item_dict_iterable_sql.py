#-*- coding: utf-8 -*-
#
# Created on Jan 15, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract, new_contract
from modsecurity_exception_factory.correlation.i_item_iterable import \
    IItemIterable
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_modsecurity_audit_entry_message import \
    SQLModsecurityAuditEntryMessage
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import union, label, literal, desc, select
from sqlalchemy.sql.functions import count

new_contract('sessionmaker', sessionmaker)

class ModsecurityAuditItemDictIterableSQL(IItemIterable):
    
    _VARIABLE_NAME_KEY = 'variableName'
    _VARIABLE_VALUE_KEY = 'variableValue'
    _VARIABLE_VALUE_COUNT_KEY = 'variableValueCountKey'

    @contract
    def __init__(self, sessionMaker, variableNameList, distinct = False):
        """
    :type sessionMaker: sessionmaker
    :type variableNameList: list(str)
    :type distinct: bool
"""
        self._sessionMaker = sessionMaker
        self._variableNameList = variableNameList
        self._distinct = distinct
        
    def __iter__(self):
        return _ModsecurityAuditItemDictIteratorSQL(self._generator())

    def __len__(self):
        query = self._queryAll().count()
        return self._executeAndCloseFetchOne(query).tbl_row_count
    
    def distinct(self):
        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker,
                                                   self._variableNameList,
                                                   distinct = True)

    def mostFrequentVariableAndValue(self):
        queryList = []
        
        # For each variable, retrieve all possible values and their occurrence count.
        for variableName in self._variableNameList:
            variableNameColumn = literal(variableName).label(self._VARIABLE_NAME_KEY)
            variableValueColumn = getattr(SQLModsecurityAuditEntryMessage, variableName).label(self._VARIABLE_VALUE_KEY)
            variableValueCountColumn = count().label(self._VARIABLE_VALUE_COUNT_KEY)
            
            # Subquery of each variable.
            query = select([variableNameColumn, variableValueColumn, variableValueCountColumn],
                           from_obj = self._queryAll()).group_by(self._VARIABLE_NAME_KEY, self._VARIABLE_VALUE_KEY)

            queryList.append(query)

        # Merging all subqueries and sorting by reverse count...
        query = union(*queryList).order_by(desc(self._VARIABLE_VALUE_COUNT_KEY))
        
        # ... then picking the first one.
        item = self._executeAndCloseFetchOne(query)
        
        if item is not None:
            return {self._VARIABLE_NAME_KEY: item.variableName, self._VARIABLE_VALUE_KEY: item.variableValue}
        else:
            return None

    def _generator(self):
        for item in self._executeAndCloseIterable(self._queryAll()):
            itemDict = {}
            for variableName in self._variableNameList:
                itemDict[variableName] = getattr(item, variableName)
            yield itemDict
    
    def _queryAll(self):
        criterionList = self._variableNameListAsCriterionList()
        query = select(criterionList)

        if self._distinct:
            query = query.distinct()

        return query
    
    def _variableNameListAsCriterionList(self):
        criterionList = []
        for variableName in self._variableNameList:
            criterionList.append(getattr(SQLModsecurityAuditEntryMessage, variableName))
        return criterionList

    def _executeAndCloseFetchOne(self, query):
        session = self._sessionMaker()
        try:
            return session.execute(query).fetchone()
        finally:
            session.close()

    def _executeAndCloseIterable(self, query):
        session = self._sessionMaker()
        try:
            for item in session.execute(query):
                yield item
        finally:
            session.close()

class _ModsecurityAuditItemDictIteratorSQL:

    def __init__(self, generator):
        self._generator = generator

    def __iter__(self):
        return self

    def next(self):
        return self._generator.next()
