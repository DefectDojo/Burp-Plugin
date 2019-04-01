from burp import IBurpExtender
from thread import start_new_thread
from burp import ITab
from burp import IContextMenuFactory
from burp import IContextMenuInvocation
from burp import IScanIssue
from java.awt import Component
from java.awt import Dimension
from java.io import PrintWriter
from java.awt.event import ActionListener
from java.awt.event import MouseAdapter
import javax.swing.AbstractAction
from java.util import ArrayList
import javax.swing.Action
from java.util import List
from javax.swing import JScrollPane
from javax.swing import JSplitPane
from javax.swing import JTabbedPane
from javax.swing import JTable
from javax.swing import JPanel
from javax.swing import JLabel
from javax.swing import JMenuItem
from javax.swing import DefaultListModel
from javax.swing import JList
from javax.swing import JTextField
from javax.swing import JComboBox
from javax.swing import JButton
from javax.swing import JMenu
from javax.swing import SwingUtilities
from javax.swing.table import AbstractTableModel
import ssl
import json
import httplib


class ProdListener(ActionListener):
    """
    Updates the productID field based on the selection from the ComboBox
    """

    def __init__(self, data):
        self.a = data

    def actionPerformed(self, e):
        cmd = e.getActionCommand()
        if cmd == 'comboBoxChanged':
            selected = self.a._productName.selectedIndex
            if selected >= 0:
                self.a._productID.setText(
                    str(self.a.products.data['objects'][selected]['id']))


class EngListener(ActionListener):
    """
    Updates the engagementID field based on the selection from the ComboBox
    """

    def __init__(self, data):
        self.a = data

    def actionPerformed(self, e):
        cmd = e.getActionCommand()
        if cmd == 'comboBoxChanged':
            selected = self.a._engagementName.selectedIndex
            if selected >= 0:
                self.a._engagementID.setText(
                    str(self.a.engagements.data['objects'][selected]['id']))


class TestListener(ActionListener):
    """
    Updates the testID field based on the selection from the ComboBox
    """

    def __init__(self, data):
        self.a = data

    def actionPerformed(self, e):
        cmd = e.getActionCommand()
        if cmd == 'comboBoxChanged':
            selected = self.a._testName.selectedIndex
            if selected >= 0:
                self.a._testID.setText(
                    str(self.a.tests.data['objects'][selected]['id']))


class IssListener(MouseAdapter):
    """
    Listener used to update the list of issues in the Defect Dojo tab when a target is double clicked
    """

    def __init__(self, data):
        self.a = data

    def mouseClicked(self, e):
        cmd = e.getClickCount()
        if cmd == 2:
            self.a.issNames.removeAllElements()
            del self.a._issList[:]
            for i in self.a._callbacks.getScanIssues(self.a._listTargets.getSelectedValue()):
                self.a._issList.append(i)
            for i in self.a._issList:
                self.a.issNames.addElement(i.getIssueName())


