#-*- coding: utf-8 -*-
#
# Created on Jan 4, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from mock import Mock, call
from modsecurity_exception_factory.correlation.correlation_engine import \
    CorrelationEngine
from modsecurity_exception_factory.correlation.i_correlation_progress_listener import \
    ICorrelationProgressListener
from modsecurity_exception_factory.modsecurity_audit_data_source.modsecurity_audit_data_source_sql import \
    ModsecurityAuditDataSourceSQL
from modsecurity_exception_factory.modsecurity_audit_log_parser.modsecurity_audit_log_parser import \
    ModsecurityAuditLogParser
from tests.common import MODSECURITY_AUDIT_LOG_SAMPLE_PATH, cleanUp, \
    MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL
import io
import unittest

class TestModsecurityAuditCorrelationEngine(unittest.TestCase):

    _EXPECTED_CORRELATION_LIST = \
["""hostName (count=656) = 1.1.1.1
        requestFileName (count=651) = /agilefant/ajax/iterationData.action, /agilefant/ajax/myAssignmentsMenuData.action, /agilefant/dailyWork.action, /agilefant/drawIterationBurndown.action, /agilefant/drawSmallIterationBurndown.action, /agilefant/static/css/main.css, /agilefant/static/img/backlog.png, /agilefant/static/img/button_fade.png, /agilefant/static/img/dailyWork.png, /agilefant/static/img/dynatree/ltL_ne.gif, /agilefant/static/img/dynatree/ltL_nes.gif, /agilefant/static/img/dynatree/ltL_ns.gif, /agilefant/static/img/dynatree/ltM_ne.gif, /agilefant/static/img/dynatree/ltM_nes.gif, /agilefant/static/img/dynatree/ltP_ne.gif, /agilefant/static/img/dynatree/ltP_nes.gif, /agilefant/static/img/dynatree/ltWait.gif, /agilefant/static/img/favicon.png, /agilefant/static/img/filter.png, /agilefant/static/img/info.png, /agilefant/static/img/labelIcon.png, /agilefant/static/img/open_close.png, /agilefant/static/img/pleasewait.gif, /agilefant/static/img/portfolio.png, /agilefant/static/img/search_small.png, /agilefant/static/img/settings.png, /agilefant/static/img/sort.png, /agilefant/static/img/team.png, /agilefant/static/img/timesheets.png, /agilefant/static/img/toggle.png, /agilefant/static/img/top-logo.png, /agilefant/static/img/ui/ui-bg_glass_85_dfeffc_1x400.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_333333_500x100.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_f5f8f9_1x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/img/ui/ui-icons_6da8d5_256x240.png, /agilefant/static/img/ui/ui-icons_f9bd01_256x240.png, /agilefant/static/js/autocomplete/autocompleteBundle.js, /agilefant/static/js/autocomplete/autocompleteDataProvider.js, /agilefant/static/js/autocomplete/autocompleteDialog.js, /agilefant/static/js/autocomplete/autocompleteInline.js, /agilefant/static/js/autocomplete/autocompleteRecent.js, /agilefant/static/js/autocomplete/autocompleteSearchBox.js, /agilefant/static/js/autocomplete/autocompleteSelectedBox.js, /agilefant/static/js/autocomplete/autocompleteSingleDialog.js, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/dynamics/Dynamics.events.js, /agilefant/static/js/dynamics/controller/AdministrationMenuController.js, /agilefant/static/js/dynamics/controller/AssignmentController.js, /agilefant/static/js/dynamics/controller/BacklogController.js, /agilefant/static/js/dynamics/controller/CommonController.js, /agilefant/static/js/dynamics/controller/CreateDialog.js, /agilefant/static/js/dynamics/controller/DailyWorkController.js, /agilefant/static/js/dynamics/controller/DailyWorkStoryListController.js, /agilefant/static/js/dynamics/controller/DailyWorkTasksWithoutStoryController.js, /agilefant/static/js/dynamics/controller/HourEntryController.js, /agilefant/static/js/dynamics/controller/HourEntryListController.js, /agilefant/static/js/dynamics/controller/IterationController.js, /agilefant/static/js/dynamics/controller/IterationRowController.js, /agilefant/static/js/dynamics/controller/MenuController.js, /agilefant/static/js/dynamics/controller/MyAssignmentsMenuController.js, /agilefant/static/js/dynamics/controller/PageController.js, /agilefant/static/js/dynamics/controller/PersonalLoadController.js, /agilefant/static/js/dynamics/controller/PortfolioController.js, /agilefant/static/js/dynamics/controller/PortfolioRowController.js, /agilefant/static/js/dynamics/controller/ProductController.js, /agilefant/static/js/dynamics/controller/ProjectController.js, /agilefant/static/js/dynamics/controller/ProjectRowController.js, /agilefant/static/js/dynamics/controller/StoryController.js, /agilefant/static/js/dynamics/controller/StoryInfoBubble.js, /agilefant/static/js/dynamics/controller/StoryListController.js, /agilefant/static/js/dynamics/controller/StoryTreeController.js, /agilefant/static/js/dynamics/controller/TaskController.js, /agilefant/static/js/dynamics/controller/TaskInfoDialog.js, /agilefant/static/js/dynamics/controller/TaskSplitDialog.js, /agilefant/static/js/dynamics/controller/TasksWithoutStoryController.js, /agilefant/static/js/dynamics/controller/TeamListController.js, /agilefant/static/js/dynamics/controller/TeamRowController.js, /agilefant/static/js/dynamics/controller/UserController.js, /agilefant/static/js/dynamics/controller/UserListController.js, /agilefant/static/js/dynamics/controller/UserRowController.js, /agilefant/static/js/dynamics/controller/WorkQueueController.js, /agilefant/static/js/dynamics/model/AssignmentModel.js, /agilefant/static/js/dynamics/model/BacklogModel.js, /agilefant/static/js/dynamics/model/CommonModel.js, /agilefant/static/js/dynamics/model/DailyWorkModel.js, /agilefant/static/js/dynamics/model/HourEntryListContainer.js, /agilefant/static/js/dynamics/model/HourEntryModel.js, /agilefant/static/js/dynamics/model/IterationModel.js, /agilefant/static/js/dynamics/model/LabelModel.js, /agilefant/static/js/dynamics/model/ModelFactory.js, /agilefant/static/js/dynamics/model/PortfolioModel.js, /agilefant/static/js/dynamics/model/ProductModel.js, /agilefant/static/js/dynamics/model/ProjectModel.js, /agilefant/static/js/dynamics/model/StoryModel.js, /agilefant/static/js/dynamics/model/TaskModel.js, /agilefant/static/js/dynamics/model/TaskSplitContainer.js, /agilefant/static/js/dynamics/model/TeamListContainer.js, /agilefant/static/js/dynamics/model/TeamModel.js, /agilefant/static/js/dynamics/model/UserListContainer.js, /agilefant/static/js/dynamics/model/UserModel.js, /agilefant/static/js/dynamics/model/WorkQueueTaskModel.js, /agilefant/static/js/dynamics/model/comparators.js, /agilefant/static/js/dynamics/view/Bubble.js, /agilefant/static/js/dynamics/view/Cell.js, /agilefant/static/js/dynamics/view/ChangePasswordDialog.js, /agilefant/static/js/dynamics/view/CommonFragmentSubView.js, /agilefant/static/js/dynamics/view/CommonSubView.js, /agilefant/static/js/dynamics/view/ConfirmationDialog.js, /agilefant/static/js/dynamics/view/DynamicView.js, /agilefant/static/js/dynamics/view/LazyLoadedDialog.js, /agilefant/static/js/dynamics/view/MessageDisplay.js, /agilefant/static/js/dynamics/view/MultiEditWidget.js, /agilefant/static/js/dynamics/view/Row.js, /agilefant/static/js/dynamics/view/SearchByTextWidget.js, /agilefant/static/js/dynamics/view/SpentEffortWidget.js, /agilefant/static/js/dynamics/view/StateFilterWidget.js, /agilefant/static/js/dynamics/view/StoryFiltersView.js, /agilefant/static/js/dynamics/view/Table.js, /agilefant/static/js/dynamics/view/TableCaption.js, /agilefant/static/js/dynamics/view/TableCellEditors.js, /agilefant/static/js/dynamics/view/TableConfiguration.js, /agilefant/static/js/dynamics/view/UserSpentEffortWidget.js, /agilefant/static/js/dynamics/view/ValidationManager.js, /agilefant/static/js/dynamics/view/ViewPart.js, /agilefant/static/js/dynamics/view/decorators.js, /agilefant/static/js/dynamics/view/subviews/AutoSuggest.js, /agilefant/static/js/dynamics/view/subviews/Button.js, /agilefant/static/js/dynamics/view/subviews/Buttons.js, /agilefant/static/js/dynamics/view/subviews/CellBubble.js, /agilefant/static/js/dynamics/view/subviews/LabelsIcon.js, /agilefant/static/js/dynamics/view/subviews/LabelsView.js, /agilefant/static/js/dynamics/view/subviews/RowActions.js, /agilefant/static/js/dynamics/view/subviews/SplitPanel.js, /agilefant/static/js/dynamics/view/subviews/StoryInfoWidget.js, /agilefant/static/js/dynamics/view/subviews/Tabs.js, /agilefant/static/js/dynamics/view/subviews/Toggle.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.autoSuggest.minified.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.jstree.js, /agilefant/static/js/jquery.labelify.js, /agilefant/static/js/jquery.tagcloud.min.js, /agilefant/static/js/jquery.tooltip.js, /agilefant/static/js/jquery.wysiwyg.js, /agilefant/static/js/utils/ArrayUtils.js, /agilefant/static/js/utils/ClassUtils.js, /agilefant/static/js/utils/HelpUtils.js, /agilefant/static/js/utils/Parsers.js, /agilefant/static/js/utils/XworkSerializer.js, /agilefant/static/js/utils/aef.jstree.plugin.js, /agilefant/static/js/utils/menuTimer.js, /agilefant/static/js/utils/quickSearch.js, /agilefant/static/js/utils/refLinkDisplay.js
                payloadContainer (count=217) = REQUEST_HEADERS:Host
                        ruleId (count=217) = 960017
                payloadContainer (count=217) = TX:anomaly_score
                        ruleId (count=217) = 981174
                payloadContainer (count=217) = TX:inbound_anomaly_score
                        ruleId (count=217) = 981203
        payloadContainer (count=5) = TX:sqli_select_statement_count
                ruleId (count=5) = 981317
                        requestFileName (count=5) = /agilefant/drawIterationBurndown.action, /agilefant/static/img/top-logo.png, /agilefant/static/js/autocomplete/autocompleteSelectedBox.js, /agilefant/static/js/backlogSelector.js
""",
 """hostName (count=59) = test.domain.com
        requestFileName (count=54) = /agilefant/editIteration.action, /agilefant/login.jsp, /agilefant/static/css/main.css, /agilefant/static/img/agilefant-logo-80px.png, /agilefant/static/img/login_gradient.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.wysiwyg.js
                payloadContainer (count=18) = REQUEST_HEADERS:Host
                        ruleId (count=18) = 960017
                payloadContainer (count=18) = TX:anomaly_score
                        ruleId (count=18) = 981174
                payloadContainer (count=18) = TX:inbound_anomaly_score
                        ruleId (count=18) = 981203
        requestFileName (count=4) = /agilefant/login.jsp
                ruleId (count=4) = 111111, 222222
                        payloadContainer (count=4) = ARGS:a, ARGS:b
        payloadContainer (count=1) = TX:sqli_select_statement_count
                requestFileName (count=1) = /agilefant/static/js/backlogSelector.js
                        ruleId (count=1) = 981317
""",
 """hostName (count=8) = None
        requestFileName (count=8) = None, /agilefant/login.jsp
                ruleId (count=8) = 111111, 222222
                        payloadContainer (count=8) = ARGS:a, ARGS:b
"""]

    _EXPECTED_CORRELATION_LIST_WITH_IGNORED_VARIABLE_DICT = \
