from burp import IBurpExtender
from thread import start_new_thread
from burp import ITab
from burp import IContextMenuFactory
from burp import IContextMenuInvocation
from burp import IScanIssue
from java.awt import Component
from java.awt import Dimension
from org.python.core.util import RelativeFile
from java.io import PrintWriter
from java.awt.event import ActionListener
from java.awt.event import MouseAdapter
import javax.swing.AbstractAction
from jarray import array
from java.util import ArrayList
import javax.swing.Action
from java.util import List
from javax.swing import JScrollPane, GroupLayout, LayoutStyle
from javax.swing import JSplitPane
from javax.swing import JTabbedPane
from javax.swing import JTable
from javax.swing import JPanel
from javax.swing import JLabel
from javax.swing import JMenuItem
from javax.swing import DefaultListModel
from javax.swing import JList, JOptionPane
from javax.swing import JTextField
from javax.swing import JComboBox
from javax.swing import JButton
from javax.swing import JMenu
from javax.swing import SwingUtilities
from javax.swing.table import AbstractTableModel
import random
import string
import ssl
import time
import json
import sys
import os
import httplib
from utils import EngListener, ProdListener, TestListener
from utils import SendReportToDojo, SendToDojo, html2text, ClickableLink

__author__ = 'Alexandru Dracea'


