#TODO: last.fm integration
#TODO: redraw on sizing
import os, glob
import sys
import json
try:
   from MusicPlayer import MusicPlayer
   from settings import Settings
   from about import MattsAboutBoxInfo
   import wx
except ImportError as error:
   if sys.version_info[0] != 2:
      print("Unfortunately as wxpython doesn't yet support python 3, you need Python version \n"
         "2.x.x to run this program, your version is: {0}.".format(sys.version.split(' ')[0]) )
   else:
      print("Cannot find the required libraries.")
   sys.exit(1)

class musicFrame(wx.Frame):
   """This is the class for the Main wx frame."""
   def __init__(self, parent, id):
      self.name = 'Matt\'s Music'
      self.size = (900, 600)
      wx.Frame.__init__   (self, parent, id, self.name, size = self.size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
      self.player = MusicPlayer()
      self.setupUI()

      #updates every 1000 miliseconds
      self.timer = wx.Timer(self)
      self.timer.Start(1000)
      self.Bind(wx.EVT_TIMER, self.update, self.timer)

   def update(self, event):
      self.position.SetValue(self.player.getPos() / 1000)
      if self.player.update() == 'changed':
         self.play()
         self.setPlayingInfo()

   def setupUI(self):
      """Calls other setup methods, sets the icon and all other initial UI stuff"""
      self.Center()
      status = self.CreateStatusBar()
      #left window for directory listing, right for playback info
      self.splitter = wx.SplitterWindow(self, -1)
      self.leftCol = wx.SashLayoutWindow(self.splitter, -1, style=wx.BORDER_SUNKEN)
      self.rightCol =  wx.SashLayoutWindow(self.splitter, -1, style=wx.BORDER_SUNKEN | wx.FULL_REPAINT_ON_RESIZE)
      self.rightCol.SetBackgroundColour('#C1C6F5')

      self.splitter.SplitVertically(self.leftCol, self.rightCol, 250)
      self.menuBarInit()
      self.ToolBarInit()
      self.directoryListInit()
      icon = wx.Icon( os.path.abspath(os.path.dirname(__file__)) + '\img\playIcon.ico', wx.BITMAP_TYPE_ICO)
      self.SetIcon(icon)

   def setPlayingInfo(self):
      self.rightCol.Update()
      self.rightCol.ClearBackground()
      rightColSize =  self.rightCol.GetSize()
      if self.player.currentTrack != None:
         ####Set position bar to have correct length:
         self.position.SetMax(self.player.currentTrack.length)

         ####Album Art:
         artPos = ((self.GetSize()[0] / 2) - (250), 10)
         artFile = self.player.currentTrack.artwork
         if artFile != None:
            art = wx.Image(str(artFile), wx.BITMAP_TYPE_JPEG)
            art = art.Scale(250, 250, wx.IMAGE_QUALITY_HIGH)
            art = art.ConvertToBitmap()
            art = wx.StaticBitmap(self.rightCol, -1, art, artPos, (art.GetWidth(),art.GetHeight()))

         ####Track info:
         trackInfoPos = (self.GetSize()[0] /2, self.GetSize()[1] - 300)
         trackNO = str(self.player.currentTrack.trackNumber[0])
         title = self.player.currentTrack.title
         artist = self.player.currentTrack.artist
         album = self.player.currentTrack.album

         #casting all of these to str as they may be None:
         self.SetTitle(trackNO + ': ' + title + ' - ' +str(artist))

         playingInfo = """\
Track: {}
Title: {}
Artist: {}
Album: {}
""".format(str(trackNO), str(title), str(artist), str(album))
         wx.StaticText(self.rightCol, -1, playingInfo, trackInfoPos).CenterOnParent(wx.HORIZONTAL)

   def directoryListInit(self, directory='D:\\music'):
      self.dirControl = wx.GenericDirCtrl(self.leftCol, -1, size=(700, 450), dir=directory, style=0)
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
      previousTool = self.tool.AddLabelTool(wx.ID_ANY, 'Previous', wx.Bitmap('img\\previous.bmp', wx.BITMAP_TYPE_ANY))
      nextTool = self.tool.AddLabelTool(wx.ID_ANY, 'Next', wx.Bitmap('img\\next.bmp', wx.BITMAP_TYPE_ANY))
      self.tool.AddSeparator()
      self.volume = wx.Slider(self.tool, -1, 50, 0, 100, style=wx.SL_AUTOTICKS | wx.SL_LABELS)
      self.volume.SetTickFreq(5, 1)

      posSizeX = self.size[0] - 425
      self.position = wx.Slider(self.tool, -1, 0, 0, 100, size=(posSizeX, -1), style=wx.SL_AUTOTICKS | wx.SL_LABELS)
      self.position.SetTickFreq(5, 1)

      self.tool.AddControl(self.volume)
      self.tool.AddSeparator()
      self.tool.AddControl(self.position)

      self.tool.Realize() #needed for windows

      #Event Bindings
      self.Bind(wx.EVT_TOOL, self.play, playTool)
      self.Bind(wx.EVT_TOOL, self.pause, pauseTool)
      self.Bind(wx.EVT_TOOL, self.stop, stopTool)
      self.Bind(wx.EVT_TOOL, self.previous, previousTool)
      self.Bind(wx.EVT_TOOL, self.next, nextTool)
      self.Bind(wx.EVT_SLIDER, self.onVolSlide, self.volume)
      self.Bind(wx.EVT_SLIDER, self.setPosition, self.position)

   def setPosition(self, event):
      self.timer.Stop()
      pos = int(event.GetEventObject().GetValue())
      self.player.seek(pos)
      self.timer.Start(1000)

   def onVolSlide(self, event):
      self.player.setVolume(float(event.GetEventObject().GetValue()) / 100.0) #needs to be between 0.0 and 1.0

   def onSettings(self, event):
      settings = Settings(self, -1, 'Preferences')

      ans = settings.ShowModal()
      if ans == wx.ID_OK:
         username = settings.userText.GetValue()
         password = settings.passText.GetValue()
         settingsData = [ {
            'workingDirectory' : settings.currentFolder,
            'scrobblingEnabled' : settings.scrobblingEnabled,
            'username' : username,
            'password' : password} ]

         with open( os.path.abspath(os.path.dirname(__file__)) + '\\settings.json', 'w') as f:
            json.dump(settingsData, f, indent=4)
      self.player.scrobblingEnabled = settings.scrobblingEnabled
      settings.Destroy()

   def openFileDialog(self, event):
      filters = 'All files (*.*)|*.*|Music files (*.mp3)|*.mp3'

      dialog = wx.FileDialog ( None, style = wx.FD_OPEN | wx.MULTIPLE, wildcard=filters )
      if dialog.ShowModal() == wx.ID_OK:
         selectedFiles = dialog.GetPaths()
         self.player.load(selectedFiles)

   def showAboutDialog(self, event):
      info = MattsAboutBoxInfo(self.name)
      wx.AboutBox(info)

   def play(self, event=None):
      try:
         self.player.play()
         self.setPlayingInfo()
      except Exception as e:
         self.showError(e)
   def next(self, event=None):
      self.player.setNext()
      self.setPlayingInfo()
      self.play()
   def previous(self, event=None):
      self.player.setPrevious()
      self.setPlayingInfo()
      self.play()
   def pause(self, event=None):
      self.player.pause()

   def stop(self, event=None):
      self.player.stop()

   def showError(self, error):
      wx.MessageBox(str(error), 'Uh Oh', wx.OK | wx.ICON_ERROR)

   def onQuit(self, event):
      self.player.quit()
      self.Close()
      sys.exit(0)