#-*- coding: utf-8 -*-
#
# Created on Jan 30, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from modsecurity_exception_factory.modsecurity_audit_data_source.sql_base import \
    SQLBase
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Boolean

class SQLFilterVariable(SQLBase):
    __tablename__ = 'filter_variable'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, index = True)
    value = Column(String, index = True)
    negate = Column(Boolean, index = True)