["""hostName (count=39) = test.domain.com
        requestFileName (count=36) = /agilefant/editIteration.action, /agilefant/login.jsp, /agilefant/static/css/main.css, /agilefant/static/img/agilefant-logo-80px.png, /agilefant/static/img/login_gradient.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.wysiwyg.js
                payloadContainer (count=18) = REQUEST_HEADERS:Host
                        ruleId (count=18) = 960017
                payloadContainer (count=18) = TX:inbound_anomaly_score
                        ruleId (count=18) = 981203
        requestFileName (count=2) = /agilefant/login.jsp
                ruleId (count=2) = 222222
                        payloadContainer (count=2) = ARGS:a, ARGS:b
        payloadContainer (count=1) = TX:sqli_select_statement_count
                requestFileName (count=1) = /agilefant/static/js/backlogSelector.js
                        ruleId (count=1) = 981317
""",
 """hostName (count=4) = None
        ruleId (count=4) = 222222
                requestFileName (count=4) = None, /agilefant/login.jsp
                        payloadContainer (count=4) = ARGS:a, ARGS:b
"""]

    _EXPECTED_CORRELATION_LIST_WITH_MINIMUM_OCCURRENCE_COUNT = \
["""hostName (count=656) = 1.1.1.1
        requestFileName (count=656) = /agilefant/ajax/iterationData.action, /agilefant/ajax/myAssignmentsMenuData.action, /agilefant/dailyWork.action, /agilefant/drawIterationBurndown.action, /agilefant/drawSmallIterationBurndown.action, /agilefant/static/css/main.css, /agilefant/static/img/backlog.png, /agilefant/static/img/button_fade.png, /agilefant/static/img/dailyWork.png, /agilefant/static/img/dynatree/ltL_ne.gif, /agilefant/static/img/dynatree/ltL_nes.gif, /agilefant/static/img/dynatree/ltL_ns.gif, /agilefant/static/img/dynatree/ltM_ne.gif, /agilefant/static/img/dynatree/ltM_nes.gif, /agilefant/static/img/dynatree/ltP_ne.gif, /agilefant/static/img/dynatree/ltP_nes.gif, /agilefant/static/img/dynatree/ltWait.gif, /agilefant/static/img/favicon.png, /agilefant/static/img/filter.png, /agilefant/static/img/info.png, /agilefant/static/img/labelIcon.png, /agilefant/static/img/open_close.png, /agilefant/static/img/pleasewait.gif, /agilefant/static/img/portfolio.png, /agilefant/static/img/search_small.png, /agilefant/static/img/settings.png, /agilefant/static/img/sort.png, /agilefant/static/img/team.png, /agilefant/static/img/timesheets.png, /agilefant/static/img/toggle.png, /agilefant/static/img/top-logo.png, /agilefant/static/img/ui/ui-bg_glass_85_dfeffc_1x400.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_333333_500x100.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_f5f8f9_1x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/img/ui/ui-icons_6da8d5_256x240.png, /agilefant/static/img/ui/ui-icons_f9bd01_256x240.png, /agilefant/static/js/autocomplete/autocompleteBundle.js, /agilefant/static/js/autocomplete/autocompleteDataProvider.js, /agilefant/static/js/autocomplete/autocompleteDialog.js, /agilefant/static/js/autocomplete/autocompleteInline.js, /agilefant/static/js/autocomplete/autocompleteRecent.js, /agilefant/static/js/autocomplete/autocompleteSearchBox.js, /agilefant/static/js/autocomplete/autocompleteSelectedBox.js, /agilefant/static/js/autocomplete/autocompleteSingleDialog.js, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/dynamics/Dynamics.events.js, /agilefant/static/js/dynamics/controller/AdministrationMenuController.js, /agilefant/static/js/dynamics/controller/AssignmentController.js, /agilefant/static/js/dynamics/controller/BacklogController.js, /agilefant/static/js/dynamics/controller/CommonController.js, /agilefant/static/js/dynamics/controller/CreateDialog.js, /agilefant/static/js/dynamics/controller/DailyWorkController.js, /agilefant/static/js/dynamics/controller/DailyWorkStoryListController.js, /agilefant/static/js/dynamics/controller/DailyWorkTasksWithoutStoryController.js, /agilefant/static/js/dynamics/controller/HourEntryController.js, /agilefant/static/js/dynamics/controller/HourEntryListController.js, /agilefant/static/js/dynamics/controller/IterationController.js, /agilefant/static/js/dynamics/controller/IterationRowController.js, /agilefant/static/js/dynamics/controller/MenuController.js, /agilefant/static/js/dynamics/controller/MyAssignmentsMenuController.js, /agilefant/static/js/dynamics/controller/PageController.js, /agilefant/static/js/dynamics/controller/PersonalLoadController.js, /agilefant/static/js/dynamics/controller/PortfolioController.js, /agilefant/static/js/dynamics/controller/PortfolioRowController.js, /agilefant/static/js/dynamics/controller/ProductController.js, /agilefant/static/js/dynamics/controller/ProjectController.js, /agilefant/static/js/dynamics/controller/ProjectRowController.js, /agilefant/static/js/dynamics/controller/StoryController.js, /agilefant/static/js/dynamics/controller/StoryInfoBubble.js, /agilefant/static/js/dynamics/controller/StoryListController.js, /agilefant/static/js/dynamics/controller/StoryTreeController.js, /agilefant/static/js/dynamics/controller/TaskController.js, /agilefant/static/js/dynamics/controller/TaskInfoDialog.js, /agilefant/static/js/dynamics/controller/TaskSplitDialog.js, /agilefant/static/js/dynamics/controller/TasksWithoutStoryController.js, /agilefant/static/js/dynamics/controller/TeamListController.js, /agilefant/static/js/dynamics/controller/TeamRowController.js, /agilefant/static/js/dynamics/controller/UserController.js, /agilefant/static/js/dynamics/controller/UserListController.js, /agilefant/static/js/dynamics/controller/UserRowController.js, /agilefant/static/js/dynamics/controller/WorkQueueController.js, /agilefant/static/js/dynamics/model/AssignmentModel.js, /agilefant/static/js/dynamics/model/BacklogModel.js, /agilefant/static/js/dynamics/model/CommonModel.js, /agilefant/static/js/dynamics/model/DailyWorkModel.js, /agilefant/static/js/dynamics/model/HourEntryListContainer.js, /agilefant/static/js/dynamics/model/HourEntryModel.js, /agilefant/static/js/dynamics/model/IterationModel.js, /agilefant/static/js/dynamics/model/LabelModel.js, /agilefant/static/js/dynamics/model/ModelFactory.js, /agilefant/static/js/dynamics/model/PortfolioModel.js, /agilefant/static/js/dynamics/model/ProductModel.js, /agilefant/static/js/dynamics/model/ProjectModel.js, /agilefant/static/js/dynamics/model/StoryModel.js, /agilefant/static/js/dynamics/model/TaskModel.js, /agilefant/static/js/dynamics/model/TaskSplitContainer.js, /agilefant/static/js/dynamics/model/TeamListContainer.js, /agilefant/static/js/dynamics/model/TeamModel.js, /agilefant/static/js/dynamics/model/UserListContainer.js, /agilefant/static/js/dynamics/model/UserModel.js, /agilefant/static/js/dynamics/model/WorkQueueTaskModel.js, /agilefant/static/js/dynamics/model/comparators.js, /agilefant/static/js/dynamics/view/Bubble.js, /agilefant/static/js/dynamics/view/Cell.js, /agilefant/static/js/dynamics/view/ChangePasswordDialog.js, /agilefant/static/js/dynamics/view/CommonFragmentSubView.js, /agilefant/static/js/dynamics/view/CommonSubView.js, /agilefant/static/js/dynamics/view/ConfirmationDialog.js, /agilefant/static/js/dynamics/view/DynamicView.js, /agilefant/static/js/dynamics/view/LazyLoadedDialog.js, /agilefant/static/js/dynamics/view/MessageDisplay.js, /agilefant/static/js/dynamics/view/MultiEditWidget.js, /agilefant/static/js/dynamics/view/Row.js, /agilefant/static/js/dynamics/view/SearchByTextWidget.js, /agilefant/static/js/dynamics/view/SpentEffortWidget.js, /agilefant/static/js/dynamics/view/StateFilterWidget.js, /agilefant/static/js/dynamics/view/StoryFiltersView.js, /agilefant/static/js/dynamics/view/Table.js, /agilefant/static/js/dynamics/view/TableCaption.js, /agilefant/static/js/dynamics/view/TableCellEditors.js, /agilefant/static/js/dynamics/view/TableConfiguration.js, /agilefant/static/js/dynamics/view/UserSpentEffortWidget.js, /agilefant/static/js/dynamics/view/ValidationManager.js, /agilefant/static/js/dynamics/view/ViewPart.js, /agilefant/static/js/dynamics/view/decorators.js, /agilefant/static/js/dynamics/view/subviews/AutoSuggest.js, /agilefant/static/js/dynamics/view/subviews/Button.js, /agilefant/static/js/dynamics/view/subviews/Buttons.js, /agilefant/static/js/dynamics/view/subviews/CellBubble.js, /agilefant/static/js/dynamics/view/subviews/LabelsIcon.js, /agilefant/static/js/dynamics/view/subviews/LabelsView.js, /agilefant/static/js/dynamics/view/subviews/RowActions.js, /agilefant/static/js/dynamics/view/subviews/SplitPanel.js, /agilefant/static/js/dynamics/view/subviews/StoryInfoWidget.js, /agilefant/static/js/dynamics/view/subviews/Tabs.js, /agilefant/static/js/dynamics/view/subviews/Toggle.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.autoSuggest.minified.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.jstree.js, /agilefant/static/js/jquery.labelify.js, /agilefant/static/js/jquery.tagcloud.min.js, /agilefant/static/js/jquery.tooltip.js, /agilefant/static/js/jquery.wysiwyg.js, /agilefant/static/js/utils/ArrayUtils.js, /agilefant/static/js/utils/ClassUtils.js, /agilefant/static/js/utils/HelpUtils.js, /agilefant/static/js/utils/Parsers.js, /agilefant/static/js/utils/XworkSerializer.js, /agilefant/static/js/utils/aef.jstree.plugin.js, /agilefant/static/js/utils/menuTimer.js, /agilefant/static/js/utils/quickSearch.js, /agilefant/static/js/utils/refLinkDisplay.js
                payloadContainer (count=217) = REQUEST_HEADERS:Host
                        ruleId (count=217) = 960017
                payloadContainer (count=217) = TX:anomaly_score
                        ruleId (count=217) = 981174
                payloadContainer (count=217) = TX:inbound_anomaly_score
                        ruleId (count=217) = 981203
""",
 """hostName (count=59) = test.domain.com
"""]

    _EXPECTED_CORRELATION_LIST_WITH_MAXIMUM_VALUE_COUNT = \
