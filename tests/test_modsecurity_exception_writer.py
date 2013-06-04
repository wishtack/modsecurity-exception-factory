#-*- coding: utf-8 -*-
#
# Created on May 29, 2013
#
# @author: Younes JAAIDI <yjaaidi@shookalabs.com>
#
# $Id$
#

from StringIO import StringIO
from modsecurity_exception_factory.correlation.correlation_serializer_yaml import \
    CorrelationSerializerYaml
from modsecurity_exception_factory.modsecurity_exception_writer import \
    ModsecurityExcetionWriter
import unittest

class TestModsecurityExceptionWriter(unittest.TestCase):

    def setUp(self):
        self._correlation_yaml_data = u"""\
variable_name: host_name
item_count: 656
variable_value_list:
- 1.1.1.1
- www.shookalabs.com
sub_correlation_list:
- variable_name: request_file_name
  item_count: 651
  variable_value_list: [/agilefant/ajax/iterationData.action, /agilefant/ajax/myAssignmentsMenuData.action, /agilefant/dailyWork.action, /agilefant/drawIterationBurndown.action, /agilefant/drawSmallIterationBurndown.action, /agilefant/static/css/main.css, /agilefant/static/img/backlog.png, /agilefant/static/img/button_fade.png, /agilefant/static/img/dailyWork.png, /agilefant/static/img/dynatree/ltL_ne.gif, /agilefant/static/img/dynatree/ltL_nes.gif, /agilefant/static/img/dynatree/ltL_ns.gif, /agilefant/static/img/dynatree/ltM_ne.gif, /agilefant/static/img/dynatree/ltM_nes.gif, /agilefant/static/img/dynatree/ltP_ne.gif, /agilefant/static/img/dynatree/ltP_nes.gif, /agilefant/static/img/dynatree/ltWait.gif, /agilefant/static/img/favicon.png, /agilefant/static/img/filter.png, /agilefant/static/img/info.png, /agilefant/static/img/labelIcon.png, /agilefant/static/img/open_close.png, /agilefant/static/img/pleasewait.gif, /agilefant/static/img/portfolio.png, /agilefant/static/img/search_small.png, /agilefant/static/img/settings.png, /agilefant/static/img/sort.png, /agilefant/static/img/team.png, /agilefant/static/img/timesheets.png, /agilefant/static/img/toggle.png, /agilefant/static/img/top-logo.png, /agilefant/static/img/ui/ui-bg_glass_85_dfeffc_1x400.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_333333_500x100.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_f5f8f9_1x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/img/ui/ui-icons_6da8d5_256x240.png, /agilefant/static/img/ui/ui-icons_f9bd01_256x240.png, /agilefant/static/js/autocomplete/autocompleteBundle.js, /agilefant/static/js/autocomplete/autocompleteDataProvider.js, /agilefant/static/js/autocomplete/autocompleteDialog.js, /agilefant/static/js/autocomplete/autocompleteInline.js, /agilefant/static/js/autocomplete/autocompleteRecent.js, /agilefant/static/js/autocomplete/autocompleteSearchBox.js, /agilefant/static/js/autocomplete/autocompleteSelectedBox.js, /agilefant/static/js/autocomplete/autocompleteSingleDialog.js, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/dynamics/Dynamics.events.js, /agilefant/static/js/dynamics/controller/AdministrationMenuController.js, /agilefant/static/js/dynamics/controller/AssignmentController.js, /agilefant/static/js/dynamics/controller/BacklogController.js, /agilefant/static/js/dynamics/controller/CommonController.js, /agilefant/static/js/dynamics/controller/CreateDialog.js, /agilefant/static/js/dynamics/controller/DailyWorkController.js, /agilefant/static/js/dynamics/controller/DailyWorkStoryListController.js, /agilefant/static/js/dynamics/controller/DailyWorkTasksWithoutStoryController.js, /agilefant/static/js/dynamics/controller/HourEntryController.js, /agilefant/static/js/dynamics/controller/HourEntryListController.js, /agilefant/static/js/dynamics/controller/IterationController.js, /agilefant/static/js/dynamics/controller/IterationRowController.js, /agilefant/static/js/dynamics/controller/MenuController.js, /agilefant/static/js/dynamics/controller/MyAssignmentsMenuController.js, /agilefant/static/js/dynamics/controller/PageController.js, /agilefant/static/js/dynamics/controller/PersonalLoadController.js, /agilefant/static/js/dynamics/controller/PortfolioController.js, /agilefant/static/js/dynamics/controller/PortfolioRowController.js, /agilefant/static/js/dynamics/controller/ProductController.js, /agilefant/static/js/dynamics/controller/ProjectController.js, /agilefant/static/js/dynamics/controller/ProjectRowController.js, /agilefant/static/js/dynamics/controller/StoryController.js, /agilefant/static/js/dynamics/controller/StoryInfoBubble.js, /agilefant/static/js/dynamics/controller/StoryListController.js, /agilefant/static/js/dynamics/controller/StoryTreeController.js, /agilefant/static/js/dynamics/controller/TaskController.js, /agilefant/static/js/dynamics/controller/TaskInfoDialog.js, /agilefant/static/js/dynamics/controller/TaskSplitDialog.js, /agilefant/static/js/dynamics/controller/TasksWithoutStoryController.js, /agilefant/static/js/dynamics/controller/TeamListController.js, /agilefant/static/js/dynamics/controller/TeamRowController.js, /agilefant/static/js/dynamics/controller/UserController.js, /agilefant/static/js/dynamics/controller/UserListController.js, /agilefant/static/js/dynamics/controller/UserRowController.js, /agilefant/static/js/dynamics/controller/WorkQueueController.js, /agilefant/static/js/dynamics/model/AssignmentModel.js, /agilefant/static/js/dynamics/model/BacklogModel.js, /agilefant/static/js/dynamics/model/CommonModel.js, /agilefant/static/js/dynamics/model/DailyWorkModel.js, /agilefant/static/js/dynamics/model/HourEntryListContainer.js, /agilefant/static/js/dynamics/model/HourEntryModel.js, /agilefant/static/js/dynamics/model/IterationModel.js, /agilefant/static/js/dynamics/model/LabelModel.js, /agilefant/static/js/dynamics/model/ModelFactory.js, /agilefant/static/js/dynamics/model/PortfolioModel.js, /agilefant/static/js/dynamics/model/ProductModel.js, /agilefant/static/js/dynamics/model/ProjectModel.js, /agilefant/static/js/dynamics/model/StoryModel.js, /agilefant/static/js/dynamics/model/TaskModel.js, /agilefant/static/js/dynamics/model/TaskSplitContainer.js, /agilefant/static/js/dynamics/model/TeamListContainer.js, /agilefant/static/js/dynamics/model/TeamModel.js, /agilefant/static/js/dynamics/model/UserListContainer.js, /agilefant/static/js/dynamics/model/UserModel.js, /agilefant/static/js/dynamics/model/WorkQueueTaskModel.js, /agilefant/static/js/dynamics/model/comparators.js, /agilefant/static/js/dynamics/view/Bubble.js, /agilefant/static/js/dynamics/view/Cell.js, /agilefant/static/js/dynamics/view/ChangePasswordDialog.js, /agilefant/static/js/dynamics/view/CommonFragmentSubView.js, /agilefant/static/js/dynamics/view/CommonSubView.js, /agilefant/static/js/dynamics/view/ConfirmationDialog.js, /agilefant/static/js/dynamics/view/DynamicView.js, /agilefant/static/js/dynamics/view/LazyLoadedDialog.js, /agilefant/static/js/dynamics/view/MessageDisplay.js, /agilefant/static/js/dynamics/view/MultiEditWidget.js, /agilefant/static/js/dynamics/view/Row.js, /agilefant/static/js/dynamics/view/SearchByTextWidget.js, /agilefant/static/js/dynamics/view/SpentEffortWidget.js, /agilefant/static/js/dynamics/view/StateFilterWidget.js, /agilefant/static/js/dynamics/view/StoryFiltersView.js, /agilefant/static/js/dynamics/view/Table.js, /agilefant/static/js/dynamics/view/TableCaption.js, /agilefant/static/js/dynamics/view/TableCellEditors.js, /agilefant/static/js/dynamics/view/TableConfiguration.js, /agilefant/static/js/dynamics/view/UserSpentEffortWidget.js, /agilefant/static/js/dynamics/view/ValidationManager.js, /agilefant/static/js/dynamics/view/ViewPart.js, /agilefant/static/js/dynamics/view/decorators.js, /agilefant/static/js/dynamics/view/subviews/AutoSuggest.js, /agilefant/static/js/dynamics/view/subviews/Button.js, /agilefant/static/js/dynamics/view/subviews/Buttons.js, /agilefant/static/js/dynamics/view/subviews/CellBubble.js, /agilefant/static/js/dynamics/view/subviews/LabelsIcon.js, /agilefant/static/js/dynamics/view/subviews/LabelsView.js, /agilefant/static/js/dynamics/view/subviews/RowActions.js, /agilefant/static/js/dynamics/view/subviews/SplitPanel.js, /agilefant/static/js/dynamics/view/subviews/StoryInfoWidget.js, /agilefant/static/js/dynamics/view/subviews/Tabs.js, /agilefant/static/js/dynamics/view/subviews/Toggle.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.autoSuggest.minified.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.jstree.js, /agilefant/static/js/jquery.labelify.js, /agilefant/static/js/jquery.tagcloud.min.js, /agilefant/static/js/jquery.tooltip.js, /agilefant/static/js/jquery.wysiwyg.js, /agilefant/static/js/utils/ArrayUtils.js, /agilefant/static/js/utils/ClassUtils.js, /agilefant/static/js/utils/HelpUtils.js, /agilefant/static/js/utils/Parsers.js, /agilefant/static/js/utils/XworkSerializer.js, /agilefant/static/js/utils/aef.jstree.plugin.js, /agilefant/static/js/utils/menuTimer.js, /agilefant/static/js/utils/quickSearch.js, /agilefant/static/js/utils/refLinkDisplay.js]
  sub_correlation_list:
  - variable_name: payload_container
    item_count: 217
    variable_value_list: ['REQUEST_HEADERS:Host']
    sub_correlation_list:
    - variable_name: rule_id
      item_count: 217
      variable_value_list: ['960017']
  - variable_name: payload_container
    item_count: 217
    variable_value_list: ['TX:anomaly_score']
    sub_correlation_list:
    - variable_name: rule_id
      item_count: 217
      variable_value_list: ['981174']
  - variable_name: payload_container
    item_count: 217
    variable_value_list: ['TX:inbound_anomaly_score']
    sub_correlation_list:
    - variable_name: rule_id
      item_count: 217
      variable_value_list: ['981203']
- variable_name: payload_container
  item_count: 5
  variable_value_list: ['TX:sqli_select_statement_count']
  sub_correlation_list:
  - variable_name: rule_id
    item_count: 5
    variable_value_list: ['981317']
    sub_correlation_list:
    - variable_name: request_file_name
      item_count: 5
      variable_value_list: [/agilefant/drawIterationBurndown.action, /agilefant/static/img/top-logo.png, /agilefant/static/js/autocomplete/autocompleteSelectedBox.js, /agilefant/static/js/backlogSelector.js]
---
variable_name: host_name
item_count: 59
variable_value_list: [test.domain.com]
sub_correlation_list:
- variable_name: request_file_name
  item_count: 54
  variable_value_list: [/agilefant/editIteration.action, /agilefant/login.jsp, /agilefant/static/css/main.css, /agilefant/static/img/agilefant-logo-80px.png, /agilefant/static/img/login_gradient.png, /agilefant/static/img/ui/ui-bg_gloss-wave_55_5c9ccc_500x100.png, /agilefant/static/img/ui/ui-bg_inset-hard_100_fcfdfd_1x100.png, /agilefant/static/js/backlogChooser.js, /agilefant/static/js/backlogSelector.js, /agilefant/static/js/date.js, /agilefant/static/js/jquery-ui.min.js, /agilefant/static/js/jquery.cookie.js, /agilefant/static/js/jquery.dynatree.js, /agilefant/static/js/jquery.hotkeys.js, /agilefant/static/js/jquery.js, /agilefant/static/js/jquery.wysiwyg.js]
  sub_correlation_list:
  - variable_name: payload_container
    item_count: 18
    variable_value_list: ['REQUEST_HEADERS:Host']
    sub_correlation_list:
    - variable_name: rule_id
      item_count: 18
      variable_value_list: ['960017']
  - variable_name: payload_container
    item_count: 18
    variable_value_list: ['REQUEST_HEADERS:Host']
    sub_correlation_list:
    - variable_name: rule_id
      item_count: 18
      variable_value_list: ['981174']
  - variable_name: payload_container
    item_count: 18
    variable_value_list: ['REQUEST_HEADERS:Host']
    sub_correlation_list:
    - variable_name: rule_id
      item_count: 18
      variable_value_list: ['981203']
- variable_name: request_file_name
  item_count: 4
  variable_value_list: [/agilefant/login.jsp]
  sub_correlation_list:
  - variable_name: rule_id
    item_count: 4
    variable_value_list: ['111111', '222222']
    sub_correlation_list:
    - variable_name: payload_container
      item_count: 4
      variable_value_list: ['ARGS:a', 'ARGS:b']
- variable_name: payload_container
  item_count: 1
  variable_value_list: ['TX:sqli_select_statement_count']
  sub_correlation_list:
  - variable_name: request_file_name
    item_count: 1
    variable_value_list: [/agilefant/static/js/backlogSelector.js]
    sub_correlation_list:
    - variable_name: rule_id
      item_count: 1
      variable_value_list: ['981317']
---
variable_name: request_file_name
item_count: 8
variable_value_list: [/agilefant/login.jsp]
sub_correlation_list:
- variable_name: rule_id
  item_count: 8
  variable_value_list: ['111111', '222222']
  sub_correlation_list:
  - variable_name: payload_container
    item_count: 8
    variable_value_list: ['ARGS:a', 'ARGS:b']
"""

        self._expected_output = u"""\
# Hit Count: 656
SecRule HOSTNAME "!@rx ^(1\.1\.1\.1|www\.shookalabs\.com)$" "id:10000,t:none,nolog,pass,skipAfter:1"
    # Hit Count: 651
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/ajax\/iterationData\.action|\/agilefant\/ajax\/myAssignmentsMenuData\.action|\/agilefant\/dailyWork\.action|\/agilefant\/drawIterationBurndown\.action|\/agilefant\/drawSmallIterationBurndown\.action|\/agilefant\/static\/css\/main\.css|\/agilefant\/static\/img\/backlog\.png|\/agilefant\/static\/img\/button\_fade\.png|\/agilefant\/static\/img\/dailyWork\.png|\/agilefant\/static\/img\/dynatree\/ltL\_ne\.gif|\/agilefant\/static\/img\/dynatree\/ltL\_nes\.gif|\/agilefant\/static\/img\/dynatree\/ltL\_ns\.gif|\/agilefant\/static\/img\/dynatree\/ltM\_ne\.gif|\/agilefant\/static\/img\/dynatree\/ltM\_nes\.gif|\/agilefant\/static\/img\/dynatree\/ltP\_ne\.gif|\/agilefant\/static\/img\/dynatree\/ltP\_nes\.gif|\/agilefant\/static\/img\/dynatree\/ltWait\.gif|\/agilefant\/static\/img\/favicon\.png|\/agilefant\/static\/img\/filter\.png|\/agilefant\/static\/img\/info\.png|\/agilefant\/static\/img\/labelIcon\.png|\/agilefant\/static\/img\/open\_close\.png|\/agilefant\/static\/img\/pleasewait\.gif|\/agilefant\/static\/img\/portfolio\.png|\/agilefant\/static\/img\/search\_small\.png|\/agilefant\/static\/img\/settings\.png|\/agilefant\/static\/img\/sort\.png|\/agilefant\/static\/img\/team\.png|\/agilefant\/static\/img\/timesheets\.png|\/agilefant\/static\/img\/toggle\.png|\/agilefant\/static\/img\/top\-logo\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_glass\_85\_dfeffc\_1x400\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_gloss\-wave\_55\_333333\_500x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_gloss\-wave\_55\_5c9ccc\_500x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_inset\-hard\_100\_f5f8f9\_1x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_inset\-hard\_100\_fcfdfd\_1x100\.png|\/agilefant\/static\/img\/ui\/ui\-icons\_6da8d5\_256x240\.png|\/agilefant\/static\/img\/ui\/ui\-icons\_f9bd01\_256x240\.png|\/agilefant\/static\/js\/autocomplete\/autocompleteBundle\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteDataProvider\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteDialog\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteInline\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteRecent\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteSearchBox\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteSelectedBox\.js|\/agilefant\/static\/js\/autocomplete\/autocompleteSingleDialog\.js|\/agilefant\/static\/js\/backlogChooser\.js|\/agilefant\/static\/js\/backlogSelector\.js|\/agilefant\/static\/js\/date\.js|\/agilefant\/static\/js\/dynamics\/Dynamics\.events\.js|\/agilefant\/static\/js\/dynamics\/controller\/AdministrationMenuController\.js|\/agilefant\/static\/js\/dynamics\/controller\/AssignmentController\.js|\/agilefant\/static\/js\/dynamics\/controller\/BacklogController\.js|\/agilefant\/static\/js\/dynamics\/controller\/CommonController\.js|\/agilefant\/static\/js\/dynamics\/controller\/CreateDialog\.js|\/agilefant\/static\/js\/dynamics\/controller\/DailyWorkController\.js|\/agilefant\/static\/js\/dynamics\/controller\/DailyWorkStoryListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/DailyWorkTasksWithoutStoryController\.js|\/agilefant\/static\/js\/dynamics\/controller\/HourEntryController\.js|\/agilefant\/static\/js\/dynamics\/controller\/HourEntryListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/IterationController\.js|\/agilefant\/static\/js\/dynamics\/controller\/IterationRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/MenuController\.js|\/agilefant\/static\/js\/dynamics\/controller\/MyAssignmentsMenuController\.js|\/agilefant\/static\/js\/dynamics\/controller\/PageController\.js|\/agilefant\/static\/js\/dynamics\/controller\/PersonalLoadController\.js|\/agilefant\/static\/js\/dynamics\/controller\/PortfolioController\.js|\/agilefant\/static\/js\/dynamics\/controller\/PortfolioRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/ProductController\.js|\/agilefant\/static\/js\/dynamics\/controller\/ProjectController\.js|\/agilefant\/static\/js\/dynamics\/controller\/ProjectRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/StoryController\.js|\/agilefant\/static\/js\/dynamics\/controller\/StoryInfoBubble\.js|\/agilefant\/static\/js\/dynamics\/controller\/StoryListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/StoryTreeController\.js|\/agilefant\/static\/js\/dynamics\/controller\/TaskController\.js|\/agilefant\/static\/js\/dynamics\/controller\/TaskInfoDialog\.js|\/agilefant\/static\/js\/dynamics\/controller\/TaskSplitDialog\.js|\/agilefant\/static\/js\/dynamics\/controller\/TasksWithoutStoryController\.js|\/agilefant\/static\/js\/dynamics\/controller\/TeamListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/TeamRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/UserController\.js|\/agilefant\/static\/js\/dynamics\/controller\/UserListController\.js|\/agilefant\/static\/js\/dynamics\/controller\/UserRowController\.js|\/agilefant\/static\/js\/dynamics\/controller\/WorkQueueController\.js|\/agilefant\/static\/js\/dynamics\/model\/AssignmentModel\.js|\/agilefant\/static\/js\/dynamics\/model\/BacklogModel\.js|\/agilefant\/static\/js\/dynamics\/model\/CommonModel\.js|\/agilefant\/static\/js\/dynamics\/model\/DailyWorkModel\.js|\/agilefant\/static\/js\/dynamics\/model\/HourEntryListContainer\.js|\/agilefant\/static\/js\/dynamics\/model\/HourEntryModel\.js|\/agilefant\/static\/js\/dynamics\/model\/IterationModel\.js|\/agilefant\/static\/js\/dynamics\/model\/LabelModel\.js|\/agilefant\/static\/js\/dynamics\/model\/ModelFactory\.js|\/agilefant\/static\/js\/dynamics\/model\/PortfolioModel\.js|\/agilefant\/static\/js\/dynamics\/model\/ProductModel\.js|\/agilefant\/static\/js\/dynamics\/model\/ProjectModel\.js|\/agilefant\/static\/js\/dynamics\/model\/StoryModel\.js|\/agilefant\/static\/js\/dynamics\/model\/TaskModel\.js|\/agilefant\/static\/js\/dynamics\/model\/TaskSplitContainer\.js|\/agilefant\/static\/js\/dynamics\/model\/TeamListContainer\.js|\/agilefant\/static\/js\/dynamics\/model\/TeamModel\.js|\/agilefant\/static\/js\/dynamics\/model\/UserListContainer\.js|\/agilefant\/static\/js\/dynamics\/model\/UserModel\.js|\/agilefant\/static\/js\/dynamics\/model\/WorkQueueTaskModel\.js|\/agilefant\/static\/js\/dynamics\/model\/comparators\.js|\/agilefant\/static\/js\/dynamics\/view\/Bubble\.js|\/agilefant\/static\/js\/dynamics\/view\/Cell\.js|\/agilefant\/static\/js\/dynamics\/view\/ChangePasswordDialog\.js|\/agilefant\/static\/js\/dynamics\/view\/CommonFragmentSubView\.js|\/agilefant\/static\/js\/dynamics\/view\/CommonSubView\.js|\/agilefant\/static\/js\/dynamics\/view\/ConfirmationDialog\.js|\/agilefant\/static\/js\/dynamics\/view\/DynamicView\.js|\/agilefant\/static\/js\/dynamics\/view\/LazyLoadedDialog\.js|\/agilefant\/static\/js\/dynamics\/view\/MessageDisplay\.js|\/agilefant\/static\/js\/dynamics\/view\/MultiEditWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/Row\.js|\/agilefant\/static\/js\/dynamics\/view\/SearchByTextWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/SpentEffortWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/StateFilterWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/StoryFiltersView\.js|\/agilefant\/static\/js\/dynamics\/view\/Table\.js|\/agilefant\/static\/js\/dynamics\/view\/TableCaption\.js|\/agilefant\/static\/js\/dynamics\/view\/TableCellEditors\.js|\/agilefant\/static\/js\/dynamics\/view\/TableConfiguration\.js|\/agilefant\/static\/js\/dynamics\/view\/UserSpentEffortWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/ValidationManager\.js|\/agilefant\/static\/js\/dynamics\/view\/ViewPart\.js|\/agilefant\/static\/js\/dynamics\/view\/decorators\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/AutoSuggest\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/Button\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/Buttons\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/CellBubble\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/LabelsIcon\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/LabelsView\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/RowActions\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/SplitPanel\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/StoryInfoWidget\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/Tabs\.js|\/agilefant\/static\/js\/dynamics\/view\/subviews\/Toggle\.js|\/agilefant\/static\/js\/jquery\-ui\.min\.js|\/agilefant\/static\/js\/jquery\.autoSuggest\.minified\.js|\/agilefant\/static\/js\/jquery\.cookie\.js|\/agilefant\/static\/js\/jquery\.dynatree\.js|\/agilefant\/static\/js\/jquery\.hotkeys\.js|\/agilefant\/static\/js\/jquery\.js|\/agilefant\/static\/js\/jquery\.jstree\.js|\/agilefant\/static\/js\/jquery\.labelify\.js|\/agilefant\/static\/js\/jquery\.tagcloud\.min\.js|\/agilefant\/static\/js\/jquery\.tooltip\.js|\/agilefant\/static\/js\/jquery\.wysiwyg\.js|\/agilefant\/static\/js\/utils\/ArrayUtils\.js|\/agilefant\/static\/js\/utils\/ClassUtils\.js|\/agilefant\/static\/js\/utils\/HelpUtils\.js|\/agilefant\/static\/js\/utils\/Parsers\.js|\/agilefant\/static\/js\/utils\/XworkSerializer\.js|\/agilefant\/static\/js\/utils\/aef\.jstree\.plugin\.js|\/agilefant\/static\/js\/utils\/menuTimer\.js|\/agilefant\/static\/js\/utils\/quickSearch\.js|\/agilefant\/static\/js\/utils\/refLinkDisplay\.js)$" "id:10001,t:none,nolog,pass,skipAfter:2"
        # Hit Count: 217
        SecAction "id:10002,t:none,nolog,pass,ctl:'ruleRemoveById=960017'"
        # Hit Count: 217
        SecAction "id:10003,t:none,nolog,pass,ctl:'ruleRemoveById=981174'"
        # Hit Count: 217
        SecAction "id:10004,t:none,nolog,pass,ctl:'ruleRemoveById=981203'"
    SecMarker EXCEPTION_2

    # Hit Count: 5
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/drawIterationBurndown\.action|\/agilefant\/static\/img\/top\-logo\.png|\/agilefant\/static\/js\/autocomplete\/autocompleteSelectedBox\.js|\/agilefant\/static\/js\/backlogSelector\.js)$" "id:10005,t:none,nolog,pass,skipAfter:3"
        # Hit Count: 5
        SecAction "id:10006,t:none,nolog,pass,ctl:'ruleRemoveById=981317'"
    SecMarker EXCEPTION_3

SecMarker EXCEPTION_1

# Hit Count: 59
SecRule HOSTNAME "!@rx ^(test\.domain\.com)$" "id:10007,t:none,nolog,pass,skipAfter:4"
    # Hit Count: 54
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/editIteration\.action|\/agilefant\/login\.jsp|\/agilefant\/static\/css\/main\.css|\/agilefant\/static\/img\/agilefant\-logo\-80px\.png|\/agilefant\/static\/img\/login\_gradient\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_gloss\-wave\_55\_5c9ccc\_500x100\.png|\/agilefant\/static\/img\/ui\/ui\-bg\_inset\-hard\_100\_fcfdfd\_1x100\.png|\/agilefant\/static\/js\/backlogChooser\.js|\/agilefant\/static\/js\/backlogSelector\.js|\/agilefant\/static\/js\/date\.js|\/agilefant\/static\/js\/jquery\-ui\.min\.js|\/agilefant\/static\/js\/jquery\.cookie\.js|\/agilefant\/static\/js\/jquery\.dynatree\.js|\/agilefant\/static\/js\/jquery\.hotkeys\.js|\/agilefant\/static\/js\/jquery\.js|\/agilefant\/static\/js\/jquery\.wysiwyg\.js)$" "id:10008,t:none,nolog,pass,skipAfter:5"
        # Hit Count: 18
        SecAction "id:10009,t:none,nolog,pass,ctl:'ruleRemoveById=960017'"
        # Hit Count: 18
        SecAction "id:10010,t:none,nolog,pass,ctl:'ruleRemoveById=981174'"
        # Hit Count: 18
        SecAction "id:10011,t:none,nolog,pass,ctl:'ruleRemoveById=981203'"
    SecMarker EXCEPTION_5

    # Hit Count: 4
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/login\.jsp)$" "id:10012,t:none,nolog,pass,skipAfter:6"
        # Hit Count: 4
        SecAction "id:10013,t:none,nolog,pass,ctl:'ruleRemoveById=111111,222222'"
    SecMarker EXCEPTION_6

    # Hit Count: 1
    SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/static\/js\/backlogSelector\.js)$" "id:10014,t:none,nolog,pass,skipAfter:7"
        # Hit Count: 1
        SecAction "id:10015,t:none,nolog,pass,ctl:'ruleRemoveById=981317'"
    SecMarker EXCEPTION_7

SecMarker EXCEPTION_4

# Hit Count: 8
SecRule REQUEST_FILENAME "!@rx ^(\/agilefant\/login\.jsp)$" "id:10016,t:none,nolog,pass,skipAfter:8"
    # Hit Count: 8
    SecAction "id:10017,t:none,nolog,pass,ctl:'ruleRemoveById=111111,222222'"
SecMarker EXCEPTION_8

"""

    def test_write(self):
        correlation_iterable = CorrelationSerializerYaml().load(StringIO(self._correlation_yaml_data))

        output = StringIO()
        ModsecurityExcetionWriter(stream = output).write(correlation_iterable)
        self.assertEqual(self._expected_output, output.getvalue())
