#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

import os

def testFilePath(relativePath):
    return os.path.join(os.path.dirname(__file__), relativePath)

MODSECURITY_AUDIT_LOG_SAMPLE_PATH = testFilePath(u"data/modsec_audit.log")
MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH = testFilePath(u"tmp/modsecurity_audit_entry.db")
MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL = "sqlite:///%s" % MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH

def cleanUp():
    if os.path.exists(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH):
        os.remove(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_FILE_PATH)