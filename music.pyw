#TODO: last.fm integration
#TODO: fix unicode filenames
#TODO: play queue system
#TODO: dirctrl
#TODO: change icons

try:
	import wx
	import pygame
	from pygame import mixer
except ImportError as error:
	import sys
	if sys.version_info[0] != 2:
		print("Unfortunately as wxpython doesn't yet support python 3, you need Python version \n"
			"2.x.x to run this program, your version is: {0}.".format(sys.version.split(' ')[0]) )
	else:
		print("Cannot find the required libraries.")
		import webbrowser
		if 'wx' not in dir():
			webbrowser.open('http://www.wxpython.org')
		elif 'pygame' not in dir():
			webbrowser.open('http://www.pygame.org')
	sys.exit(1)

mixer.init()

class frameClass(wx.Frame):
	"""This is the class for the Main wx frame."""
	def __init__(self, parent, id):
		self.name = 'Music all up in yo\' grill'
		wx.Frame.__init__(self, parent, id, self.name, size = (800, 600)) #calling base constructor, size and stuff
		self.setupUI()
		self.isPaused = False

	def setupUI(self):
		"""Calls other setup methods, sets the icon and all other initial UI stuff"""
		self.panel = wx.Panel(self)
		self.Center()
		status = self.CreateStatusBar()
		self.menuBarInit()
		self.ToolBarInit()
		icon = wx.Icon('playIcon.ico', wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon)

	def menuBarInit(self):
		"""Sets up the menubar and its menu items, binding them to their onClick methods"""
		self.menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		openfile = fileMenu.Append(wx.ID_OPEN, '&Open\tCtrl+O', 'Open a file.')
		fileMenu.AppendSeparator()
		quitItem = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Exit application.')
		helpMenu = wx.Menu()
		about = helpMenu.Append(wx.NewId(), '&About', 'About this program.')
		self.menubar.Append(fileMenu, '&File')#The & makes the first char underlined on hitting 'alt' - cool
		self.menubar.Append(helpMenu, '&Help')

		#bind the items to their respective handlers:
		self.Bind(wx.EVT_MENU, self.openFileDialog, openfile)
		self.Bind(wx.EVT_MENU, self.onQuit, quitItem)
		self.Bind(wx.EVT_MENU, self.showAboutDialog, about)

		self.SetMenuBar(self.menubar)

	def ToolBarInit(self):
		"""Sets up the tool bar which contains various wx controls"""
		self.tool = self.CreateToolBar()
		playTool = self.tool.AddLabelTool(wx.ID_ANY, 'Play', wx.Bitmap('play.bmp', wx.BITMAP_TYPE_ANY))
		pauseTool = self.tool.AddLabelTool(wx.ID_ANY, 'Pause', wx.Bitmap('pause.bmp', wx.BITMAP_TYPE_ANY))
		stopTool = self.tool.AddLabelTool(wx.ID_ANY, 'Stop', wx.Bitmap('stop.bmp', wx.BITMAP_TYPE_ANY))

		self.tool.AddSeparator()

		self.volume = wx.Slider(self.tool, -1, 50, 0, 100, style= wx.SL_AUTOTICKS | wx.SL_LABELS)
		self.volume.SetTickFreq(5, 1)

		self.tool.AddControl(self.volume)

		self.tool.AddSeparator()

		self.tool.Realize() #needed for windows

		self.Bind(wx.EVT_TOOL, self.play, playTool)
		self.Bind(wx.EVT_TOOL, self.pause, pauseTool)
		self.Bind(wx.EVT_TOOL, self.stop, stopTool)

		self.Bind(wx.EVT_SLIDER, self.onSlide, self.volume)

	def onSlide(self, event):
		print (mixer.music.get_volume())
		vol = float(event.GetEventObject().GetValue()) / 100.0 #needs to be between 0.0 and 1.0
		mixer.music.set_volume(vol)

	def onQuit(self, event):
		self.Close()

	def openFileDialog(self, event):
		filters = 'All files (*.*)|*.*|Music files (*.mp3)|*.mp3'

		dialog = wx.FileDialog ( None, style = wx.FD_OPEN | wx.MULTIPLE, wildcard=filters )
		if dialog.ShowModal() == wx.ID_OK:
			selectedFiles = dialog.GetPaths()

			print (selectedFiles)
			try:
				mixer.music.load(selectedFiles[0].encode('utf-8'))
				for fo in selectedFiles:
					mixer.music.queue(fo)
				print(mixer.music.get_pos())
				mixer.music.play()
			except pygame.error as error:
				self.showError(error)

	def showAboutDialog(self, event):
		description = """A music playing application written in python 2.7.3 using the wxPython tool kit."""

		try:
			with open('.licence', 'r') as licenceText:
				licence = licenceText.read().replace('NAME', self.name) #for ease of name changing
		except IOError:
			licence = 'See http://www.matthewoneill.com/%s/' % (self.name.strip().replace(' ', ''))

		info = wx.AboutDialogInfo()
		info.SetIcon(wx.Icon('aboutIcon.png', wx.BITMAP_TYPE_PNG))
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
			if not self.isPaused:
				mixer.music.play()
			else:
				mixer.music.unpause()
				self.isPaused = False
		except pygame.error as error:
			self.showError(error)

	def pause(self, event):
		if mixer.music.get_busy() and not self.isPaused:
			mixer.music.pause()
			self.isPaused = True

	def stop(self, event):
		print ('stop')
		mixer.music.stop()

	def showError(self, error):
		wx.MessageBox(str(error), 'Uh Oh', wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = frameClass(parent = None, id = -1)
	frame.Show()
	app.MainLoop()