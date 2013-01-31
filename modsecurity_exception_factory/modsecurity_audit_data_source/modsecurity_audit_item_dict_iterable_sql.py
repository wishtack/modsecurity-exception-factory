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
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_filter import \
    SQLFilter
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_filter_variable import \
    SQLFilterVariable
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_modsecurity_audit_entry_message import \
    SQLModsecurityAuditEntryMessage
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import union, literal, desc, not_, and_
from sqlalchemy.sql.functions import count
from synthetic.decorators import synthesizeMember, synthesizeConstructor

new_contract('sessionmaker', sessionmaker)
new_contract('SQLFilterVariable', SQLFilterVariable)

class EmptyVariableNameListError(Exception):
    def __init__(self):
        super(EmptyVariableNameListError, self).__init__(u"Variable name list can't be empty.")

class ModsecurityAuditItemDictIterableSQL(IItemIterable):
    
    _VARIABLE_NAME_KEY = 'variableName'
    _VARIABLE_VALUE_KEY = 'variableValue'
    _VARIABLE_VALUE_COUNT_KEY = 'variableValueCountKey'

    @contract
    def __init__(self, sessionMaker, variableNameList, distinct = False, sqlFilterVariableList = None):
        """
    :type sessionMaker: sessionmaker
    :type variableNameList: list(str)
    :type distinct: bool
    :type sqlFilterVariableList: list(SQLFilterVariable)|None
"""
        self._sessionMaker = sessionMaker
        self._variableNameList = variableNameList
        self._distinct = distinct
        self._sqlFilterVariableList = sqlFilterVariableList
        self._queryFilter = None

    def __iter__(self):
        return _ModsecurityAuditItemDictIteratorSQL(self._generator())

    def __len__(self):
        with self._sessionMaker() as session:
            return self._makeQuery(session).count()
    
    def distinct(self):
        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker,
                                                   self._variableNameList,
                                                   distinct = True,
                                                   sqlFilterVariableList = self._sqlFilterVariableList)

    @contract
    def filterByVariable(self, variableName, variableValue, negate = False):
        """
    :type variableName: str
    :type variableValue: unicode
    :type negate: bool
"""

        # Adding variable to filter's variable list.
        sqlVariable = SQLFilterVariable(name = variableName,
                                        value = variableValue,
                                        negate = negate)
        
        sqlFilterVariableList =  [sqlVariable]
        if self._sqlFilterVariableList is not None:
            sqlFilterVariableList += self._sqlFilterVariableList
        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker,
                                                   self._variableNameList,
                                                   distinct = self._distinct,
                                                   sqlFilterVariableList = sqlFilterVariableList)

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
                # @hack: converting to unicode because the value might be None.
                # @todo: manage None values.
                return {str(item.variableName): unicode(item.variableValue)}
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
        query = self._applyFilter(query)
            
        # Only 'select' distinct values if asked for.
        if self._distinct:
            query = query.distinct()

        return query

    def _applyFilter(self, query):
        queryFilter = self._makeQueryFilter()
        if queryFilter is not None:
            query = query.filter(queryFilter)
        return query

    def _makeQueryFilter(self):
        # Query filter has already been generated.
        if self._queryFilter is not None:
            return self._queryFilter
        
        # There's no filter to apply.
        if self._sqlFilterVariableList is None:
            return None
        
        queryFilterList = []
        
        with self._sessionMaker() as session:
            # Now we store the filter and it's variables in the database before using them through sub queries.
            sqlFilter = SQLFilter(variableList = self._sqlFilterVariableList)
            session.add(sqlFilter)
            session.commit()

            # Group filter variables by name and 'negate' information.
            for sqlFilterVariableGroup in session.query(SQLFilterVariable)\
                                                 .with_parent(sqlFilter)\
                                                 .group_by(SQLFilterVariable.name, SQLFilterVariable.negate):
                variableName = sqlFilterVariableGroup.name
                variable = getattr(SQLModsecurityAuditEntryMessage, variableName)
                negate = sqlFilterVariableGroup.negate

                # Crawling group items.
                sqlFilterVariableValueIterable = session.query(SQLFilterVariable.value)\
                                                   .with_parent(sqlFilter)\
                                                   .filter(SQLFilterVariable.name == variableName,
                                                           SQLFilterVariable.negate == negate)

                # If it's a negation, we create one 'NOT IN' query filter for all values.
                if negate:
                    queryFilterList.append(not_(variable.in_(sqlFilterVariableValueIterable)))

                # We create a filter for each value if it's an equality condition.
                else:
                    for variableValueKeyedTuple in sqlFilterVariableValueIterable:
                        queryFilterList.append(variable == variableValueKeyedTuple.value)
        
        self._queryFilter = and_(*queryFilterList)
        return self._queryFilter
    
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

    def variableValueIterable(self):
        for filterObject in self._selfAndChildrenIterable():
            yield filterObject.variableValue()

    def _selfAndChildrenIterable(self):
        filterObject = self
        while filterObject is not None:
            yield filterObject
            filterObject = filterObject.childFilter()
