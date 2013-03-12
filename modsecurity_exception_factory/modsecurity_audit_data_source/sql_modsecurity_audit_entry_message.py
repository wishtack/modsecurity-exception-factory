#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from modsecurity_exception_factory.modsecurity_audit_data_source.sql_base import SQLBase
from sqlalchemy import Column, Integer, String

class SQLModsecurityAuditEntryMessage(SQLBase):
    __tablename__ = 'messages'
    
    index = Column(Integer, primary_key = True)
    hostName = Column(String, index = True)
    requestFileName = Column(String, index = True)
    payloadContainer = Column(String, index = True)
    ruleId = Column(String, index = True)
