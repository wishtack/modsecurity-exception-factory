#-*- coding: utf-8 -*-
#
# Created on Jan 30, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from modsecurity_exception_factory.modsecurity_audit_data_source.sql_base import \
    SQLBase
from modsecurity_exception_factory.modsecurity_audit_data_source.sql_filter_condition import \
    SQLFilterCondition
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table, ForeignKey

SQLFilterFilterVariableAssociationTable = Table('filter_filter_condition_association',
                                                SQLBase.metadata,
                                                Column('filter_id', Integer, ForeignKey('filter.id')),
                                                Column('filter_condition_id', Integer, ForeignKey('filter_condition.id'))
                                                )

class SQLFilter(SQLBase):
    __tablename__ = 'filter'
    
    id = Column(Integer, primary_key = True)
    conditionList = relationship(SQLFilterCondition,
                                 secondary = SQLFilterFilterVariableAssociationTable)