["""hostName (count=656) = 1.1.1.1
        payloadContainer (count=217) = REQUEST_HEADERS:Host
                ruleId (count=217) = 960017
        payloadContainer (count=217) = TX:anomaly_score
                ruleId (count=217) = 981174
        payloadContainer (count=217) = TX:inbound_anomaly_score
                ruleId (count=217) = 981203
        payloadContainer (count=5) = TX:sqli_select_statement_count
                ruleId (count=5) = 981317
                        requestFileName (count=5) = /agilefant/drawIterationBurndown.action, /agilefant/static/img/top-logo.png, /agilefant/static/js/autocomplete/autocompleteSelectedBox.js, /agilefant/static/js/backlogSelector.js
""",
"""hostName (count=59) = test.domain.com
        payloadContainer (count=18) = REQUEST_HEADERS:Host
                ruleId (count=18) = 960017
        payloadContainer (count=18) = TX:anomaly_score
                ruleId (count=18) = 981174
        payloadContainer (count=18) = TX:inbound_anomaly_score
                ruleId (count=18) = 981203
        requestFileName (count=4) = /agilefant/login.jsp
                ruleId (count=4) = 111111, 222222
                        payloadContainer (count=4) = ARGS:a, ARGS:b
        payloadContainer (count=1) = TX:sqli_select_statement_count
                requestFileName (count=1) = /agilefant/static/js/backlogSelector.js
                        ruleId (count=1) = 981317
""",
"""hostName (count=8) = None
        requestFileName (count=8) = None, /agilefant/login.jsp
                ruleId (count=8) = 111111, 222222
                        payloadContainer (count=8) = ARGS:a, ARGS:b
"""]

    _VARIABLE_NAME_LIST = ['hostName', 'requestFileName', 'payloadContainer', 'ruleId']

    def setUp(self):
        cleanUp()
        self._fillupDataSource()
    
    def tearDown(self):
        cleanUp()

    def _fillupDataSource(self):
        # Fillup database.
        with io.open(MODSECURITY_AUDIT_LOG_SAMPLE_PATH, 'rt', errors = 'replace') as stream:
            iterable = ModsecurityAuditLogParser().parseStream(stream)
            dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
            
            dataSource.insertModsecurityAuditEntryIterable(iterable)

    def testCorrelate(self):
        # Fillup database.
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)

        # Making correlation engine.
        correlationEngine = CorrelationEngine(self._VARIABLE_NAME_LIST)
        
        # Testing progress listener.
        progressListener = Mock(ICorrelationProgressListener)
        correlationEngine.addProgressListener(progressListener)

        # Correlating.
        correlationList = map(lambda correlation: repr(correlation), correlationEngine.correlate(dataSource))
        self.assertEqual(self._EXPECTED_CORRELATION_LIST, correlationList)
        
        self.assertEqual([call.progress(217, 723),
                          call.progress(434, 723),
                          call.progress(651, 723),
                          call.progress(656, 723),
                          call.progress(674, 723),
                          call.progress(692, 723),
                          call.progress(710, 723),
                          call.progress(712, 723),
                          call.progress(714, 723),
                          call.progress(715, 723),
                          call.progress(717, 723),
                          call.progress(719, 723),
                          call.progress(721, 723),
                          call.progress(723, 723)],
                         progressListener.mock_calls)

    def testCorrelateWithIgnoredVariableDict(self):
        # Fillup database.
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)
        
        ignoredVariableDict = {'hostName': [u"1.1.1.1"],
                               'ruleId': [u"111111", u"981174"]}
        
        correlationEngine = CorrelationEngine(self._VARIABLE_NAME_LIST, ignoredVariableDict)
        correlationList = map(lambda correlation: repr(correlation), correlationEngine.correlate(dataSource))
        self.assertEqual(self._EXPECTED_CORRELATION_LIST_WITH_IGNORED_VARIABLE_DICT, correlationList)

    def testCorrelationWithMinimumOccurrenceCount(self):
        # Fillup database.
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)

        correlationEngine = CorrelationEngine(self._VARIABLE_NAME_LIST,
                                              minimumOccurrenceCountThreshold = 20)
        correlationList = map(lambda correlation: repr(correlation), correlationEngine.correlate(dataSource))
        self.assertEqual(self._EXPECTED_CORRELATION_LIST_WITH_MINIMUM_OCCURRENCE_COUNT, correlationList)

    def testCorrelationWithMaximumValueCount(self):
        # Fillup database.
        dataSource = ModsecurityAuditDataSourceSQL(MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL)

        correlationEngine = CorrelationEngine(self._VARIABLE_NAME_LIST,
                                              maximumValueCountThreshold = 5)
        correlationList = map(lambda correlation: repr(correlation), correlationEngine.correlate(dataSource))
        self.assertEqual(self._EXPECTED_CORRELATION_LIST_WITH_MAXIMUM_VALUE_COUNT, correlationList)