class DDTabUi():
    def __init__(self, ext):
        self._panel = JPanel()
        layout = GroupLayout(self._panel)
        innerPanel = JPanel()
        innerPanelLayout = GroupLayout(innerPanel)
        self._panel.setLayout(layout)
        innerPanel.setLayout(innerPanelLayout)
        self.labelDojoURL = JLabel("Defect Dojo :")
        self.defectDojoURL = JTextField("https://defectdojo.herokuapp.com")
        self.labelApiKey = JLabel("API Key :")
        self.apiKey = JTextField("1dfdfa2042567ec751f6b3fa96038b743ea6f1cc")
        self.labelUsername = JLabel("Username :")
        self.user = JTextField("admin")
        self.labelProductID = JLabel("Product :")
        self.productID = JTextField(focusLost=ext.getEngagements)
        self.labelProductName = JLabel("Product Name :")
        self.productName = JComboBox()
        self.prodMan = ProdListener(ext)
        self.productName.addActionListener(self.prodMan)
        self.labelEngagementID = JLabel("Engagement :")
        self.engagementID = JTextField(focusLost=ext.getTests)
        self.engagementName = JComboBox()
        self.engMan = EngListener(ext)
        self.engagementName.addActionListener(self.engMan)
        self.labelTestID = JLabel("Test :")
        self.testID = JTextField()
        self.testName = JComboBox()
        self.testMan = TestListener(ext)
        self.testName.addActionListener(self.testMan)
        self.search = JTextField()
        self.searchProductButton = JButton('Search Product',
                                           actionPerformed=ext.getProducts)
        innerPanelLayout.setHorizontalGroup(
            innerPanelLayout.createParallelGroup().addGroup(
                GroupLayout.Alignment.TRAILING,
                innerPanelLayout.createSequentialGroup().addContainerGap().
                addGroup(
                    innerPanelLayout.createParallelGroup(
                        GroupLayout.Alignment.TRAILING).
                    addGroup(innerPanelLayout.createParallelGroup().addGroup(
                        innerPanelLayout.createParallelGroup(
                            GroupLayout.Alignment.TRAILING).addGroup(
                                innerPanelLayout.createParallelGroup(
                                    GroupLayout.Alignment.TRAILING).addGroup(
                                        innerPanelLayout.createSequentialGroup(
                                        ).addComponent(
                                            self.labelUsername,
                                            GroupLayout.PREFERRED_SIZE, 168,
                                            GroupLayout.PREFERRED_SIZE).addGap(
                                                105, 105, 105)).
                                addComponent(self.labelProductName,
                                             GroupLayout.Alignment.LEADING,
                                             GroupLayout.PREFERRED_SIZE, 168,
                                             GroupLayout.PREFERRED_SIZE)).
                        addGroup(
                            GroupLayout.Alignment.LEADING,
                            innerPanelLayout.createSequentialGroup().addGroup(
                                innerPanelLayout.createParallelGroup(
                                    GroupLayout.Alignment.TRAILING).
                                addComponent(
                                    self.labelEngagementID,
                                    GroupLayout.Alignment.LEADING,
                                    GroupLayout.PREFERRED_SIZE, 168,
                                    GroupLayout.PREFERRED_SIZE).addComponent(
                                        self.labelDojoURL,
                                        GroupLayout.Alignment.LEADING,
                                        GroupLayout.PREFERRED_SIZE, 168,
                                        GroupLayout.PREFERRED_SIZE)).
                            addPreferredGap(
                                LayoutStyle.ComponentPlacement.RELATED))
                    ).addGroup(innerPanelLayout.createSequentialGroup(
                    ).addGroup(
                        innerPanelLayout.createParallelGroup().addComponent(
                            self.labelTestID, GroupLayout.PREFERRED_SIZE, 168,
                            GroupLayout.PREFERRED_SIZE).addComponent(
                                self.searchProductButton,
                                GroupLayout.PREFERRED_SIZE, 269,
                                GroupLayout.PREFERRED_SIZE)).addPreferredGap(
                                    LayoutStyle.ComponentPlacement.RELATED))).
                    addGroup(
                        GroupLayout.Alignment.LEADING,
                        innerPanelLayout.createSequentialGroup().addComponent(
                            self.labelApiKey, GroupLayout.PREFERRED_SIZE, 168,
                            GroupLayout.PREFERRED_SIZE).addPreferredGap(
                                LayoutStyle.ComponentPlacement.RELATED))).
                addGroup(innerPanelLayout.createParallelGroup().addGroup(
                    innerPanelLayout.createSequentialGroup().addComponent(
                        self.engagementID, GroupLayout.PREFERRED_SIZE, 36,
                        GroupLayout.PREFERRED_SIZE).addGap(
                            18, 18,
                            18).addComponent(self.engagementName,
                                             GroupLayout.PREFERRED_SIZE, 260,
                                             GroupLayout.PREFERRED_SIZE)
                ).addGroup(innerPanelLayout.createSequentialGroup().addGap(
                    54, 54, 54).addGroup(
                        innerPanelLayout.createParallelGroup().addComponent(
                            self.defectDojoURL, GroupLayout.PREFERRED_SIZE,
                            260, GroupLayout.PREFERRED_SIZE).addComponent(
                                self.apiKey, GroupLayout.PREFERRED_SIZE, 260,
                                GroupLayout.PREFERRED_SIZE).addComponent(
                                    self.user, GroupLayout.PREFERRED_SIZE, 260,
                                    GroupLayout.PREFERRED_SIZE).addComponent(
                                        self.productName,
                                        GroupLayout.PREFERRED_SIZE, 260,
                                        GroupLayout.PREFERRED_SIZE)
                    )).addGroup(
                        innerPanelLayout.createSequentialGroup().addComponent(
                            self.testID, GroupLayout.PREFERRED_SIZE, 36,
                            GroupLayout.PREFERRED_SIZE).addGap(18, 18, 18).
                        addGroup(innerPanelLayout.createParallelGroup(
                        ).addComponent(
                            self.search, GroupLayout.PREFERRED_SIZE, 260,
                            GroupLayout.PREFERRED_SIZE).addComponent(
                                self.testName, GroupLayout.PREFERRED_SIZE, 260,
                                GroupLayout.PREFERRED_SIZE)))).addGap(
                                    348, 348, 348)))
        innerPanelLayout.setVerticalGroup(innerPanelLayout.createParallelGroup(
        ).addGroup(innerPanelLayout.createSequentialGroup().addContainerGap(
        ).addGroup(
            innerPanelLayout.createParallelGroup(
                GroupLayout.Alignment.LEADING,
                False).addComponent(self.defectDojoURL).addComponent(
                    self.labelDojoURL, GroupLayout.DEFAULT_SIZE,
                    GroupLayout.DEFAULT_SIZE, sys.maxint)
        ).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(
            innerPanelLayout.createParallelGroup(
                GroupLayout.Alignment.BASELINE).addComponent(
                    self.apiKey, GroupLayout.PREFERRED_SIZE,
                    GroupLayout.DEFAULT_SIZE,
                    GroupLayout.PREFERRED_SIZE).addComponent(
                        self.labelApiKey, GroupLayout.PREFERRED_SIZE, 19,
                        GroupLayout.PREFERRED_SIZE)
        ).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(
            innerPanelLayout.createParallelGroup(
                GroupLayout.Alignment.BASELINE).addComponent(
                    self.user, GroupLayout.PREFERRED_SIZE,
                    GroupLayout.DEFAULT_SIZE,
                    GroupLayout.PREFERRED_SIZE).addComponent(
                        self.labelUsername, GroupLayout.PREFERRED_SIZE, 19,
                        GroupLayout.PREFERRED_SIZE)
        ).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(
            innerPanelLayout.createParallelGroup(
                GroupLayout.Alignment.BASELINE).addComponent(
                    self.productName, GroupLayout.PREFERRED_SIZE,
                    GroupLayout.DEFAULT_SIZE,
                    GroupLayout.PREFERRED_SIZE).addComponent(
                        self.labelProductName, GroupLayout.PREFERRED_SIZE, 19,
                        GroupLayout.PREFERRED_SIZE)
        ).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(
            innerPanelLayout.createParallelGroup(
                GroupLayout.Alignment.BASELINE).addComponent(
                    self.engagementName, GroupLayout.PREFERRED_SIZE,
                    GroupLayout.DEFAULT_SIZE,
                    GroupLayout.PREFERRED_SIZE).addComponent(
                        self.engagementID, GroupLayout.PREFERRED_SIZE,
                        GroupLayout.DEFAULT_SIZE,
                        GroupLayout.PREFERRED_SIZE).addComponent(
                            self.labelEngagementID, GroupLayout.PREFERRED_SIZE,
                            19, GroupLayout.PREFERRED_SIZE)
        ).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(
            innerPanelLayout.createParallelGroup(
                GroupLayout.Alignment.BASELINE).addComponent(
                    self.testName, GroupLayout.PREFERRED_SIZE,
                    GroupLayout.DEFAULT_SIZE,
                    GroupLayout.PREFERRED_SIZE).addComponent(
                        self.testID, GroupLayout.PREFERRED_SIZE,
                        GroupLayout.DEFAULT_SIZE,
                        GroupLayout.PREFERRED_SIZE).addComponent(
                            self.labelTestID, GroupLayout.PREFERRED_SIZE, 19,
                            GroupLayout.PREFERRED_SIZE)
        ).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(
            innerPanelLayout.createParallelGroup(
                GroupLayout.Alignment.LEADING, False).addComponent(
                    self.search, GroupLayout.DEFAULT_SIZE,
                    GroupLayout.DEFAULT_SIZE, sys.maxint).addComponent(
                        self.searchProductButton)).addContainerGap(
                            131, sys.maxint)))
        layout.setHorizontalGroup(layout.createParallelGroup().addGroup(
            layout.createSequentialGroup().addComponent(
                innerPanel, GroupLayout.PREFERRED_SIZE, 633,
                GroupLayout.PREFERRED_SIZE).addGap(0, 312, sys.maxint)))
        layout.setVerticalGroup(layout.createParallelGroup().addGroup(
            layout.createSequentialGroup().addComponent(
                innerPanel, GroupLayout.PREFERRED_SIZE,
                GroupLayout.DEFAULT_SIZE,
                GroupLayout.PREFERRED_SIZE).addGap(0, 199, sys.maxint)))


