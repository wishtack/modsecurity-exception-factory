#-*- coding: utf-8 -*-
#
# Created on Jan 24, 2013
#
# @author: Younes JAAIDI
#
# $Id: $
#

from StringIO import StringIO
from modsecurity_exception_factory.commands.command_modsecurity_exception_factory import \
    CommandModsecurityExceptionFactory
from sqlalchemy.exc import OperationalError
from tests.common import cleanUp, MODSECURITY_AUDIT_LOG_SAMPLE_PATH, MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL
import sys
import unittest

class TestCommandModsecurityExceptionFactory(unittest.TestCase):

    _EXPECTED_OUTPUT = """{'hostName': set([u'1.1.1.1']),
 'requestFileName': set([u'/agilefant/ajax/iterationData.action',
                         u'/agilefant/ajax/myAssignmentsMenuData.action',
                         u'/agilefant/dailyWork.action',
                         u'/agilefant/drawIterationBurndown.action',
                         u'/agilefant/drawSmallIterationBurndown.action',
                         u'/agilefant/static/css/main.css',
                         u'/agilefant/static/img/backlog.png',
                         u'/agilefant/static/img/button_fade.png',
                         u'/agilefant/static/img/dailyWork.png',
                         u'/agilefant/static/img/dynatree/ltL_ne.gif',
                         u'/agilefant/static/img/dynatree/ltL_nes.gif',
                         u'/agilefant/static/img/dynatree/ltL_ns.gif',
                         u'/agilefant/static/img/dynatree/ltM_ne.gif',
                         u'/agilefant/static/img/dynatree/ltM_nes.gif',
                         u'/agilefant/static/img/dynatree/ltP_ne.gif',
                         u'/agilefant/static/img/dynatree/ltP_nes.gif',
                         u'/agilefant/static/img/dynatree/ltWait.gif',
                         u'/agilefant/static/img/favicon.png',
                         u'/agilefant/static/img/filter.png',
                         u'/agilefant/static/img/info.png',
                         u'/agilefant/static/img/labelIcon.png',
                         u'/agilefant/static/img/open_close.png',
                         u'/agilefant/static/img/pleasewait.gif',
                         u'/agilefant/static/img/portfolio.png',
                         u'/agilefant/static/img/search_small.png',
                         u'/agilefant/static/img/settings.png',
                         u'/agilefant/static/img/sort.png',
                         u'/agilefant/static/img/team.png',
                         u'/agilefant/static/img/timesheets.png',
                         u'/agilefant/static/img/toggle.png',
                         u'/agilefant/static/img/top-logo.png',
                         u'/agilefant/static/img/ui/ui-bg_glass_85_dfeffc_1x400.png',
                         u'/agilefant/static/img/ui/ui-bg_gloss-wave_55_333333_500x100.png',
                         u'/agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png',
                         u'/agilefant/static/img/ui/ui-bg_inset-hard_100_f5f8f9_1x100.png',
                         u'/agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png',
                         u'/agilefant/static/img/ui/ui-icons_6da8d5_256x240.png',
                         u'/agilefant/static/img/ui/ui-icons_f9bd01_256x240.png',
                         u'/agilefant/static/js/autocomplete/autocompleteBundle.js',
                         u'/agilefant/static/js/autocomplete/autocompleteDataProvider.js',
                         u'/agilefant/static/js/autocomplete/autocompleteDialog.js',
                         u'/agilefant/static/js/autocomplete/autocompleteInline.js',
                         u'/agilefant/static/js/autocomplete/autocompleteRecent.js',
                         u'/agilefant/static/js/autocomplete/autocompleteSearchBox.js',
                         u'/agilefant/static/js/autocomplete/autocompleteSelectedBox.js',
                         u'/agilefant/static/js/autocomplete/autocompleteSingleDialog.js',
                         u'/agilefant/static/js/backlogChooser.js',
                         u'/agilefant/static/js/backlogSelector.js',
                         u'/agilefant/static/js/date.js',
                         u'/agilefant/static/js/dynamics/Dynamics.events.js',
                         u'/agilefant/static/js/dynamics/controller/AdministrationMenuController.js',
                         u'/agilefant/static/js/dynamics/controller/AssignmentController.js',
                         u'/agilefant/static/js/dynamics/controller/BacklogController.js',
                         u'/agilefant/static/js/dynamics/controller/CommonController.js',
                         u'/agilefant/static/js/dynamics/controller/CreateDialog.js',
                         u'/agilefant/static/js/dynamics/controller/DailyWorkController.js',
                         u'/agilefant/static/js/dynamics/controller/DailyWorkStoryListController.js',
                         u'/agilefant/static/js/dynamics/controller/DailyWorkTasksWithoutStoryController.js',
                         u'/agilefant/static/js/dynamics/controller/HourEntryController.js',
                         u'/agilefant/static/js/dynamics/controller/HourEntryListController.js',
                         u'/agilefant/static/js/dynamics/controller/IterationController.js',
                         u'/agilefant/static/js/dynamics/controller/IterationRowController.js',
                         u'/agilefant/static/js/dynamics/controller/MenuController.js',
                         u'/agilefant/static/js/dynamics/controller/MyAssignmentsMenuController.js',
                         u'/agilefant/static/js/dynamics/controller/PageController.js',
                         u'/agilefant/static/js/dynamics/controller/PersonalLoadController.js',
                         u'/agilefant/static/js/dynamics/controller/PortfolioController.js',
                         u'/agilefant/static/js/dynamics/controller/PortfolioRowController.js',
                         u'/agilefant/static/js/dynamics/controller/ProductController.js',
                         u'/agilefant/static/js/dynamics/controller/ProjectController.js',
                         u'/agilefant/static/js/dynamics/controller/ProjectRowController.js',
                         u'/agilefant/static/js/dynamics/controller/StoryController.js',
                         u'/agilefant/static/js/dynamics/controller/StoryInfoBubble.js',
                         u'/agilefant/static/js/dynamics/controller/StoryListController.js',
                         u'/agilefant/static/js/dynamics/controller/StoryTreeController.js',
                         u'/agilefant/static/js/dynamics/controller/TaskController.js',
                         u'/agilefant/static/js/dynamics/controller/TaskInfoDialog.js',
                         u'/agilefant/static/js/dynamics/controller/TaskSplitDialog.js',
                         u'/agilefant/static/js/dynamics/controller/TasksWithoutStoryController.js',
                         u'/agilefant/static/js/dynamics/controller/TeamListController.js',
                         u'/agilefant/static/js/dynamics/controller/TeamRowController.js',
                         u'/agilefant/static/js/dynamics/controller/UserController.js',
                         u'/agilefant/static/js/dynamics/controller/UserListController.js',
                         u'/agilefant/static/js/dynamics/controller/UserRowController.js',
                         u'/agilefant/static/js/dynamics/controller/WorkQueueController.js',
                         u'/agilefant/static/js/dynamics/model/AssignmentModel.js',
                         u'/agilefant/static/js/dynamics/model/BacklogModel.js',
                         u'/agilefant/static/js/dynamics/model/CommonModel.js',
                         u'/agilefant/static/js/dynamics/model/DailyWorkModel.js',
                         u'/agilefant/static/js/dynamics/model/HourEntryListContainer.js',
                         u'/agilefant/static/js/dynamics/model/HourEntryModel.js',
                         u'/agilefant/static/js/dynamics/model/IterationModel.js',
                         u'/agilefant/static/js/dynamics/model/LabelModel.js',
                         u'/agilefant/static/js/dynamics/model/ModelFactory.js',
                         u'/agilefant/static/js/dynamics/model/PortfolioModel.js',
                         u'/agilefant/static/js/dynamics/model/ProductModel.js',
                         u'/agilefant/static/js/dynamics/model/ProjectModel.js',
                         u'/agilefant/static/js/dynamics/model/StoryModel.js',
                         u'/agilefant/static/js/dynamics/model/TaskModel.js',
                         u'/agilefant/static/js/dynamics/model/TaskSplitContainer.js',
                         u'/agilefant/static/js/dynamics/model/TeamListContainer.js',
                         u'/agilefant/static/js/dynamics/model/TeamModel.js',
                         u'/agilefant/static/js/dynamics/model/UserListContainer.js',
                         u'/agilefant/static/js/dynamics/model/UserModel.js',
                         u'/agilefant/static/js/dynamics/model/WorkQueueTaskModel.js',
                         u'/agilefant/static/js/dynamics/model/comparators.js',
                         u'/agilefant/static/js/dynamics/view/Bubble.js',
                         u'/agilefant/static/js/dynamics/view/Cell.js',
                         u'/agilefant/static/js/dynamics/view/ChangePasswordDialog.js',
                         u'/agilefant/static/js/dynamics/view/CommonFragmentSubView.js',
                         u'/agilefant/static/js/dynamics/view/CommonSubView.js',
                         u'/agilefant/static/js/dynamics/view/ConfirmationDialog.js',
                         u'/agilefant/static/js/dynamics/view/DynamicView.js',
                         u'/agilefant/static/js/dynamics/view/LazyLoadedDialog.js',
                         u'/agilefant/static/js/dynamics/view/MessageDisplay.js',
                         u'/agilefant/static/js/dynamics/view/MultiEditWidget.js',
                         u'/agilefant/static/js/dynamics/view/Row.js',
                         u'/agilefant/static/js/dynamics/view/SearchByTextWidget.js',
                         u'/agilefant/static/js/dynamics/view/SpentEffortWidget.js',
                         u'/agilefant/static/js/dynamics/view/StateFilterWidget.js',
                         u'/agilefant/static/js/dynamics/view/StoryFiltersView.js',
                         u'/agilefant/static/js/dynamics/view/Table.js',
                         u'/agilefant/static/js/dynamics/view/TableCaption.js',
                         u'/agilefant/static/js/dynamics/view/TableCellEditors.js',
                         u'/agilefant/static/js/dynamics/view/TableConfiguration.js',
                         u'/agilefant/static/js/dynamics/view/UserSpentEffortWidget.js',
                         u'/agilefant/static/js/dynamics/view/ValidationManager.js',
                         u'/agilefant/static/js/dynamics/view/ViewPart.js',
                         u'/agilefant/static/js/dynamics/view/decorators.js',
                         u'/agilefant/static/js/dynamics/view/subviews/AutoSuggest.js',
                         u'/agilefant/static/js/dynamics/view/subviews/Button.js',
                         u'/agilefant/static/js/dynamics/view/subviews/Buttons.js',
                         u'/agilefant/static/js/dynamics/view/subviews/CellBubble.js',
                         u'/agilefant/static/js/dynamics/view/subviews/LabelsIcon.js',
                         u'/agilefant/static/js/dynamics/view/subviews/LabelsView.js',
                         u'/agilefant/static/js/dynamics/view/subviews/RowActions.js',
                         u'/agilefant/static/js/dynamics/view/subviews/SplitPanel.js',
                         u'/agilefant/static/js/dynamics/view/subviews/StoryInfoWidget.js',
                         u'/agilefant/static/js/dynamics/view/subviews/Tabs.js',
                         u'/agilefant/static/js/dynamics/view/subviews/Toggle.js',
                         u'/agilefant/static/js/jquery-ui.min.js',
                         u'/agilefant/static/js/jquery.autoSuggest.minified.js',
                         u'/agilefant/static/js/jquery.cookie.js',
                         u'/agilefant/static/js/jquery.dynatree.js',
                         u'/agilefant/static/js/jquery.hotkeys.js',
                         u'/agilefant/static/js/jquery.js',
                         u'/agilefant/static/js/jquery.jstree.js',
                         u'/agilefant/static/js/jquery.labelify.js',
                         u'/agilefant/static/js/jquery.tagcloud.min.js',
                         u'/agilefant/static/js/jquery.tooltip.js',
                         u'/agilefant/static/js/jquery.wysiwyg.js',
                         u'/agilefant/static/js/utils/ArrayUtils.js',
                         u'/agilefant/static/js/utils/ClassUtils.js',
                         u'/agilefant/static/js/utils/HelpUtils.js',
                         u'/agilefant/static/js/utils/Parsers.js',
                         u'/agilefant/static/js/utils/XworkSerializer.js',
                         u'/agilefant/static/js/utils/aef.jstree.plugin.js',
                         u'/agilefant/static/js/utils/menuTimer.js',
                         u'/agilefant/static/js/utils/quickSearch.js',
                         u'/agilefant/static/js/utils/refLinkDisplay.js']),
 ('payloadContainer', 'ruleId'): set([(u'REQUEST_HEADERS:Host', u'960017'),
                                      (u'TX:anomaly_score', u'981174'),
                                      (u'TX:inbound_anomaly_score',
                                       u'981203')])}
{'hostName': set([u'1.1.1.1']),
 'payloadContainer': set([u'TX:sqli_select_statement_count']),
 'requestFileName': set([u'/agilefant/drawIterationBurndown.action',
                         u'/agilefant/static/img/top-logo.png',
                         u'/agilefant/static/js/autocomplete/autocompleteSelectedBox.js',
                         u'/agilefant/static/js/backlogSelector.js']),
 'ruleId': set([u'981317'])}
{'hostName': set([u'test.domain.com']),
 'requestFileName': set([u'/agilefant/editIteration.action',
                         u'/agilefant/login.jsp',
                         u'/agilefant/static/css/main.css',
                         u'/agilefant/static/img/agilefant-logo-80px.png',
                         u'/agilefant/static/img/login_gradient.png',
                         u'/agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png',
                         u'/agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png',
                         u'/agilefant/static/js/backlogChooser.js',
                         u'/agilefant/static/js/backlogSelector.js',
                         u'/agilefant/static/js/date.js',
                         u'/agilefant/static/js/jquery-ui.min.js',
                         u'/agilefant/static/js/jquery.cookie.js',
                         u'/agilefant/static/js/jquery.dynatree.js',
                         u'/agilefant/static/js/jquery.hotkeys.js',
                         u'/agilefant/static/js/jquery.js',
                         u'/agilefant/static/js/jquery.wysiwyg.js']),
 ('payloadContainer', 'ruleId'): set([(u'REQUEST_HEADERS:Host', u'960017'),
                                      (u'TX:anomaly_score', u'981174'),
                                      (u'TX:inbound_anomaly_score',
                                       u'981203')])}
{'hostName': set([u'test.domain.com']),
 'payloadContainer': set([u'ARGS:a', u'ARGS:b']),
 'requestFileName': set([u'/agilefant/login.jsp']),
 'ruleId': set([u'111111', u'222222'])}
{'hostName': set([u'test.domain.com']),
 'payloadContainer': set([u'TX:sqli_select_statement_count']),
 'requestFileName': set([u'/agilefant/static/js/backlogSelector.js']),
 'ruleId': set([u'981317'])}
"""

    def setUp(self):
        # Backup stdout.
        cleanUp()
        self._stdout = sys.stdout
        sys.stdout = StringIO()
    
    def tearDown(self):
        # Restore stdout.
        sys.stdout = self._stdout
        cleanUp()
    
    def testOK(self):
        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])
        self.assertEqual(self._EXPECTED_OUTPUT, sys.stdout.getvalue())

    def testDataSourceReuse(self):
        # This will create the data source.
        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])

        # Reuse the data source.
        sys.stdout = StringIO()
        CommandModsecurityExceptionFactory().main([u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])
        self.assertEqual(self._EXPECTED_OUTPUT, sys.stdout.getvalue())

    def testLogPathInvalid(self):
        self.assertRaises(IOError, CommandModsecurityExceptionFactory().main,
                          [u"-i", u"Invalid path",
                           u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])

    def testDataSourceInvalid(self):
        self.assertRaises(OperationalError, CommandModsecurityExceptionFactory().main,
                          [u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])
