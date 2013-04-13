import sys
try:
	import wx
	from pygame import mixer
except ImportError:
	if sys.version_info[0] != 2:
		print("Need Python version 2.x.x, your version is: " + sys.version.split(' ')[0])
	else:
		
		print("Cannot find the required libraries.")
	sys.exit(1)
class MainFrame(wx.Frame):
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, 'Matt\'s Music', style=wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER 
	| wx.SYSTEM_MENU | wx.CAPTION |	 wx.CLOSE_BOX)
		self.SetSize((800, 600))
		self.Centre()

if __name__ == '__main__':
	mixer.init()
	app = wx.App()
	frame = MainFrame(None, -1)
	frame.Show()
	app.MainLoop()