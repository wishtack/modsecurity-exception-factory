#-*- coding: utf-8 -*-
#
# Created on Jan 15, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract, new_contract
from modsecurity_exception_factory.correlation.i_item_iterable import \
    IItemIterable
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_filter import \
    SQLFilter
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_filter_condition import \
    SQLFilterCondition
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_modsecurity_audit_entry_message import \
    SQLModsecurityAuditEntryMessage
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import union, literal, desc, not_, and_, or_
from sqlalchemy.sql.functions import count
from synthetic.decorators import synthesizeMember, synthesizeConstructor
import copy

new_contract('sessionmaker', sessionmaker)
new_contract('SQLFilterCondition', SQLFilterCondition)

class EmptyVariableNameListError(Exception):
    def __init__(self):
        super(EmptyVariableNameListError, self).__init__(u"Variable name list can't be empty.")

class ModsecurityAuditItemDictIterableSQL(IItemIterable):
    
    _VARIABLE_NAME_KEY = 'variableName'
    _VARIABLE_VALUE_KEY = 'variableValue'
    _VARIABLE_VALUE_COUNT_KEY = 'variableValueCountKey'

    @contract
    def __init__(self, sessionMaker, variableNameList, distinct = False, sqlFilterConditionListDict = None):
        """
    :type sessionMaker: sessionmaker
    :type variableNameList: list(str)
    :type distinct: bool
    :type sqlFilterConditionListDict: dict(tuple:list(SQLFilterCondition))|None
"""

        if sqlFilterConditionListDict is None:
            sqlFilterConditionListDict = {}
        
        self._sessionMaker = sessionMaker
        self._variableNameList = variableNameList
        self._distinct = distinct
        self._sqlFilterConditionListDict = sqlFilterConditionListDict
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
                                                   sqlFilterConditionListDict = self._sqlFilterConditionListDict)

    @contract
    def filterByVariable(self, variableName, variableValue, negate = False):
        """
    :type variableName: str
    :type variableValue: unicode|None
    :type negate: bool
"""

        # Adding variable to filter's variable list.
        sqlFilterCondition = SQLFilterCondition(variableName = variableName,
                                                variableValue = variableValue,
                                                negate = negate)
        
        # Cloning dict.        
        sqlFilterConditionListDict = {}
        for key, conditionList in self._sqlFilterConditionListDict.items():
            sqlFilterConditionListDict[key] = copy.copy(conditionList)

        # Adding item in new dict.            
        key = (variableName, negate)
        if key not in sqlFilterConditionListDict:
            sqlFilterConditionListDict[key] = []
        sqlFilterConditionListDict[key].append(sqlFilterCondition)
        
        return ModsecurityAuditItemDictIterableSQL(self._sessionMaker,
                                                   self._variableNameList,
                                                   distinct = self._distinct,
                                                   sqlFilterConditionListDict = sqlFilterConditionListDict)

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
        if self._sqlFilterConditionListDict is None:
            return None
        
        queryFilterList = []
        
        for key, sqlFilterConditionList in self._sqlFilterConditionListDict.items():
            variableName, negate = key
            variable = getattr(SQLModsecurityAuditEntryMessage, variableName)

            # If it's a negation, we create one 'NOT IN' query filter for all values.
            if negate:
                with self._sessionMaker() as session:
                    # Now we store the filter and it's variables in the database before using them through sub queries.
                    sqlFilterObject = SQLFilter(conditionList = sqlFilterConditionList)
                    session.add(sqlFilterObject)
                    session.commit()
    
                    # Crawling group items.
                    
                    # @hack: why is this line necessary ?
                    sqlFilterObject = session.query(SQLFilter).filter(SQLFilter.id == sqlFilterObject.id).one()
                    
                    # Making a 'NOT IN' filter with not null values.
                    sqlFilterVariableValueIterable = session.query(SQLFilterCondition.variableValue)\
                                                            .with_parent(sqlFilterObject)\
                                                            .filter(SQLFilterCondition.variableValue != None)
                    queryFilter = not_(variable.in_(sqlFilterVariableValueIterable))
                    
                    # @hack: managing NULL values as they are ignored by 'IN' and 'NOT IN'.
                    # Making a 'IS NOT NULL' filter if there's a null value.
                    if session.query(SQLFilterCondition.variableValue)\
                              .with_parent(sqlFilterObject)\
                              .filter(SQLFilterCondition.variableValue == None)\
                              .count() > 0:
                        queryFilter = and_(queryFilter, variable != None)
                    else:
                        queryFilter = or_(queryFilter, variable == None)
                    queryFilterList.append(queryFilter)
                    

            # We create a filter for each value if it's an equality condition.
            else:
                for sqlFilterCondition in sqlFilterConditionList:
                    queryFilterList.append(variable == sqlFilterCondition.variableValue)

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
@synthesizeMember('negate', default = False, contract = bool)
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