class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Defect Dojo")
        self.ddui = DDTabUi(self)
        self.sender = HttpData(self.ddui.defectDojoURL.getText(),
                               self.ddui.user.getText(),
                               self.ddui.apiKey.getText())
        self.contextMenu = SendToDojo(self)
        self.contextMenu2 = SendReportToDojo(self)
        callbacks.registerContextMenuFactory(self.contextMenu)
        callbacks.registerContextMenuFactory(self.contextMenu2)
        callbacks.customizeUiComponent(self.ddui._panel)
        callbacks.addSuiteTab(self)
        return

    def getTabCaption(self):
        return "Defect Dojo"

    def getUiComponent(self):
        return self.ddui._panel

    def getProducts(self, event):
        """
        Updates the list of products from the API , and also makes the call
        to retreive the userId behind the scenes .
        """
        self.ddui.productName.removeAllItems()
        start_new_thread(self.doGetProducts, ())

    def doGetProducts(self):
        self.checkUpdateSender()
        self.sender.makeRequest(
            'GET', '/api/v1/products/?name__icontains=' +
            self._helpers.urlEncode(self.ddui.search.getText()))
        data = self.sender.req_data
        test = DefectDojoResponse(message="Done",
                                  data=json.loads(data),
                                  success=True)
        self.ddui.products = test
        for objects in test.data['objects']:
            self.ddui.productName.addItem(objects['name'])
        start_new_thread(self.getUserId, ())

    def getEngagements(self, event):
        """
        Updates the list of engagements from the API
        """
        self.ddui.engagementName.removeAllItems()
        start_new_thread(self.doGetEngagements, ())

    def doGetEngagements(self):
        self.checkUpdateSender()
        self.sender.makeRequest(
            'GET', '/api/v1/engagements/?product=' +
            self._helpers.urlEncode(self.ddui.productID.getText()) +
            '&status=In%20Progress')
        data = self.sender.req_data
        test = DefectDojoResponse(message="Done",
                                  data=json.loads(data),
                                  success=True)
        self.ddui.engagements = test
        if test.data:
            for objects in test.data['objects']:
                self.ddui.engagementName.addItem(objects['name'])

    def getTests(self, event):
        """
        Updates the list containing test names based on test_type+date created
        so that there is some visual indicator .
        """
        self.ddui.testName.removeAllItems()
        self.checkUpdateSender()
        start_new_thread(self.doGetTests, ())

    def doGetTests(self):
        self.checkUpdateSender()
        self.sender.makeRequest(
            'GET', '/api/v1/tests/?engagement=' +
            self._helpers.urlEncode(self.ddui.engagementID.getText()))
        data = self.sender.req_data
        test = DefectDojoResponse(message="Done",
                                  data=json.loads(data),
                                  success=True)
        self.ddui.tests = test
        if test.data:
            for objects in test.data['objects']:
                self.ddui.testName.addItem(
                    str(objects['test_type']) + str(objects['created']))

    def getUserId(self):
        self.checkUpdateSender()
        self.sender.makeRequest('GET', '/api/v1/users/')
        data = self.sender.req_data
        test = DefectDojoResponse(message="Done",
                                  data=json.loads(data),
                                  success=True)
        for objects in test.data['objects']:
            if self.ddui.user.getText() == objects['username']:
                self.ddui.userID = objects['id']

    def sendAsReport(self, event):
        """
        This sends selected issues(>=1) to Defect Dojo bundled as a report ,
        this will mean that they will be imported into a new test each time .
        """
        if hasattr(self.ddui, 'userID'):
            pass
        else:
            self.getUserId()
        f = RelativeFile("Scan.xml")
        f.createNewFile()
        if event.getActionCommand() == "Send All Issues to Defect Dojo":
            ctr = 0
            for urls in self.contextMenu._invoker.getSelectedMessages():
                url = ""
                if urls.getHttpService().getProtocol(
                ) == 'http' and urls.getHttpService().getPort() == 80:
                    url_loc = str(urls.getUrl()).split('/')
                    url_loc = '/'.join(url_loc[3:])
                    url = "http://" + urls.getHttpService().getHost(
                    ) + '/' + url_loc
                elif urls.getHttpService().getProtocol(
                ) == 'https' and urls.getHttpService().getPort() == 443:
                    url_loc = str(urls.getUrl()).split('/')
                    url_loc = '/'.join(url_loc[3:])
                    url = "https://" + urls.getHttpService().getHost(
                    ) + '/' + url_loc
                else:
                    url = str(urls.getUrl())
                if ctr == 0:
                    issues = self._callbacks.getScanIssues(url)
                    ctr += 1
                else:
                    for iss in self._callbacks.getScanIssues(url):
                        issues.append(iss)
                    ctr += 1
            self._callbacks.generateScanReport("XML", issues, f)
        else:
            self._callbacks.generateScanReport(
                "XML", self.contextMenu._invoker.getSelectedIssues(), f)
        ct_boundry = ''.join(random.SystemRandom().choice(string.hexdigits)
                             for _ in range(30))
        self.sender.headers[
            'Content-Type'] = 'multipart/form-data; boundary=----------' \
            + ct_boundry
        import datetime
        now = datetime.datetime.now()
        content = {
            'build_id':
            "",
            "minimum_severity":
            "Info",
            "scan_date":
            "%d-%d-%d" % (now.year, now.month, now.day),
            "tags":
            "BurpPlugin",
            "active":
            "true",
            "verified":
            "true",
            "engagement":
            '/api/v1/engagements/' +
            self._helpers.urlEncode(self.ddui.engagementID.getText()) + '/',
            'scan_type':
            'Burp Scan'
        }
        nl = '\r\n'
        data = []
        for (key, value) in content.iteritems():
            data.append('------------' + ct_boundry)
            data.append('Content-Disposition: form-data; name="%s";' % (key))
            data.append('')
            data.append(value)
        data.append('------------' + ct_boundry)
        data.append(
            'Content-Disposition: form-data;name="file"; filename="Scan.xml";')
        data.append('Content-Type: application/xml')
        data.append('')
        with open("./Scan.xml") as a:
            for line in a:
                data.append(line.encode('utf8', 'replace'))
        os.remove("./Scan.xml")
        data.append('------------' + ct_boundry + '--')
        body_s = nl.join(data)
        data2 = open("./Data.txt", "w")
        data2.write(body_s)
        data2.close()
        data2 = open('./Data.txt', "r")
        self.checkUpdateSender()
        start_new_thread(self.sender.makeRequest,
                         ('POST', '/api/v1/importscan/', data2,
                          self.getUiComponent().parent))

    def sendIssue(self, event):
        """
        This sends selected issues(>=1) to Defect Dojo be they selected from
        the Defect Dojo Tab or the Context Menu in the Target Tab .
        Due to the current limitations in Defect Dojo API request/response
        pairs cannot be added *yet* .
        """
        if hasattr(self.ddui, 'userID'):
            pass
        else:
            self.getUserId()
        if event.getActionCommand() == 'Send To Defect Dojo':
            lgt = len(self.contextMenu._invoker.getSelectedIssues())
            issues = self.contextMenu._invoker.getSelectedIssues()
        elif event.getActionCommand() == 'Send Issue':
            lgt = len(self.ddui._listTargetIss.getSelectedIndices())
            issues = self.ddui._listTargetIss.getSelectedIndices()
        for i in range(lgt):
            ureqresp = []
            if event.getActionCommand() == 'Send To Defect Dojo':
                title = issues[i].getIssueName()
                description = issues[i].getIssueDetail(
                ) if issues[i].getIssueDetail(
                ) else issues[i].getIssueBackground()
                severity = issues[i].getSeverity()
                if severity == 'Information' or severity == 'Informational':
                    severity = "Info"
                impact = issues[i].getIssueBackground()
                if issues[i].getRemediationBackground():
                    mitigation = issues[i].getRemediationBackground() + '\n'
                    if issues[i].getRemediationDetail():
                        mitigation += issues[i].getRemediationDetail()
                else:
                    mitigation = str(issues[i].getIssueType())
                for mess in issues[i].getHttpMessages():
                    ureqresp.append({
                        "req":
                        self._helpers.bytesToString(mess.getRequest()),
                        "resp":
                        self._helpers.bytesToString(mess.getResponse())
                    })
                url = str(issues[i].getUrl())
            description = html2text(description)
            impact = html2text(impact)
            mitigation = html2text(mitigation)
            try:
                json.loads(description)
            except:
                description = description.replace("\'", "")
            try:
                json.loads(impact)
            except:
                impact = impact.replace("\'", "")
            try:
                json.loads(mitigation)
            except:
                mitigation = mitigation.replace("\'", "")
            data = {
                'title':
                title,
                'description':
                description,
                'severity':
                severity,
                'product':
                '/api/v1/products/' +
                self._helpers.urlEncode(self.ddui.productID.getText()) + '/',
                'engagement':
                '/api/v1/engagements/' +
                self._helpers.urlEncode(self.ddui.engagementID.getText()) +
                '/',
                'reporter':
                '/api/v1/users/' +
                self._helpers.urlEncode(str(self.ddui.userID)) + '/',
                'test':
                '/api/v1/tests/' +
                self._helpers.urlEncode(self.ddui.testID.getText()) + '/',
                'impact':
                impact,
                'active':
                True,
                'verified':
                True,
                'mitigation':
                mitigation,
                'static_finding':
                False,
                'dynamic_finding':
                False,
                'file_path':
                url
                # 'steps_to_reproduce': ureqresp
            }
            data = json.dumps(data)
            self.checkUpdateSender()
            start_new_thread(self.sender.makeRequest,
                             ('POST', '/api/v1/findings/', data))

    def checkUpdateSender(self):
        if self.sender.ddurl != self.ddui.defectDojoURL.getText().lower(
        ).split('://'):
            self.sender.setUrl(self.ddui.defectDojoURL.getText())
        if self.sender.user != self.ddui.user.getText():
            self.sender.setUser(self.ddui.user.getText())
        if self.ddui.apiKey.getText() != self.sender.apikey:
            self.sender.setApiKey(self.ddui.apiKey.getText())


