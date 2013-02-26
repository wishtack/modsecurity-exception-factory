##-*- coding: utf-8 -*-
##
## Created on Jan 19, 2013
##
## @author: Younes JAAIDI
##
## $Id$
##
#
#from sqlalchemy.orm.session import sessionmaker
#
#class WrapperForWithStatement:
#    """This class makes it easy to use any object with python's 'with' statement."""
#    def __init__(self, instance, enterMethod = None, exitMethod = None):
#        self._instance = instance
#        self._enterMethod = enterMethod
#        self._exitMethod = exitMethod
#    
#    def __enter__(self):
#        if self._enterMethod is not None:
#            self._enterMethod(self._instance)
#        return self._instance
#    
#    def __exit__(self, exceptionType, exceptionValue, traceback):
#        if self._exitMethod is not None:
#            self._exitMethod(self._instance)
#
#class SQLSessionMakerForWithStatement(sessionmaker):
#    def __call__(self, *args, **kwargs):
#        session = super(SQLSessionMakerForWithStatement, self).__call__(*args, **kwargs)
#        return WrapperForWithStatement(session, exitMethod = session.close.__func__)
