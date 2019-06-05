from java.awt.event import ActionListener, MouseAdapter
from thread import start_new_thread
from java.awt.event import MouseAdapter
from burp import IContextMenuFactory
from burp import IContextMenuInvocation
from javax.swing import JMenuItem
from javax.swing import JButton
from java.awt import Desktop
from java.lang import Runtime
import platform
import os
from java import net


class ClickableLink():
    """
    This method generates a clickable button inside the prompt
    after the report is uploaded . It supposedly opens
    your default browser on the test's page .
    """
    def __init__(self,text,url):
        self.text = text
        self.url = url
    def getClickAbleLink(self):
        self.link = JButton(actionPerformed=self.openURL)
        self.link.setText(self.text)
        return self.link
    def openURL(self,event):
        try:
            Desktop.getDesktop().browse(net.URI(self.url))
        except:
            Runtime.getRuntime().exec("xdg-open "+self.url)

def linkDialog(message, link, JOptionPane, src):
    lbl = ClickableLink(message, link)
    JOptionPane.showMessageDialog(src, lbl.getClickAbleLink()) 

def html2text(strText):
    """
    This method transforms burp's HTML tags into normal
    text .
    TODO tranform into markdown .
    """
    html = str(strText).encode('utf8', 'replace')
    int2 = html.lower().find("<body")
    if int2 > 0:
        html = html[int2:]
    int2 = html.lower().find("</body>")
    if int2 > 0:
        html = html[:int2]
    list1 = ['<br>', '<tr', '<td', '</p>', 'span>', 'li>', '</h', 'div>']
    list2 = [
        chr(13),
        chr(13),
        chr(9),
        chr(13),
        chr(13),
        chr(13),
        chr(13),
        chr(13)
    ]
    f1 = True
    f2 = True
    toText = ""
    for int1 in range(len(html)):
        str2 = html[int1]
        for int2 in range(len(list1)):
            if html[int1:int1 + len(list1[int2])].lower() == list1[int2]:
                toText = toText + list2[int2]
        if str2 == '<':
            f2 = False
        if f1 and f2 and (ord(str2) != 10):
            toText = toText + str2
        if str2 == '>':
            f2 = True
        if f1 and f2:
            toText = toText.replace(chr(32) + chr(13), chr(13))
            toText = toText.replace(chr(9) + chr(13), chr(13))
            toText = toText.replace(chr(13) + chr(32), chr(13))
            toText = toText.replace(chr(13) + chr(9), chr(13))
            toText = toText.replace(chr(13) + chr(13), chr(13))
    return toText


class SendToDojo(IContextMenuFactory):
    """
    SendToDojo implements the class needed to create the context
    menu when rightclicking an issue .
    """

    def __init__(self, data):
        self.a = data

    def createMenuItems(self, invoker):
        self._invoker = invoker
        context = self._invoker.getInvocationContext()
        if not context == self._invoker.CONTEXT_SCANNER_RESULTS:
            return None
        self.selection = JMenuItem("Send To DefectDojo (Existing Test)",
                                   actionPerformed=self.a.sendIssue)
        return [self.selection]


class SendReportToDojo(IContextMenuFactory):
    """
    SendReportToDojo implements the class needed to create
    the context menu when rightclicking an issue(s) in order
    to send them as a report to Defect Dojo .
    """

    def __init__(self, data):
        self.a = data

    def createMenuItems(self, invoker):
        self._invoker = invoker
        context = self._invoker.getInvocationContext()
        if not (context == self._invoker.CONTEXT_SCANNER_RESULTS
                or context == self._invoker.CONTEXT_TARGET_SITE_MAP_TREE):
            return None
        if context == self._invoker.CONTEXT_SCANNER_RESULTS:
            self.selection = JMenuItem("Send Report To DefectDojo (New Burp Test)",
                                       actionPerformed=self.a.sendAsReport)
            return [self.selection]
        else:
            self.selection = JMenuItem("Send All Issues to DefectDojo (New Burp Test)",
                                       actionPerformed=self.a.sendAsReport)
            return [self.selection]


class ProdListener(ActionListener):
    """
    Updates the productID field based on the selection from the ComboBox
    """

    def __init__(self, data):
        self.a = data

    def actionPerformed(self, e):
        cmd = e.getActionCommand()
        if cmd == 'comboBoxChanged':
            selected = self.a.ddui.productName.selectedIndex
            if selected >= 0:
                self.a.ddui.productID.setText(
                    str(self.a.ddui.products.data['objects'][selected]['id']))
                start_new_thread(self.a.getEngagements, (e, ))

class ProdMouseListener(MouseAdapter):
    """
    Fetches products for the product ComboBox 
    """

    def __init__(self, data):
        self.a = data

    def mousePressed(self, event):
        self.a.getProducts(event)

class EngListener(ActionListener):
    """
    Updates the engagementID field based on the selection from the ComboBox
    """

    def __init__(self, data):
        self.a = data

    def actionPerformed(self, e):
        cmd = e.getActionCommand()
        if cmd == 'comboBoxChanged':
            selected = self.a.ddui.engagementName.selectedIndex
            if selected >= 0:
                self.a.ddui.engagementID.setText(
                    str(self.a.ddui.engagements.data['objects'][selected]['id']))
                start_new_thread(self.a.getTests, (e, ))


class TestListener(ActionListener):
    """
    Updates the testID field based on the selection from the ComboBox
    """

    def __init__(self, data):
        self.a = data

    def actionPerformed(self, e):
        cmd = e.getActionCommand()
        if cmd == 'comboBoxChanged':
            selected = self.a.ddui.testName.selectedIndex
            if selected >= 0:
                self.a.ddui.testID.setText(
                    str(self.a.ddui.tests.data['objects'][selected]['id']))