class HttpData():
    req_data = ''
    ddurl = ''
    user = ''
    apikey = ''

    def __init__(self, ddurl, user, apikey):
        self.ddurl = ddurl.lower().split('://')
        self.user = user
        self.apikey = apikey
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Testing',
            'Authorization': "ApiKey " + self.user + ":" + self.apikey
        }

    def setUrl(self, ddurl):
        self.ddurl = ddurl.lower().split('://')

    def setApiKey(self, apikey):
        self.apikey = apikey
        self.headers['Authorization'] = "ApiKey " + self.user + ":" + apikey

    def setUser(self, user):
        self.user = user

    def makeRequest(self, method, url, data=None, src=None):
        if self.ddurl[0] == 'http':
            conn = httplib.HTTPConnection(self.ddurl[1])
        elif self.ddurl[0] == 'https':
            conn = httplib.HTTPSConnection(self.ddurl[1])
        else:
            return None
        if data:
            conn.request(method, url, body=data, headers=self.headers)
        else:
            conn.request(method, url, headers=self.headers)
        response = conn.getresponse()
        self.req_data = response.read()
        conn.close()
        if url == '/api/v1/importscan/':
            try:
                lbl = ClickableLink(
                    str("Successfully Imported selected Issues ! Access Test : "
                        + response.getheader('location').split('/')[4]),
                    str(self.ddurl[0] + "://" + self.ddurl[1] + "/test/" +
                        response.getheader('location').split('/')[4]))
                JOptionPane.showMessageDialog(src, lbl.getClickAbleLink())
            except:
                JOptionPane.showMessageDialog(src, "Import possibly failed!",
                                              "Error",
                                              JOptionPane.WARNING_MESSAGE)
        try:
            os.remove("./Data.txt")
        except:
            pass
        if self.headers['Content-Type'] != 'application/json':
            self.headers['Content-Type'] = 'application/json'
        return


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
            raise ValueError('Object not created:' + json.dumps(
                self.data, sort_keys=True, indent=4, separators=(',', ': ')))
        return int(self.data)

    def count(self):
        return self.data["meta"]["total_count"]

    def data_json(self, pretty=False):
        """Returns the data as a valid JSON string."""
        if pretty:
            return json.dumps(self.data,
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': '))
        else:
            return json.dumps(self.data)
