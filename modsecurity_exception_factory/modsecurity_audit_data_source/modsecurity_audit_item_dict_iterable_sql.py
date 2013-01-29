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
from sqlalchemy.sql.expression import union, literal, desc
from sqlalchemy.sql.functions import count
from synthetic.decorators import synthesizeMember, synthesizeConstructor
import copy

new_contract('sessionmaker', sessionmaker)

class EmptyVariableNameListError(Exception):
    def __init__(self):
        super(EmptyVariableNameListError, self).__init__(u"Variable name list can't be empty.")

class ModsecurityAuditItemDictIterableSQL(IItemIterable):
    
    _VARIABLE_NAME_KEY = 'variableName'
    _VARIABLE_VALUE_KEY = 'variableValue'
    _VARIABLE_VALUE_COUNT_KEY = 'variableValueCountKey'

    @contract
    def __init__(self, sessionMaker, variableNameList, distinct = False, filterDict = None):
        """
    :type sessionMaker: sessionmaker
    :type variableNameList: list(str)
    :type distinct: bool
    :type filterDict: dict|None
"""
        if filterDict is None:
            filterDict = {}

        self._sessionMaker = sessionMaker
        self._variableNameList = variableNameList
        self._distinct = distinct
        self._filterDict = filterDict

    def __iter__(self):
        return _ModsecurityAuditItemDictIteratorSQL(self._generator())

    def __len__(self):
        with self._sessionMaker() as session:
            return self._makeQuery(session).count()
    
    def distinct(self):
        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker,
                                                   self._variableNameList,
                                                   distinct = True,
                                                   filterDict = self._filterDict)

    @contract
    def filterByVariable(self, variableName, variableValue, negate = False):
        """
    :type variableName: str
    :type variableValue: unicode
    :type negate: bool
"""
        filterDict = copy.copy(self._filterDict)

        key = (variableName, negate)
        filterDict[key] = _Filter(variableName = variableName,
                                  variableValue = variableValue,
                                  childFilter = filterDict.get(key, None),
                                  negate = negate)

        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker,
                                                   self._variableNameList,
                                                   distinct = self._distinct,
                                                   filterDict = filterDict)

    @contract
    def mostFrequentVariableAndValue(self, variableNameList):
        """
    :type variableNameList: list(str)
"""
        subQueryList = []
        
        if len(variableNameList) == 0:
            raise EmptyVariableNameListError()

        with self._sessionMaker() as session:
            # For each variable, retrieve all possible values and their occurrence count.
            for variableName in variableNameList:
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
                return {str(item.variableName): item.variableValue}
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
        for filterObject in self._filterDict.values():
            sqlFilter = self._filterObjectToSQL(filterObject)
            
            # Apply filter.
            query = query.filter(sqlFilter)
            
        # Only 'select' distinct values if asked for.
        if self._distinct:
            query = query.distinct()

        return query
    
    def _filterObjectToSQL(self, filterObject):
        variableName = filterObject.variableName()
        variableValueRegexString = filterObject.variableValueRegexString()
        negate = filterObject.negate()
        
        # Make the 'in' filter...
        variable = getattr(SQLModsecurityAuditEntryMessage, variableName)
        sqlFilter = variable.op('REGEXP')(variableValueRegexString)

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

@synthesizeMember('variableName', contract = str)
@synthesizeMember('variableValue', contract = 'unicode')
@synthesizeMember('childFilter')
@synthesizeMember('negate', contract = bool, defaultValue = False)
@synthesizeConstructor()
class _Filter:

    def variableValueRegexString(self):
        variableValueList = []
        filterObject = self
        while filterObject is not None:
            variableValueList.append(filterObject.variableValue())
            filterObject = filterObject.childFilter()
        return u"|".join(variableValueList)
        
