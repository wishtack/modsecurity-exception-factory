#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

MODSECURITY_AUDIT_LOG_SAMPLE_PATH = u"data/modsec_audit.log"
MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH = u"tmp/modsecurity_audit_entry.db"
MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL = "sqlite:///%s" % MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH
