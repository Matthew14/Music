import wx
from musicFrame import musicFrame
if __name__ == '__main__':
    """ This is the main program's entry point. Instantiates a frame and that does the work from there."""
    app = wx.PySimpleApp()
    frame = musicFrame(parent = None, id = -1)
    frame.Show()
    app.MainLoop()