import os
import wx
import json

class Settings(wx.Dialog):
    def __init__(self, parent, ID, title, size=(400, 400), pos=(100, 100), style=wx.DEFAULT_DIALOG_STYLE, useMetal=False):
        filename = os.path.dirname(__file__) + 'settings.json'
        self.getInfo(filename)

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size)
        self.PostCreate(pre)
        self.Center()
        self.UiInit()

    def UiInit(self):
        panel = wx.Panel(self)
        vertSizer = wx.BoxSizer(wx.VERTICAL)
        #Last.fm settings
        settings = wx.StaticBox(panel, label='Settings')
        settingsSizer = wx.StaticBoxSizer(settings, orient=wx.VERTICAL)

        enableLastFmSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lastCheckBox = wx.CheckBox(panel, -1, "Enable last.fm scrobbling")
        enableLastFmSizer.Add(self.lastCheckBox, flag=wx.ALL | wx.EXPAND, border=5)
        settingsSizer.Add(enableLastFmSizer)
        self.Bind(wx.EVT_CHECKBOX, self.onLastCheck, self.lastCheckBox)

        usernameSizer = wx.BoxSizer(wx.HORIZONTAL)
        userLabel = wx.StaticText(panel, -1, 'Last.fm Username: ')
        usernameSizer.Add(userLabel, flag=wx.ALL | wx.EXPAND, border=5)
        self.userText = wx.TextCtrl(panel, -1, "", size=(150, -1))
        self.userText.SetHelpText("Enter the last.fm username for scrobbling")
        self.userText.SetValue(self.username)
        usernameSizer.Add(self.userText, flag=wx.ALL | wx.EXPAND, border=5)
        settingsSizer.Add(usernameSizer)

        passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
        passwordLabel = wx.StaticText(panel, -1, 'Last.fm Password: ')
        passwordSizer.Add(passwordLabel,  flag=wx.ALL | wx.EXPAND, border=5)
        self.passText = wx.TextCtrl(panel, -1, "", style=wx.TE_PASSWORD, size=(150, -1))
        self.passText.SetValue(self.password)
        passwordSizer.Add(self.passText, flag=wx.ALL | wx.EXPAND, border=5)
        settingsSizer.Add(passwordSizer)
        #end last.fm settings

        #set folder setting
        currentFolderSizer = wx.BoxSizer(wx.HORIZONTAL)
        folderLabel = wx.StaticText(panel, -1, 'Current Folder: {}'.format(self.currentFolder))
        currentFolderSizer.Add(folderLabel, flag=wx.ALL | wx.EXPAND, border=5)
        settingsSizer.Add(currentFolderSizer)

        setFolderSizer = wx.BoxSizer(wx.HORIZONTAL)
        dirButt= wx.Button(panel, -1, "Set Music Folder", (150,50))
        self.Bind(wx.EVT_BUTTON, self.onDirButton , dirButt)
        setFolderSizer.Add(dirButt, flag=wx.ALL | wx.EXPAND, border=5)
        settingsSizer.Add(setFolderSizer)
        #end folder settings

        #ok and cancel
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK)
        cancelButton = wx.Button(self, wx.ID_CANCEL)
        okButton.SetDefault()
        buttonSizer.Add(okButton)
        buttonSizer.Add(cancelButton, flag=wx.LEFT, border=5)

        vertSizer.Add(panel, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vertSizer.Add(buttonSizer,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        panel.SetSizer(settingsSizer)
        self.SetSizer(vertSizer)

        if self.userText.GetValue() == '' or not self.scrobblingEnabled:
            self.lastCheckBox.Set3StateValue(0)
            self.userText.Disable()
            self.passText.Disable()
        else:
            self.lastCheckBox.Set3StateValue(1)
            self.userText.Enable()
            self.passText.Enable()

    def getInfo(self, filename):
        with open( os.path.abspath(os.path.dirname(__file__)) + '\\settings.json', 'r') as f:
            settingsDict = json.load(f)
        self.scrobblingEnabled = settingsDict[0]['scrobblingEnabled']
        self.username= settingsDict[0]['username']
        self.password = settingsDict[0]['password']
        self.currentFolder = settingsDict[0]['workingDirectory']

    def onLastCheck(self, event):
        result = self.lastCheckBox.Get3StateValue()
        if result == 0:
            self.userText.Disable()
            self.passText.Disable()
            self.scrobblingEnabled = False
        elif result == 1:
            self.userText.Enable()
            self.passText.Enable()
            self.scrobblingEnabled = True

    def onDirButton(self, event):
        directoryDialog = wx.DirDialog(self, "Choose a directory:",
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.DD_CHANGE_DIR)

        if directoryDialog.ShowModal() == wx.ID_OK:
           self.currentFolder = directoryDialog.GetPath()
           print self.currentFolder
        directoryDialog.Destroy()

if __name__ == '__main__':
    print("You must open the main.pyw file")