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
    MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL, makeTestFilePath
import sys
import unittest

class TestCommandModsecurityExceptionFactory(unittest.TestCase):

    def setUp(self):
        self._test_config_file_path = makeTestFilePath(u"data/test_command_modsecurity_exception_factory.yaml")

        self._expected_output = """\

# Hit Count: 656
SecRule HOSTNAME "!@rx ^(1\.1\.1\.1)$" "id:10000,t:none,nolog,pass,skipAfter:EXCEPTION_1"
    
    # Hit Count: 651
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/ajax\/iterationData\.action|\/agilefant\/ajax\/myAssignmentsMenuData\.action|\/agilefant\/dailyWork\.action|\/agilefant\/drawIterationBurndown\.action|\/agilefant\/drawSmallIterationBurndown\.action|\/agilefant\/static\/css\/main\.css|\/agilefant\/static\/img\/backlog\.png|\/agilefant\/static\/img\/button\_fade\.png|\/agilefant\/static\/img\/dailyWork\.png|\/agilefant\/static\/img\/dynatree\/ltL\_ne\.gif|\/agilefant\/static\/img\/dynatree\/ltL\_nes\.gif|\/agilefant\/static\/img\/dynatree\/ltL\_ns\.gif|\/agilefant\/static\/img\/dynatree\/ltM\_ne\.gif|\/agilefant\/static\/img\/dynatree\/ltM\_nes\.gif|\/agilefant\/static\/img\/dynatree\/ltP\_ne\.gif|\/agilefant\/static\/img\/dynatree\/ltP\_nes\.gif|\/agilefant\/static\/img\/dynatree\/ltWait\.gif|\/agilefant\/static\/img\/favicon\.png|\/agilefant\/static\/img\/filter\.png|\/agilefant\/static\/img\/info\.png|\/agilefant\/static\/img\/labelIcon\.png|\/agilefant\/static\/img\/open\_close\.png|\/agilefant\/static\/img\/pleasewait\.gif|\/agilefant\/static\/img\/portfolio\.png|\/agilefant\/static\/img\/search\_small\.png|\/agilefant\/static\/img\/settings\.png|\/agilefant\/static\/img\/sort\.png|\/agilefant\/static\/img\/team\.png|\/agilefant\/static\/img\/timesheets\.png|\/agilefant\/static\/img\/toggle\.png|\/agilefant\/static\/img\/top\-logo\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_glass\_85\_dfeffc\_1x400\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_gloss\-wave\_55\_333333\_500x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_gloss\-wave\_55\_5c9ccc\_500x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_inset\-hard\_100\_f5f8f9\_1x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_inset\-hard\_100\_fcfdfd\_1x100\.png|\/agilefant\/static\/img\/ui\/ui\-icons\_6da8d5\_256x240\.png|\/agilefant\/static\/img\/ui\/ui\-icons\_f9bd01\_256x240\.png|\/agilefant\/static\/js\/autocomplete\/autocompleteBundle\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteDataProvider\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteDialog\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteInline\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteRecent\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteSearchBox\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteSelectedBox\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteSingleDialog\.js|\/agilefant\/static\/js\/backlogChooser\.js|\/agilefant\/static\/js\/backlogSelector\.js|\/agilefant\/static\/js\/date\.js|\/agilefant\/static\/js\/dynamics\/Dynamics\.events\.js|\/agilefant\/static\/js\/dynamics\/controller\/AdministrationMenuController\.js|\/agilefant\/static\/js\/dynamics\/controller\/AssignmentController\.js|\/agilefant\/static\/js\/dynamics\/controller\/BacklogController\.js|\/agilefant\/static\/js\/dynamics\/controller\/CommonController\.js|\/agilefant\/static\/js\/dynamics\/controller\/CreateDialog\.js|\/agilefant\/static\/js\/dynamics\/controller\/DailyWorkController\.js|\/agilefant\/static\/js\/dynamics\/controller\/DailyWorkStoryListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/DailyWorkTasksWithoutStoryController\.js|\/agilefant\/static\/js\/dynamics\/controller\/HourEntryController\.js|\/agilefant\/static\/js\/dynamics\/controller\/HourEntryListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/IterationController\.js|\/agilefant\/static\/js\/dynamics\/controller\/IterationRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/MenuController\.js|\/agilefant\/static\/js\/dynamics\/controller\/MyAssignmentsMenuController\.js|\/agilefant\/static\/js\/dynamics\/controller\/PageController\.js|\/agilefant\/static\/js\/dynamics\/controller\/PersonalLoadController\.js|\/agilefant\/static\/js\/dynamics\/controller\/PortfolioController\.js|\/agilefant\/static\/js\/dynamics\/controller\/PortfolioRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/ProductController\.js|\/agilefant\/static\/js\/dynamics\/controller\/ProjectController\.js|\/agilefant\/static\/js\/dynamics\/controller\/ProjectRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/StoryController\.js|\/agilefant\/static\/js\/dynamics\/controller\/StoryInfoBubble\.js|\/agilefant\/static\/js\/dynamics\/controller\/StoryListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/StoryTreeController\.js|\/agilefant\/static\/js\/dynamics\/controller\/TaskController\.js|\/agilefant\/static\/js\/dynamics\/controller\/TaskInfoDialog\.js|\/agilefant\/static\/js\/dynamics\/controller\/TaskSplitDialog\.js|\/agilefant\/static\/js\/dynamics\/controller\/TasksWithoutStoryController\.js|\/agilefant\/static\/js\/dynamics\/controller\/TeamListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/TeamRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/UserController\.js|\/agilefant\/static\/js\/dynamics\/controller\/UserListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/UserRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/WorkQueueController\.js|\/agilefant\/static\/js\/dynamics\/model\/AssignmentModel\.js|\/agilefant\/static\/js\/dynamics\/model\/BacklogModel\.js|\/agilefant\/static\/js\/dynamics\/model\/CommonModel\.js|\/agilefant\/static\/js\/dynamics\/model\/DailyWorkModel\.js|\/agilefant\/static\/js\/dynamics\/model\/HourEntryListContainer\.js|\/agilefant\/static\/js\/dynamics\/model\/HourEntryModel\.js|\/agilefant\/static\/js\/dynamics\/model\/IterationModel\.js|\/agilefant\/static\/js\/dynamics\/model\/LabelModel\.js|\/agilefant\/static\/js\/dynamics\/model\/ModelFactory\.js|\/agilefant\/static\/js\/dynamics\/model\/PortfolioModel\.js|\/agilefant\/static\/js\/dynamics\/model\/ProductModel\.js|\/agilefant\/static\/js\/dynamics\/model\/ProjectModel\.js|\/agilefant\/static\/js\/dynamics\/model\/StoryModel\.js|\/agilefant\/static\/js\/dynamics\/model\/TaskModel\.js|\/agilefant\/static\/js\/dynamics\/model\/TaskSplitContainer\.js|\/agilefant\/static\/js\/dynamics\/model\/TeamListContainer\.js|\/agilefant\/static\/js\/dynamics\/model\/TeamModel\.js|\/agilefant\/static\/js\/dynamics\/model\/UserListContainer\.js|\/agilefant\/static\/js\/dynamics\/model\/UserModel\.js|\/agilefant\/static\/js\/dynamics\/model\/WorkQueueTaskModel\.js|\/agilefant\/static\/js\/dynamics\/model\/comparators\.js|\/agilefant\/static\/js\/dynamics\/view\/Bubble\.js|\/agilefant\/static\/js\/dynamics\/view\/Cell\.js|\/agilefant\/static\/js\/dynamics\/view\/ChangePasswordDialog\.js|\/agilefant\/static\/js\/dynamics\/view\/CommonFragmentSubView\.js|\/agilefant\/static\/js\/dynamics\/view\/CommonSubView\.js|\/agilefant\/static\/js\/dynamics\/view\/ConfirmationDialog\.js|\/agilefant\/static\/js\/dynamics\/view\/DynamicView\.js|\/agilefant\/static\/js\/dynamics\/view\/LazyLoadedDialog\.js|\/agilefant\/static\/js\/dynamics\/view\/MessageDisplay\.js|\/agilefant\/static\/js\/dynamics\/view\/MultiEditWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/Row\.js|\/agilefant\/static\/js\/dynamics\/view\/SearchByTextWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/SpentEffortWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/StateFilterWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/StoryFiltersView\.js|\/agilefant\/static\/js\/dynamics\/view\/Table\.js|\/agilefant\/static\/js\/dynamics\/view\/TableCaption\.js|\/agilefant\/static\/js\/dynamics\/view\/TableCellEditors\.js|\/agilefant\/static\/js\/dynamics\/view\/TableConfiguration\.js|\/agilefant\/static\/js\/dynamics\/view\/UserSpentEffortWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/ValidationManager\.js|\/agilefant\/static\/js\/dynamics\/view\/ViewPart\.js|\/agilefant\/static\/js\/dynamics\/view\/decorators\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/AutoSuggest\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/Button\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/Buttons\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/CellBubble\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/LabelsIcon\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/LabelsView\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/RowActions\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/SplitPanel\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/StoryInfoWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/Tabs\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/Toggle\.js|\/agilefant\/static\/js\/jquery\-ui\.min\.js|\/agilefant\/static\/js\/jquery\.autoSuggest\.minified\.js|\/agilefant\/static\/js\/jquery\.cookie\.js|\/agilefant\/static\/js\/jquery\.dynatree\.js|\/agilefant\/static\/js\/jquery\.hotkeys\.js|\/agilefant\/static\/js\/jquery\.js|\/agilefant\/static\/js\/jquery\.jstree\.js|\/agilefant\/static\/js\/jquery\.labelify\.js|\/agilefant\/static\/js\/jquery\.tagcloud\.min\.js|\/agilefant\/static\/js\/jquery\.tooltip\.js|\/agilefant\/static\/js\/jquery\.wysiwyg\.js|\/agilefant\/static\/js\/utils\/ArrayUtils\.js|\/agilefant\/static\/js\/utils\/ClassUtils\.js|\/agilefant\/static\/js\/utils\/HelpUtils\.js|\/agilefant\/static\/js\/utils\/Parsers\.js|\/agilefant\/static\/js\/utils\/XworkSerializer\.js|\/agilefant\/static\/js\/utils\/aef\.jstree\.plugin\.js|\/agilefant\/static\/js\/utils\/menuTimer\.js|\/agilefant\/static\/js\/utils\/quickSearch\.js|\/agilefant\/static\/js\/utils\/refLinkDisplay\.js)$" "id:10001,t:none,nolog,pass,skipAfter:EXCEPTION_2"
        
        # Hit Count: 217
        SecAction "id:10002,t:none,nolog,pass,ctl:'ruleRemoveTargetById=960017;REQUEST_HEADERS:Host'"
        
        # Hit Count: 217
        SecAction "id:10003,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981174;TX:anomaly_score'"
        
        # Hit Count: 217
        SecAction "id:10004,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981203;TX:inbound_anomaly_score'"
    
    SecMarker EXCEPTION_2
    
    # Hit Count: 5
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/drawIterationBurndown\.action|\/agilefant\/static\/img\/top\-logo\.png|\/agilefant\/static\/js\/autocomplete\/autocompleteSelectedBox\.js|\/agilefant\/static\/js\/backlogSelector\.js)$" "id:10005,t:none,nolog,pass,skipAfter:EXCEPTION_3"
        
        # Hit Count: 5
        SecAction "id:10006,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981317;TX:sqli_select_statement_count'"
    
    SecMarker EXCEPTION_3

SecMarker EXCEPTION_1

# Hit Count: 59
SecRule HOSTNAME "!@rx ^(test\.domain\.com)$" "id:10007,t:none,nolog,pass,skipAfter:EXCEPTION_4"
    
    # Hit Count: 54
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/editIteration\.action|\/agilefant\/login\.jsp|\/agilefant\/static\/css\/main\.css|\/agilefant\/static\/img\/agilefant\-logo\-80px\.png|\/agilefant\/static\/img\/login\_gradient\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_gloss\-wave\_55\_5c9ccc\_500x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_inset\-hard\_100\_fcfdfd\_1x100\.png|\/agilefant\/static\/js\/backlogChooser\.js|\/agilefant\/static\/js\/backlogSelector\.js|\/agilefant\/static\/js\/date\.js|\/agilefant\/static\/js\/jquery\-ui\.min\.js|\/agilefant\/static\/js\/jquery\.cookie\.js|\/agilefant\/static\/js\/jquery\.dynatree\.js|\/agilefant\/static\/js\/jquery\.hotkeys\.js|\/agilefant\/static\/js\/jquery\.js|\/agilefant\/static\/js\/jquery\.wysiwyg\.js)$" "id:10008,t:none,nolog,pass,skipAfter:EXCEPTION_5"
        
        # Hit Count: 18
        SecAction "id:10009,t:none,nolog,pass,ctl:'ruleRemoveTargetById=960017;REQUEST_HEADERS:Host'"
        
        # Hit Count: 18
        SecAction "id:10010,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981174;TX:anomaly_score'"
        
        # Hit Count: 18
        SecAction "id:10011,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981203;TX:inbound_anomaly_score'"
    
    SecMarker EXCEPTION_5
    
    # Hit Count: 4
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/login\.jsp)$" "id:10012,t:none,nolog,pass,skipAfter:EXCEPTION_6"
        
        # Hit Count: 4
        SecAction "id:10013,t:none,nolog,pass,ctl:'ruleRemoveTargetById=111111;ARGS:a,ARGS:b'"
        SecAction "id:10014,t:none,nolog,pass,ctl:'ruleRemoveTargetById=222222;ARGS:a,ARGS:b'"
    
    SecMarker EXCEPTION_6
    
    # Hit Count: 1
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/static\/js\/backlogSelector\.js)$" "id:10015,t:none,nolog,pass,skipAfter:EXCEPTION_7"
        
        # Hit Count: 1
        SecAction "id:10016,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981317;TX:sqli_select_statement_count'"
    
    SecMarker EXCEPTION_7

SecMarker EXCEPTION_4

# Hit Count: 8
SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/login\.jsp)$" "id:10017,t:none,nolog,pass,skipAfter:EXCEPTION_8"
    
    # Hit Count: 8
    SecAction "id:10018,t:none,nolog,pass,ctl:'ruleRemoveTargetById=111111;ARGS:a,ARGS:b'"
    SecAction "id:10019,t:none,nolog,pass,ctl:'ruleRemoveTargetById=222222;ARGS:a,ARGS:b'"

SecMarker EXCEPTION_8
"""

        self._expected_output_with_ignored_variable_dict = """\

# Hit Count: 55
SecRule HOSTNAME "!@rx ^(test\.domain\.com)$" "id:10000,t:none,nolog,pass,skipAfter:EXCEPTION_1"
    
    # Hit Count: 54
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/editIteration\.action|\/agilefant\/login\.jsp|\/agilefant\/static\/css\/main\.css|\/agilefant\/static\/img\/agilefant\-logo\-80px\.png|\/agilefant\/static\/img\/login\_gradient\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_gloss\-wave\_55\_5c9ccc\_500x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_inset\-hard\_100\_fcfdfd\_1x100\.png|\/agilefant\/static\/js\/backlogChooser\.js|\/agilefant\/static\/js\/backlogSelector\.js|\/agilefant\/static\/js\/date\.js|\/agilefant\/static\/js\/jquery\-ui\.min\.js|\/agilefant\/static\/js\/jquery\.cookie\.js|\/agilefant\/static\/js\/jquery\.dynatree\.js|\/agilefant\/static\/js\/jquery\.hotkeys\.js|\/agilefant\/static\/js\/jquery\.js|\/agilefant\/static\/js\/jquery\.wysiwyg\.js)$" "id:10001,t:none,nolog,pass,skipAfter:EXCEPTION_2"
        
        # Hit Count: 18
        SecAction "id:10002,t:none,nolog,pass,ctl:'ruleRemoveTargetById=960017;REQUEST_HEADERS:Host'"
        
        # Hit Count: 18
        SecAction "id:10003,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981174;TX:anomaly_score'"
        
        # Hit Count: 18
        SecAction "id:10004,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981203;TX:inbound_anomaly_score'"
    
    SecMarker EXCEPTION_2
    
    # Hit Count: 1
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/static\/js\/backlogSelector\.js)$" "id:10005,t:none,nolog,pass,skipAfter:EXCEPTION_3"
        
        # Hit Count: 1
        SecAction "id:10006,t:none,nolog,pass,ctl:'ruleRemoveTargetById=981317;TX:sqli_select_statement_count'"
    
    SecMarker EXCEPTION_3

SecMarker EXCEPTION_1
"""

        cleanUp()
    
    def tearDown(self):
        cleanUp()

    @patch('sys.stderr', StringIO())
    @patch('sys.stdout', StringIO())
    def testOK(self):
        sys.stdout.encoding = 'utf-8'
        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL])
        self.assertEqual(self._expected_output, sys.stdout.getvalue())
        self.assertEqual(u"\r 30.01% (217/723)\r 60.03% (434/723)\r 90.04% (651/723)\r 90.73% (656/723)\r 93.22% (674/723)\r 95.71% (692/723)\r 98.20% (710/723)\r 98.48% (712/723)\r 98.76% (714/723)\r 98.89% (715/723)\r 99.17% (717/723)\r 99.45% (719/723)\r 99.72% (721/723)\r100.00% (723/723)",
                         sys.stderr.getvalue())

    @patch('modsecurity_exception_factory.correlation.correlation_progress_listener_console.CorrelationProgressListenerConsole.progress')
    @patch('sys.stdout', StringIO())
    def testWithIgnoredVariableDict(self, *args):
        sys.stdout.encoding = 'utf-8'
        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL,
                                                   u"-c", self._test_config_file_path])
        self.assertEqual(self._expected_output_with_ignored_variable_dict, sys.stdout.getvalue())

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
        self.assertEqual(self._expected_output, sys.stdout.getvalue())

    @patch('sys.stdout', StringIO())
    @patch('modsecurity_exception_factory.correlation.correlation_progress_listener_console.CorrelationProgressListenerConsole.progress')
    @patch.object(CorrelationEngine, 'addProgressListener')
    @patch.object(CorrelationEngine, 'correlate')
    @patch.object(CorrelationEngine, '__init__', return_value = None)
    def testConfig(self, mockCorrelationEngineInit, *args):
        sys.stdout.encoding = 'utf-8'

        CommandModsecurityExceptionFactory().main([u"-i", MODSECURITY_AUDIT_LOG_SAMPLE_PATH,
                                                   u"-d", MODSECURITY_AUDIT_ENTRY_DATA_SOURCE_SQLITE_URL,
                                                   u"-c", self._test_config_file_path])
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
