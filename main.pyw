#TODO: playing bar
#TODO: last.fm integration
#TODO: fix unicode filenames
#TODO: play queue system
#TODO: settings panel
#TODO: change icons
#TODO: redraw on sizing
#TODO: Help
import os, glob
import sys
try:
   from MusicPlayer import MusicPlayer
   from settings import Settings
   import wx

except ImportError as error:
   if sys.version_info[0] != 2:
      print("Unfortunately as wxpython doesn't yet support python 3, you need Python version \n"
         "2.x.x to run this program, your version is: {0}.".format(sys.version.split(' ')[0]) )
   else:
      print("Cannot find the required libraries.")
   sys.exit(1)

class frameClass(wx.Frame):
   """This is the class for the Main wx frame."""
   def __init__(self, parent, id):
      self.name = 'Matt\'s Music'
      wx.Frame.__init__   (self, parent, id, self.name, size = (800, 600)) #calling base constructor, size and stuff
      self.player = MusicPlayer()
      self.setupUI()

      #updates every 1000 miliseconds
      self.timer = wx.Timer(self)
      self.timer.Start(1000)
      self.Bind(wx.EVT_TIMER, self.update, self.timer)

   def update(self, event):
      self.position.SetValue(self.player.getPos() / 1000)
      if self.player.currentTrack != None and self.player.getPos() / 1000 >= self.player.currentTrack.length:
         self.player.setNext()
         self.play()

   def setupUI(self):
      """Calls other setup methods, sets the icon and all other initial UI stuff"""
      self.Center()
      status = self.CreateStatusBar()
      self.splitter = wx.SplitterWindow(self, -1)
      self.leftCol = wx.SashLayoutWindow(self.splitter, -1, style=wx.BORDER_SUNKEN)
      self.rightCol =  wx.SashLayoutWindow(self.splitter, -1, style=wx.BORDER_SUNKEN)
      self.rightCol.SetBackgroundColour(wx.WHITE)
      self.splitter.SplitVertically(self.leftCol, self.rightCol, 250)
      self.menuBarInit()
      self.ToolBarInit()
      self.directoryListInit()
      icon = wx.Icon('img\playIcon.ico', wx.BITMAP_TYPE_ICO)
      self.SetIcon(icon)

   def setPlayingInfo(self):
      self.rightCol.Update()
      self.rightCol.ClearBackground()

      if self.player.currentTrack != None:
         ####Set position bar to have correct length:
         self.position.SetMax(self.player.currentTrack.length)

         ####Track info:
         trackNO = str(self.player.currentTrack.trackNumber[0])
         track = trackNO + ' of ' +str(self.player.currentTrack.trackNumber[1])
         title = self.player.currentTrack.title
         artist = self.player.currentTrack.artist
         album = self.player.currentTrack.album

         #casting all of these to str as they may be None:
         self.SetTitle(trackNO + ': ' + title + ' - ' +str(artist))

         if self.player.currentTrack.trackNumber[1] == None:
            wx.StaticText(self.rightCol, -1, 'Track: ' + str(trackNO), (20, 10))
         else:
            wx.StaticText(self.rightCol, -1, 'Track: ' + str(track), (20, 10))

         wx.StaticText(self.rightCol, -1, 'Title: ' + str(title), (20, 30))
         wx.StaticText(self.rightCol, -1, 'Artist: ' + str(artist), (20, 50))
         wx.StaticText(self.rightCol, -1, 'Album: ' + str(album), (20, 70))

         ####Album Art:
         artFile = self.player.currentTrack.artwork
         if artFile != None:
            art = wx.Image(str(artFile), wx.BITMAP_TYPE_JPEG)
            art = art.Scale(250, 250, wx.IMAGE_QUALITY_HIGH)
            art = art.ConvertToBitmap()
            # art.Scale(250)
            wx.StaticBitmap(self.rightCol, -1, art, (10, 100), (art.GetWidth(),art.GetHeight()))

   def directoryListInit(self):
      self.dirControl = wx.GenericDirCtrl(self.leftCol, -1, size=(700, 450), dir='D:\\music', style=0)
      tree = self.dirControl.GetTreeCtrl()

      ###Event binding
      self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDirCtrlSelect, id=tree.GetId()) #either double-clicked, or selected and 'enter'

   def onDirCtrlSelect(self, event):
      selected = self.dirControl.GetPath()
      self.player.load(selected)
      self.setPlayingInfo()

   def menuBarInit(self):
      """Sets up the menubar and its menu items, binding them to their onClick methods"""
      self.menubar = wx.MenuBar()
      fileMenu = wx.Menu()
      openfile = fileMenu.Append(wx.ID_OPEN, '&Open\tCtrl+O', 'Open a file.')
      fileMenu.AppendSeparator()
      quitItem = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Exit application.')
      helpMenu = wx.Menu()
      about = helpMenu.Append(wx.NewId(), '&About', 'About this program.')
      editMenu = wx.Menu()
      prefs = editMenu.Append(wx.NewId(), '&Preferences\tCtrl+P', 'Opens a settings dialog.')
      self.menubar.Append(fileMenu, '&File')#The & makes the first char underlined on hitting 'alt' - cool
      self.menubar.Append(editMenu, '&Edit')
      self.menubar.Append(helpMenu, '&Help')

      #Event Bindings
      self.Bind(wx.EVT_MENU, self.openFileDialog, openfile)
      self.Bind(wx.EVT_MENU, self.onQuit, quitItem)
      self.Bind(wx.EVT_MENU, self.showAboutDialog, about)
      self.Bind(wx.EVT_MENU, self.onSettings, prefs)

      self.SetMenuBar(self.menubar)

   def ToolBarInit(self):
      """Sets up the tool bar which contains various wx controls"""
      self.tool = self.CreateToolBar()
      playTool = self.tool.AddLabelTool(wx.ID_ANY, 'Play', wx.Bitmap('img\play.bmp', wx.BITMAP_TYPE_ANY))
      pauseTool = self.tool.AddLabelTool(wx.ID_ANY, 'Pause', wx.Bitmap('img\pause.bmp', wx.BITMAP_TYPE_ANY))
      stopTool = self.tool.AddLabelTool(wx.ID_ANY, 'Stop', wx.Bitmap('img\stop.bmp', wx.BITMAP_TYPE_ANY))

      # self.tool.SetToolBitmapSize((8,8))
      self.tool.AddSeparator()

      self.volume = wx.Slider(self.tool, -1, 50, 0, 100, style=wx.SL_AUTOTICKS | wx.SL_LABELS)
      self.volume.SetTickFreq(5, 1)

      self.position = wx.Slider(self.tool, -1, 0, 0, 100, size=(490, -1), style=wx.SL_AUTOTICKS | wx.SL_LABELS)
      self.position.SetTickFreq(5, 1)

      self.tool.AddControl(self.volume)
      self.tool.AddSeparator()
      self.tool.AddControl(self.position)

      self.tool.Realize() #needed for windows

      #Event Bindings
      self.Bind(wx.EVT_TOOL, self.play, playTool)
      self.Bind(wx.EVT_TOOL, self.pause, pauseTool)
      self.Bind(wx.EVT_TOOL, self.stop, stopTool)
      self.Bind(wx.EVT_SLIDER, self.onVolSlide, self.volume)
      self.Bind(wx.EVT_SLIDER, self.setPosition, self.position)

   def setPosition(self, event):
      pos = int(event.GetEventObject().GetValue())
      print pos
      self.player.stop()
      self.player.seek(pos)
      self.player.play()

   def onVolSlide(self, event):
      self.player.setVolume(float(event.GetEventObject().GetValue()) / 100.0) #needs to be between 0.0 and 1.0

   def onSettings(self, event):
      settings = Settings(self, -1, 'Preferences')

      ans = settings.ShowModal()
      if ans == wx.ID_OK:
         pass
      else:
         pass
      settings.Destroy()

   def onQuit(self, event):
      self.player.quit()
      self.Close()
      sys.exit()

   def openFileDialog(self, event):
      filters = 'All files (*.*)|*.*|Music files (*.mp3)|*.mp3'

      dialog = wx.FileDialog ( None, style = wx.FD_OPEN | wx.MULTIPLE, wildcard=filters )
      if dialog.ShowModal() == wx.ID_OK:
         selectedFiles = dialog.GetPaths()
         self.player.load(selectedFiles)

   def showAboutDialog(self, event):
      description = """A music playing application written in python 2.7.3 using the wxPython tool kit."""

      try:
         with open(os.path.dirname(__file__) + '\.licence', 'r') as licenceText:
            licence = licenceText.read().replace('NAME', self.name) #for ease of name changing
      except IOError:
         licence = 'See http://www.matthewoneill.com/%s/' % (self.name.strip().replace(' ', ''))

      info = wx.AboutDialogInfo()
      info.SetIcon(wx.Icon(os.path.dirname(__file__) + '\\img\\aboutIcon.png', wx.BITMAP_TYPE_PNG))
      info.SetName(self.name)
      info.SetVersion('0.1')
      info.SetDescription(description)
      info.SetCopyright('(C) 2013 Matthew O\'Neill')
      info.SetWebSite('http://www.matthewoneill.com')
      info.SetLicence(licence)
      info.AddDeveloper('Matthew O\'Neill')
      info.AddDocWriter('Matthew O\'Neill')
      wx.AboutBox(info)

   def play(self, event):
      try:
         if self.player.currentTrack != None:
            self.player.play()
            self.setPlayingInfo()
         else:
            raise Exception("No track loaded")
      except Exception as e:
         self.showError(e)

   def pause(self, event):
      self.player.pause()

   def stop(self, event):
      print ('stop')
      self.player.stop()

   def showError(self, error):
      wx.MessageBox(str(error), 'Uh Oh', wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
   app = wx.PySimpleApp()
   frame = frameClass(parent = None, id = -1)
   frame.Show()
   app.MainLoop()