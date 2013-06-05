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
    host_name = Column(String, index = True)
    request_file_name = Column(String, index = True)
    payload_container = Column(String, index = True)
    rule_id = Column(String, index = True)