class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Defect Dojo")
        self._panel = JPanel()
        self._panel.setLayout(None)
        self._panel.setPreferredSize(Dimension(1368, 1368))
        self._labelDojoURL = JLabel("Defect Dojo :")
        self._labelDojoURL.setBounds(15, 15, 100, 30)
        self._defectDojoURL = JTextField("https://defectdojo.herokuapp.com")
        self._defectDojoURL.setBounds(105, 15, 155, 30)
        self._labelApiKey = JLabel("API Key :")
        self._labelApiKey.setBounds(15, 45, 100, 30)
        self._apiKey = JTextField(
            "1dfdfa2042567ec751f6b3fa96038b743ea6f1cc")
        self._apiKey.setBounds(105, 45, 155, 30)
        self._labelUsername = JLabel("Username :")
        self._labelUsername.setBounds(265, 15, 100, 30)
        self._user = JTextField("admin")
        self._user.setBounds(370, 15, 100, 30)
        self._labelProductID = JLabel("Product ID :")
        self._labelProductID.setBounds(15, 75, 125, 30)
        self._productID = JTextField(actionPerformed=self.getEngagements)
        self._productID.setBounds(105, 75, 50, 30)
        self._labelProductName = JLabel("Product Name :")
        self._labelProductName.setBounds(265, 45, 100, 30)
        self._productName = JComboBox()
        self._productName.setBounds(370, 45, 100, 30)
        self._labelEngagementID = JLabel("Engagement ID :")
        self._labelEngagementID.setBounds(15, 100, 125, 30)
        self._engagementID = JTextField(40, actionPerformed=self.getTests)
        self._engagementID.setBounds(105, 105, 50, 30)
        self._labelTestID = JLabel("Test ID :")
        self._labelTestID.setBounds(15, 135, 125, 30)
        self._testID = JTextField()
        self._testID.setBounds(105, 135, 50, 30)
        self._testName = JComboBox()
        self._testName.setBounds(160, 135, 300, 30)
        self._labelSearch = JLabel("Search Product :")
        self._labelSearch.setBounds(160, 75, 100, 30)
        self.prodMan = ProdListener(self)
        self.engMan = EngListener(self)
        self.testMan = TestListener(self)
        self._engagementName = JComboBox()
        self._engagementName.setBounds(160, 105, 300, 30)
        self._productName.addActionListener(self.prodMan)
        self._engagementName.addActionListener(self.engMan)
        self._testName.addActionListener(self.testMan)
        self._search = JTextField(40)
        self._search.setBounds(265, 75, 100, 30)
        self._searchProductButton = JButton(
            'Search Product', actionPerformed=self.getProducts)
        self._searchProductButton.setBounds(370, 75, 100, 30)
        self._sendIssueButton = JButton(
            'Send Issue', actionPerformed=self.sendIssue)
        self._sendIssueButton.setBounds(465, 135, 100, 30)
        self._targets = self._callbacks.getSiteMap(None)
        self._tgts = DefaultListModel()
        tgts = set([])
        for i, resps in enumerate(self._targets):
            tgts.add(str(resps.getHttpService()))
        tgts = list(tgts)
        for targets in tgts:
            self._tgts.addElement(targets)
        self._listTargets = JList(self._tgts)
        self.issMan = IssListener(self)
        self._listTargets.addMouseListener(self.issMan)
        self._issList = []
        self.issNames = DefaultListModel()
        self._listTargetIss = JList(self.issNames)
        self._scrollList = JScrollPane(self._listTargets)
        self._listTargets.setBounds(15, 175, 300, 100)
        self._scrollList.setBounds(15, 175, 300, 100)
        self._targetsRefButton = JButton(
            'Refresh Targets', actionPerformed=self.refTargets)
        self._targetsRefButton.setBounds(15, 275, 100, 30)
        self._scrollIssList = JScrollPane(self._listTargetIss)
        self._listTargetIss.setBounds(325, 175, 300, 100)
        self._scrollIssList.setBounds(325, 175, 300, 100)
        self._panel.add(self._labelDojoURL)
        self._panel.add(self._defectDojoURL)
        self._panel.add(self._scrollList)
        self._panel.add(self._targetsRefButton)
        self._panel.add(self._scrollIssList)
        self._panel.add(self._labelApiKey)
        self._panel.add(self._apiKey)
        self._panel.add(self._labelProductID)
        self._panel.add(self._productID)
        self._panel.add(self._testName)
        self._panel.add(self._labelUsername)
        self._panel.add(self._user)
        self._panel.add(self._labelProductName)
        self._panel.add(self._productName)
        self._panel.add(self._engagementName)
        self._panel.add(self._labelEngagementID)
        self._panel.add(self._engagementID)
        self._panel.add(self._labelTestID)
        self._panel.add(self._testID)
        self._panel.add(self._sendIssueButton)
        self._panel.add(self._search)
        self._panel.add(self._searchProductButton)
        self._panel.add(self._labelSearch)
        self.sender = HttpData(self._defectDojoURL.getText(
        ), self._user.getText(), self._apiKey.getText())
        self.contextMenu = SendToDojo(self)
        callbacks.registerContextMenuFactory(self.contextMenu)
        callbacks.customizeUiComponent(self._panel)
        callbacks.addSuiteTab(self)
        return

    def getTabCaption(self):
        return "Defect Dojo"

    def refTargets(self, event):
        """
        Refreshes the list of targets displayed in the Defect Dojo tab
        """
        self._tgts.removeAllElements()
        self._targets = self._callbacks.getSiteMap(None)
        tgts = set([])
        for i, resps in enumerate(self._targets):
            tgts.add(str(resps.getHttpService()))
        tgts = list(tgts)
        for targets in tgts:
            self._tgts.addElement(targets)

    def getUiComponent(self):
        return self._panel

    def getProducts(self, event):
        """
        Updates the list of products from the API , and also makes the call to retreive the userId behind the scenes .
        """
        self._productName.removeAllItems()
        self.checkUpdateSender()
        start_new_thread(self.doGetProducts, ())

    def doGetProducts(self):
        self.sender.makeRequest(
            'GET', '/api/v1/products/?name__icontains='+self._search.getText())
        data = self.sender.req_data
        test = DefectDojoResponse(
            message="Done", data=json.loads(data), success=True)
        self.products = test
        for objects in test.data['objects']:
            self._productName.addItem(objects['name'])
        start_new_thread(self.getUserId, ())

    def getEngagements(self, event):
        """
        Updates the list of engagements from the API
        """
        self._engagementName.removeAllItems()
        self.checkUpdateSender()
        start_new_thread(self.doGetEngagements, ())

    def doGetEngagements(self):
        self.sender.makeRequest('GET', '/api/v1/engagements/?product=' +
                                self._productID.getText()+'&status=In%20Progress')
        data = self.sender.req_data
        test = DefectDojoResponse(
            message="Done", data=json.loads(data), success=True)
        self.engagements = test
        for objects in test.data['objects']:
            self._engagementName.addItem(objects['name'])

    def getTests(self, event):
        """
        Updates the list containing test names based on test_type+date created so that there is some visual indicator .
        """
        self._testName.removeAllItems()
        self.checkUpdateSender()
        start_new_thread(self.doGetTests, ())

    def doGetTests(self):
        self.sender.makeRequest('GET', '/api/v1/tests/?engagement=' +
                                self._engagementID.getText())
        data = self.sender.req_data
        test = DefectDojoResponse(
            message="Done", data=json.loads(data), success=True)
        self.tests = test
        for objects in test.data['objects']:
            self._testName.addItem(objects['test_type']+objects['created'])

    def getUserId(self):
        self.sender.makeRequest('GET', '/api/v1/users/')
        data = self.sender.req_data
        test = DefectDojoResponse(
            message="Done", data=json.loads(data), success=True)
        for objects in test.data['objects']:
            if self._user.getText() == objects['username']:
                self._userID = objects['id']

    def sendIssue(self, event):
        """
        This sends a single issue to Defect Dojo be it selected from the Defect Dojo Tab or the Context Menu in the Target Tab .
        Due to the current limitations in Defect Dojo API request/response pairs cannot be added *yet* .
        """
        ureqresp = []
        if event.getActionCommand() == 'Send To Defect Dojo':
            title = self.contextMenu._invoker.getSelectedIssues()[
                0].getIssueName()
            description = self.contextMenu._invoker.getSelectedIssues()[
                0].getIssueDetail()
            severity = self.contextMenu._invoker.getSelectedIssues()[
                0].getSeverity()
            impact = self.contextMenu._invoker.getSelectedIssues()[
                0].getIssueBackground()
            mitigation = self.contextMenu._invoker.getSelectedIssues()[
                0].getRemediationBackground()+'\n'
            if self.contextMenu._invoker.getSelectedIssues()[0].getRemediationDetail():
                mitigation += self.contextMenu._invoker.getSelectedIssues()[
                    0].getRemediationDetail()
            for mess in self.contextMenu._invoker.getSelectedIssues()[0].getHttpMessages():
                ureqresp.append({"req": self._helpers.bytesToString(mess.getRequest()),
                                 "resp": self._helpers.bytesToString(mess.getResponse())})
        elif event.getActionCommand() == 'Send Issue':
            title = self._issList[self._listTargetIss.getSelectedIndex(
            )].getIssueName()
            description = self._issList[self._listTargetIss.getSelectedIndex(
            )].getIssueDetail()
            severity = self._issList[self._listTargetIss.getSelectedIndex(
            )].getSeverity()
            impact = self._issList[self._listTargetIss.getSelectedIndex(
            )].getIssueBackground()
            mitigation = self._issList[self._listTargetIss.getSelectedIndex(
            )].getRemediationBackground()+'\n'
            if self._issList[self._listTargetIss.getSelectedIndex()].getRemediationDetail():
                mitigation += self._issList[self._listTargetIss.getSelectedIndex()
                                            ].getRemediationDetail()
            for mess in self._issList[self._listTargetIss.getSelectedIndex(
            )].getHttpMessages():
                ureqresp.append({"req": self._helpers.bytesToString(mess.getRequest()),
                                 "resp": self._helpers.bytesToString(mess.getResponse())})
        data = {
            'title': title,
            'description': description,
            'severity': severity,
            'product': '/api/v1/products/'+self._productID.getText()+'/',
            'engagement': '/api/v1/engagements/'+self._engagementID.getText()+'/',
            'reporter': '/api/v1/users/'+str(self._userID)+'/',
            'test': '/api/v1/tests/'+self._testID.getText()+'/',
            'impact': impact,
            'active': True,
            'verified': True,
            'mitigation': mitigation,
            'static_finding': False,
            'dynamic_finding': False
            # 'steps_to_reproduce': ureqresp
        }
        data = json.dumps(data)
        self.checkUpdateSender()
        start_new_thread(self.sender.makeRequest,
                         ('POST', '/api/v1/findings/', data))

    def checkUpdateSender(self):
        if self.sender.ddurl != self._defectDojoURL.getText().lower().split('://'):
            self.sender.setUrl(self._defectDojoURL.getText())
        if self.sender.user != self._user.getText():
            self.sender.setUser(self._user.getText())
        if self.sender.apikey != self._apiKey.getText():
            self.sender.setApiKey(self._apiKey.getText())


