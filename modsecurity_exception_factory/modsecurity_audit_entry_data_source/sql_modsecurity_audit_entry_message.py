#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from modsecurity_exception_factory.modsecurity_audit_entry_data_source.sql_base import SQLBase
from sqlalchemy import Column, Integer, String

class SQLModsecurityAuditEntryMessage(SQLBase):
    __tablename__ = 'messages'
    
    index = Column(Integer, primary_key=True)
    hostName = Column(String)
    requestFileName = Column(String)
    payloadContainer = Column(String)
    ruleId = Column(String)
