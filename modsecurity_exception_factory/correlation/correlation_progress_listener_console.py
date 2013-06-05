#-*- coding: utf-8 -*-
#
# Created on Feb 15, 2013
#
# @author: rm4dillo
#
# $Id$
#

from .i_correlation_progress_listener import ICorrelationProgressListener
from contracts import contract
from synthetic import synthesizeConstructor, synthesizeMember

@synthesizeMember('stream')
@synthesizeConstructor()
class CorrelationProgressListenerConsole(ICorrelationProgressListener):

    @contract
    def progress(self, count, totalCount):
        """
    :type count: int
    :type totalCount: int
"""
        percentage = 0
        if totalCount > 0:
            percentage = 100 * float(count) / totalCount
        self._stream.write(u"\r%6.2f%% (%d/%d)" % (percentage, count, totalCount))
        self._stream.flush()