class HttpData():
    req_data = ''
    ddurl = ''
    user = ''
    apikey = ''

    def __init__(self, ddurl, user, apikey):
        self.ddurl = ddurl.lower().split('://')
        self.user = user
        self.apikey = apikey

    def setUrl(self, ddurl):
        self.ddurl = ddurl.lower().split('://')

    def setApiKey(self, apikey):
        self.apikey = apikey

    def setUser(self, user):
        self.user = user

    def makeRequest(self, method, url, data=None):
        if self.ddurl[0] == 'http':
            conn = httplib.HTTPConnection(self.ddurl[1])
        elif self.ddurl[0] == 'https':
            conn = httplib.HTTPSConnection(self.ddurl[1])
        else:
            return None
        headers = {
            'User-Agent': 'Testing',
            'Authorization': "ApiKey " + self.user + ":" + self.apikey
        }
        if data:
            conn.request(method, url, body=data, headers=headers)
        else:
            conn.request(method, url, headers=headers)
        response = conn.getresponse()
        self.req_data = response.read()
        conn.close()
        return


class SendToDojo(IContextMenuFactory):
    """
    SendToDojo implements the class needed to create the context menu when rightclicking an issue .
    """

    def __init__(self, data):
        self.a = data

    def createMenuItems(self, invoker):
        self._invoker = invoker
        context = self._invoker.getInvocationContext()
        if not context == self._invoker.CONTEXT_SCANNER_RESULTS:
            return None
        self.selection = JMenuItem(
            "Send To Defect Dojo", actionPerformed=self.a.sendIssue)
        return [self.selection]


class DefectDojoResponse(object):
    """
    Container for all DefectDojo API responses, even errors.
    """

    def __init__(self, message, success, data=None, response_code=-1):
        self.message = message
        self.data = data
        self.success = success
        self.response_code = response_code

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return self.message

    def id(self):
        if self.response_code == 400:  # Bad Request
            raise ValueError('Object not created:' + json.dumps(self.data,
                                                                sort_keys=True, indent=4, separators=(',', ': ')))
        return int(self.data)

    def count(self):
        return self.data["meta"]["total_count"]

    def data_json(self, pretty=False):
        """Returns the data as a valid JSON string."""
        if pretty:
            return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self.data)
