import pygame
from pygame import mixer
import os
import glob
import Queue
from track import Track

class MusicPlayer(object):
    def __init__(self):
        mixer.init()
        self._paused = False
        self.playQueue = Queue.Queue(-1) # queue of 'infinite' size

    @property
    def paused(self):
        """Boolean, for determining if the music is paused"""
        return self._paused
    @paused.setter
    def paused(self, value):
        self._paused = value

    def setNext(self):
        trackname = self.playQueue.get()
        self.currentTrack = Track(trackname)
        mixer.music.load(trackname)

    def play(self):
        try:
         if not self.paused:
            mixer.music.play()
            print 'play'
         else:
            mixer.music.unpause()
            self._paused = False

        except pygame.error as error:
             # self.showError(error)
             pass

    def pause(self):
        if mixer.music.get_busy() and not self.paused:
         mixer.music.pause()
         self._paused = True

    def stop(self):
        mixer.music.stop()

    def seek(self, position):
        # mixer.music.set_pos(pos)
        print dir(pygame.mixer.music)
        print "yep"

    def load(self, toLoad):
        if not self.playQueue.empty():
            self.playQueue = Queue.Queue(-1)#empty the queue


        if isinstance(toLoad, basestring): #checking if a string or a list
            toLoad = toLoad.encode('utf-8')
            print toLoad

            if os.path.isdir(toLoad): # we've been given a directory
                os.chdir(toLoad)
                for track in glob.glob('*.mp3'):
                    print track
                    self.playQueue.put(track)

            elif os.path.isfile(toLoad): #a file from the dirctrl
                self.playQueue.put(toLoad)

        else: # a list from the file -> open dialogue
            for track in toLoad:
                track = track.encode('utf-8')
                self.playQueue.put(track)

        self.setNext()
    def quit(self):
        pygame.quit()