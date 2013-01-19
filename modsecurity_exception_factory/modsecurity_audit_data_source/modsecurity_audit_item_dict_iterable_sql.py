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
from sqlalchemy.sql.expression import union, literal, desc, select, and_
from sqlalchemy.sql.functions import count
from synthetic.decorators import synthesizeMember, synthesizeConstructor

new_contract('sessionmaker', sessionmaker)

class EmptyVariableNameListError(Exception):
    def __init__(self):
        super(EmptyVariableNameListError, self).__init__(u"Variable name list can't be empty.")

class ModsecurityAuditItemDictIterableSQL(IItemIterable):
    
    _VARIABLE_NAME_KEY = 'variableName'
    _VARIABLE_VALUE_KEY = 'variableValue'
    _VARIABLE_VALUE_COUNT_KEY = 'variableValueCountKey'

    @contract
    def __init__(self, sessionMaker, variableNameList, distinct = False, filterList = None):
        """
    :type sessionMaker: sessionmaker
    :type variableNameList: list(str)
    :type distinct: bool
"""
        if filterList is None:
            filterList = []

        self._sessionMaker = sessionMaker
        self._variableNameList = variableNameList
        self._distinct = distinct
        self._filterList = filterList

    def __iter__(self):
        return _ModsecurityAuditItemDictIteratorSQL(self._generator())

    def __len__(self):
        with self._sessionMaker() as session:
            return self._makeQuery(session).count()
    
    def distinct(self):
        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker,
                                                   self._variableNameList,
                                                   distinct = True,
                                                   filterList = self._filterList)

    @contract
    def filter(self, conditionDict, negate = False):
        """
    :type conditionDict: dict(str: list(unicode))
""" 
        filterObject = _Filter(conditionDict, negate)
        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker,
                                                   self._variableNameList,
                                                   distinct = self._distinct,
                                                   filterList = self._filterList + [filterObject])

    def mostFrequentVariableAndValue(self):
        subQueryList = []
        
        if len(self._variableNameList) == 0:
            raise EmptyVariableNameListError()

        with self._sessionMaker() as session:
            # For each variable, retrieve all possible values and their occurrence count.
            for variableName in self._variableNameList:
                variableNameColumn = literal(variableName).label(self._VARIABLE_NAME_KEY)
                variableValueColumn = getattr(SQLModsecurityAuditEntryMessage, variableName).label(self._VARIABLE_VALUE_KEY)
                variableValueCountColumn = count().label(self._VARIABLE_VALUE_COUNT_KEY)
                
                # Subquery of each variable.
                subQuery = self._makeQuery(session, [variableNameColumn, variableValueColumn, variableValueCountColumn])
                subQuery = subQuery.group_by(self._VARIABLE_NAME_KEY, self._VARIABLE_VALUE_KEY) 
                subQueryList.append(subQuery)
    
            # Merging all subqueries and sorting by reverse count...
            query = union(*subQueryList).order_by(desc(self._VARIABLE_VALUE_COUNT_KEY)).limit(1)
            query = query.order_by(desc(self._VARIABLE_VALUE_COUNT_KEY)).limit(1)
            
            # ... then picking the first one.
            item = session.execute(query).fetchone()
            
            if item is not None:
                return {self._VARIABLE_NAME_KEY: item.variableName, self._VARIABLE_VALUE_KEY: item.variableValue}
            else:
                return None

    def _generator(self):
        with self._sessionMaker() as session:
            for item in self._makeQuery(session):
                itemDict = {}
                for variableName in self._variableNameList:
                    itemDict[variableName] = getattr(item, variableName)
                yield itemDict
    
    def _makeQuery(self, session, criterionList = None):
        # Make 'select' query with all variables.
        if criterionList is None:
            criterionList = self._variableNameListAsCriterionList()

        query = session.query(*criterionList)
        
        # Add filters to the query.
        for filterObject in self._filterList:
            sqlFilter = self._filterObjectToSQL(filterObject)
            
            # Apply filter.
            query = query.filter(sqlFilter)
            
        # Only 'select' distinct values if asked for.
        if self._distinct:
            query = query.distinct()

        return query
    
    def _filterObjectToSQL(self, filterObject):
        conditionDict = filterObject.conditionDict()
        negate = filterObject.negate()
        
        # Retrieve accepted or rejected values for each variable...
        sqlSubFilterList = []
        for variableName, variableValueList in conditionDict.items():
            # ... make the 'in' filter...
            variable = getattr(SQLModsecurityAuditEntryMessage, variableName)
            sqlSubFilter = variable.in_(variableValueList)
            sqlSubFilterList.append(sqlSubFilter)

        # ... merge all sub filers ...
        sqlFilter = and_(*sqlSubFilterList)

        # ... reverse it if needed.
        if negate:
            sqlFilter = ~sqlFilter
        
        return sqlFilter
    
    def _variableNameListAsCriterionList(self):
        criterionList = []
        for variableName in self._variableNameList:
            criterionList.append(getattr(SQLModsecurityAuditEntryMessage, variableName))
        return criterionList

class _ModsecurityAuditItemDictIteratorSQL:

    def __init__(self, generator):
        self._generator = generator

    def __iter__(self):
        return self

    def next(self):
        return self._generator.next()

@synthesizeMember('conditionDict', contract = 'dict(str: list(unicode))')
@synthesizeMember('negate', contract = bool, defaultValue = False)
@synthesizeConstructor()
class _Filter:
    pass

