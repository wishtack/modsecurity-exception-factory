#-*- coding: utf-8 -*-
#
# Created on Jan 24, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from StringIO import StringIO
from mock import call, patch
from modsecurity_exception_factory.commands.command_modsecurity_exception_factory import \
    CommandModsecurityExceptionFactory
from modsecurity_exception_factory.correlation.correlation_engine import \
    CorrelationEngine
from sqlalchemy.exc import OperationalError
from tests.common import cleanUp, MODSECURITY_AUDIT_LOG_SAMPLE_PATH, \
    MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL, testFilePath
import sys
import unittest

class TestCommandModsecurityExceptionFactory(unittest.TestCase):

    _TEST_CONFIG_FILE_PATH = testFilePath(u"data/test_command_modsecurity_exception_factory.yaml")

    _EXPECTED_OUTPUT = """\
host_name (count=656) = 1.1.1.1
        request_file_name (count=651) = /agilefant/ajax/iterationData.action, /agilefant/ajax/myAssignmentsMenuData.action, /agilefant/dailyWork.action, /agilefant/drawIterationBurndown.action, /agilefant/drawSmallIterationBurndown.action, /agilefant/static/css/main.css, /agilefant/static/img/backlog.png, /agilefant/static/img/button_fade.png, /agilefant/static/img/dailyWork.png, /agilefant/static/img/dynatree/ltL_ne.gif, /agilefant/static/img/dynatree/ltL_nes.gif, /agilefant/static/img/dynatree/ltL_ns.gif, /agilefant/static/img/dynatree/ltM_ne.gif, /agilefant/static/img/dynatree/ltM_nes.gif, /agilefant/static/img/dynatree/ltP_ne.gif, /agilefant/static/img/dynatree/ltP_nes.gif, /agilefant/static/img/dynatree/ltWait.gif, /agilefant/static/img/favicon.png, /agilefant/static/img/filter.png, /agilefant/static/img/info.png, /agilefant/static/img/labelIcon.png, /agilefant/static/img/open_close.png, /agilefant/static/img/pleasewait.gif, /agilefant/static/img/portfolio.png, /agilefant/static/img/search_small.png, /agilefant/static/img/settings.png, /agilefant/static/img/sort.png, /agilefant/static/img/team.png, /agilefant/static/img/timesheets.png, /agilefant/static/img/toggle.png, /agilefant/static/img/top-logo.png, /agilefant/static/img/ui/ui-bg_glass_85_dfeffc_1x400.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_333333_500x100.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_f5f8f9_1x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/img/ui/ui-icons_6da8d5_256x240.png, /agilefant/static/img/ui/ui-icons_f9bd01_256x240.png, /agilefant/static/js/autocomplete/autocompleteBundle.js, /agilefant/static/js/autocomplete/autocompleteDataProvider.js, /agilefant/static/js/autocomplete/autocompleteDialog.js, /agilefant/static/js/autocomplete/autocompleteInline.js, /agilefant/static/js/autocomplete/autocompleteRecent.js, /agilefant/static/js/autocomplete/autocompleteSearchBox.js, /agilefant/static/js/autocomplete/autocompleteSelectedBox.js, /agilefant/static/js/autocomplete/autocompleteSingleDialog.js, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/dynamics/Dynamics.events.js, /agilefant/static/js/dynamics/controller/AdministrationMenuController.js, /agilefant/static/js/dynamics/controller/AssignmentController.js, /agilefant/static/js/dynamics/controller/BacklogController.js, /agilefant/static/js/dynamics/controller/CommonController.js, /agilefant/static/js/dynamics/controller/CreateDialog.js, /agilefant/static/js/dynamics/controller/DailyWorkController.js, /agilefant/static/js/dynamics/controller/DailyWorkStoryListController.js, /agilefant/static/js/dynamics/controller/DailyWorkTasksWithoutStoryController.js, /agilefant/static/js/dynamics/controller/HourEntryController.js, /agilefant/static/js/dynamics/controller/HourEntryListController.js, /agilefant/static/js/dynamics/controller/IterationController.js, /agilefant/static/js/dynamics/controller/IterationRowController.js, /agilefant/static/js/dynamics/controller/MenuController.js, /agilefant/static/js/dynamics/controller/MyAssignmentsMenuController.js, /agilefant/static/js/dynamics/controller/PageController.js, /agilefant/static/js/dynamics/controller/PersonalLoadController.js, /agilefant/static/js/dynamics/controller/PortfolioController.js, /agilefant/static/js/dynamics/controller/PortfolioRowController.js, /agilefant/static/js/dynamics/controller/ProductController.js, /agilefant/static/js/dynamics/controller/ProjectController.js, /agilefant/static/js/dynamics/controller/ProjectRowController.js, /agilefant/static/js/dynamics/controller/StoryController.js, /agilefant/static/js/dynamics/controller/StoryInfoBubble.js, /agilefant/static/js/dynamics/controller/StoryListController.js, /agilefant/static/js/dynamics/controller/StoryTreeController.js, /agilefant/static/js/dynamics/controller/TaskController.js, /agilefant/static/js/dynamics/controller/TaskInfoDialog.js, /agilefant/static/js/dynamics/controller/TaskSplitDialog.js, /agilefant/static/js/dynamics/controller/TasksWithoutStoryController.js, /agilefant/static/js/dynamics/controller/TeamListController.js, /agilefant/static/js/dynamics/controller/TeamRowController.js, /agilefant/static/js/dynamics/controller/UserController.js, /agilefant/static/js/dynamics/controller/UserListController.js, /agilefant/static/js/dynamics/controller/UserRowController.js, /agilefant/static/js/dynamics/controller/WorkQueueController.js, /agilefant/static/js/dynamics/model/AssignmentModel.js, /agilefant/static/js/dynamics/model/BacklogModel.js, /agilefant/static/js/dynamics/model/CommonModel.js, /agilefant/static/js/dynamics/model/DailyWorkModel.js, /agilefant/static/js/dynamics/model/HourEntryListContainer.js, /agilefant/static/js/dynamics/model/HourEntryModel.js, /agilefant/static/js/dynamics/model/IterationModel.js, /agilefant/static/js/dynamics/model/LabelModel.js, /agilefant/static/js/dynamics/model/ModelFactory.js, /agilefant/static/js/dynamics/model/PortfolioModel.js, /agilefant/static/js/dynamics/model/ProductModel.js, /agilefant/static/js/dynamics/model/ProjectModel.js, /agilefant/static/js/dynamics/model/StoryModel.js, /agilefant/static/js/dynamics/model/TaskModel.js, /agilefant/static/js/dynamics/model/TaskSplitContainer.js, /agilefant/static/js/dynamics/model/TeamListContainer.js, /agilefant/static/js/dynamics/model/TeamModel.js, /agilefant/static/js/dynamics/model/UserListContainer.js, /agilefant/static/js/dynamics/model/UserModel.js, /agilefant/static/js/dynamics/model/WorkQueueTaskModel.js, /agilefant/static/js/dynamics/model/comparators.js, /agilefant/static/js/dynamics/view/Bubble.js, /agilefant/static/js/dynamics/view/Cell.js, /agilefant/static/js/dynamics/view/ChangePasswordDialog.js, /agilefant/static/js/dynamics/view/CommonFragmentSubView.js, /agilefant/static/js/dynamics/view/CommonSubView.js, /agilefant/static/js/dynamics/view/ConfirmationDialog.js, /agilefant/static/js/dynamics/view/DynamicView.js, /agilefant/static/js/dynamics/view/LazyLoadedDialog.js, /agilefant/static/js/dynamics/view/MessageDisplay.js, /agilefant/static/js/dynamics/view/MultiEditWidget.js, /agilefant/static/js/dynamics/view/Row.js, /agilefant/static/js/dynamics/view/SearchByTextWidget.js, /agilefant/static/js/dynamics/view/SpentEffortWidget.js, /agilefant/static/js/dynamics/view/StateFilterWidget.js, /agilefant/static/js/dynamics/view/StoryFiltersView.js, /agilefant/static/js/dynamics/view/Table.js, /agilefant/static/js/dynamics/view/TableCaption.js, /agilefant/static/js/dynamics/view/TableCellEditors.js, /agilefant/static/js/dynamics/view/TableConfiguration.js, /agilefant/static/js/dynamics/view/UserSpentEffortWidget.js, /agilefant/static/js/dynamics/view/ValidationManager.js, /agilefant/static/js/dynamics/view/ViewPart.js, /agilefant/static/js/dynamics/view/decorators.js, /agilefant/static/js/dynamics/view/subviews/AutoSuggest.js, /agilefant/static/js/dynamics/view/subviews/Button.js, /agilefant/static/js/dynamics/view/subviews/Buttons.js, /agilefant/static/js/dynamics/view/subviews/CellBubble.js, /agilefant/static/js/dynamics/view/subviews/LabelsIcon.js, /agilefant/static/js/dynamics/view/subviews/LabelsView.js, /agilefant/static/js/dynamics/view/subviews/RowActions.js, /agilefant/static/js/dynamics/view/subviews/SplitPanel.js, /agilefant/static/js/dynamics/view/subviews/StoryInfoWidget.js, /agilefant/static/js/dynamics/view/subviews/Tabs.js, /agilefant/static/js/dynamics/view/subviews/Toggle.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.autoSuggest.minified.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.jstree.js, /agilefant/static/js/jquery.labelify.js, /agilefant/static/js/jquery.tagcloud.min.js, /agilefant/static/js/jquery.tooltip.js, /agilefant/static/js/jquery.wysiwyg.js, /agilefant/static/js/utils/ArrayUtils.js, /agilefant/static/js/utils/ClassUtils.js, /agilefant/static/js/utils/HelpUtils.js, /agilefant/static/js/utils/Parsers.js, /agilefant/static/js/utils/XworkSerializer.js, /agilefant/static/js/utils/aef.jstree.plugin.js, /agilefant/static/js/utils/menuTimer.js, /agilefant/static/js/utils/quickSearch.js, /agilefant/static/js/utils/refLinkDisplay.js
                payload_container (count=217) = REQUEST_HEADERS:Host
                        rule_id (count=217) = 960017
                payload_container (count=217) = TX:anomaly_score
                        rule_id (count=217) = 981174
                payload_container (count=217) = TX:inbound_anomaly_score
                        rule_id (count=217) = 981203
        payload_container (count=5) = TX:sqli_select_statement_count
                rule_id (count=5) = 981317
                        request_file_name (count=5) = /agilefant/drawIterationBurndown.action, /agilefant/static/img/top-logo.png, /agilefant/static/js/autocomplete/autocompleteSelectedBox.js, /agilefant/static/js/backlogSelector.js

host_name (count=59) = test.domain.com
        request_file_name (count=54) = /agilefant/editIteration.action, /agilefant/login.jsp, /agilefant/static/css/main.css, /agilefant/static/img/agilefant-logo-80px.png, /agilefant/static/img/login_gradient.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.wysiwyg.js
                payload_container (count=18) = REQUEST_HEADERS:Host
                        rule_id (count=18) = 960017
                payload_container (count=18) = TX:anomaly_score
                        rule_id (count=18) = 981174
                payload_container (count=18) = TX:inbound_anomaly_score
                        rule_id (count=18) = 981203
        request_file_name (count=4) = /agilefant/login.jsp
                rule_id (count=4) = 111111, 222222
                        payload_container (count=4) = ARGS:a, ARGS:b
        payload_container (count=1) = TX:sqli_select_statement_count
                request_file_name (count=1) = /agilefant/static/js/backlogSelector.js
                        rule_id (count=1) = 981317

host_name (count=8) = None
        rule_id (count=8) = 111111, 222222
                request_file_name (count=8) = None, /agilefant/login.jsp
                        payload_container (count=8) = ARGS:a, ARGS:b

"""

    _EXPECTED_OUTPUT_WTTH_IGNORED_VARIABLE_DICT = """\
host_name (count=55) = test.domain.com
        request_file_name (count=54) = /agilefant/editIteration.action, /agilefant/login.jsp, /agilefant/static/css/main.css, /agilefant/static/img/agilefant-logo-80px.png, /agilefant/static/img/login_gradient.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.wysiwyg.js
                payload_container (count=18) = REQUEST_HEADERS:Host
                        rule_id (count=18) = 960017
                payload_container (count=18) = TX:anomaly_score
                        rule_id (count=18) = 981174
                payload_container (count=18) = TX:inbound_anomaly_score
                        rule_id (count=18) = 981203
        payload_container (count=1) = TX:sqli_select_statement_count
                request_file_name (count=1) = /agilefant/static/js/backlogSelector.js
                        rule_id (count=1) = 981317

"""

    def setUp(self):
        cleanUp()
    
    def tearDown(self):
        cleanUp()

    @patch('sys.stderr', StringIO())
    @patch('sys.stdout', StringIO())
    def testOK(self):
        sys.stdout.encoding = 'utf-8'
        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])
        self.assertEqual(self._EXPECTED_OUTPUT, sys.stdout.getvalue())
        self.assertEqual(u"\r 30.01% (217/723)\r 60.03% (434/723)\r 90.04% (651/723)\r 90.73% (656/723)\r 93.22% (674/723)\r 95.71% (692/723)\r 98.20% (710/723)\r 98.48% (712/723)\r 98.76% (714/723)\r 98.89% (715/723)\r 99.17% (717/723)\r 99.45% (719/723)\r 99.72% (721/723)\r100.00% (723/723)",
                         sys.stderr.getvalue())

    @patch('modsecurity_exception_factory.correlation.correlation_progress_listener_console.CorrelationProgressListenerConsole.progress')
    @patch('sys.stdout', StringIO())
    def testWithIgnoredVariableDict(self, *args):
        sys.stdout.encoding = 'utf-8'
        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL,
                                                   u"-c", self._TEST_CONFIG_FILE_PATH])
        self.assertEqual(self._EXPECTED_OUTPUT_WTTH_IGNORED_VARIABLE_DICT, sys.stdout.getvalue())

    @patch('sys.stdout', StringIO())
    @patch('modsecurity_exception_factory.correlation.correlation_progress_listener_console.CorrelationProgressListenerConsole.progress')
    def testDataSourceReuse(self, *args):
        sys.stdout.encoding = 'utf-8'

        # This will create the data source.
        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])

        # Reset the buffer.            
        sys.stdout = StringIO()
        sys.stdout.encoding = 'utf-8'
                
        # Reuse the data source.
        CommandModsecurityExceptionFactory().main([u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])
        self.assertEqual(self._EXPECTED_OUTPUT, sys.stdout.getvalue())

    @patch('sys.stdout', StringIO())
    @patch('modsecurity_exception_factory.correlation.correlation_progress_listener_console.CorrelationProgressListenerConsole.progress')
    @patch.object(CorrelationEngine, 'addProgressListener')
    @patch.object(CorrelationEngine, 'correlate')
    @patch.object(CorrelationEngine, '__init__', return_value = None)
    def testConfig(self, mockCorrelationEngineInit, *args):
        sys.stdout.encoding = 'utf-8'

        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL,
                                                   u"-c", self._TEST_CONFIG_FILE_PATH])
        self.assertEqual([call(['host_name', 'request_file_name', 'payload_container', 'rule_id'],
                               {'host_name': [u'1.1.1.1'], 'rule_id': [u'111111', u'222222', u'333333']},
                               1,
                               100)],
                         mockCorrelationEngineInit.mock_calls)

    def testLogPathInvalid(self):
        self.assertRaises(IOError, CommandModsecurityExceptionFactory().main,
                          [u"-i", u"Invalid path",
                           u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])

    def testDataSourceInvalid(self):
        self.assertRaises(OperationalError, CommandModsecurityExceptionFactory().main,
                          [u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])
