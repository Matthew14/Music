import os
import wx

class MattsAboutBoxInfo(wx.AboutDialogInfo):
    """Custom about dialog for the application"""
    def __init__(self, name):
        wx.AboutDialogInfo.__init__(self) # base constructor

        self.name = name
        description = """A music playing application written in python 2.7.3 using the wxPython tool kit."""

        try:
         with open(os.path.dirname(__file__) + '\.licence', 'r') as licenceText:
            licence = licenceText.read().replace('NAME', self.name) #for ease of name changing
        except IOError:
         licence = 'See http://www.matthewoneill.com/%s/' % (self.name.strip().replace(' ', ''))

        self.SetIcon(wx.Icon(os.path.dirname(__file__) + '\\img\\aboutIcon.png', wx.BITMAP_TYPE_PNG))
        self.SetName(name)
        self.SetVersion('0.1')
        self.SetDescription(description)
        self.SetCopyright('(C) 2013 Matthew O\'Neill')
        self.SetWebSite('http://www.matthewoneill.com')
        self.SetLicence(licence)
        self.AddDeveloper('Matthew O\'Neill')
        self.AddDocWriter('Matthew O\'Neill')