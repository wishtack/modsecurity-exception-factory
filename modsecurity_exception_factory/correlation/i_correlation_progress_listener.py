#-*- coding: utf-8 -*-
#
# Created on Feb 15, 2013
#
# @author: rm4dillo
#
# $Id$
#

from abc import abstractmethod

class ICorrelationProgressListener:

    @abstractmethod
    def progress(self, correlatedCount, totalCount):
        raise NotImplementedError()
