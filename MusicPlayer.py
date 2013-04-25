import pygame
from pygame import mixer
import os
import glob
import Queue
from track import Track
from lastfm import LastFM
class MusicPlayer(object):
    """the music playing class."""
    def __init__(self):
        mixer.init()
        self._paused = False
        self.currentTrack = None
        self.last = LastFM()
        self.offset = 0
        self.playQueue = Queue.Queue(-1) # queue of 'infinite' size
        self.previous = [] #using a list as a stack to hold previous plays

    @property
    def paused(self):
        """Boolean, for determining if the music is paused"""
        return self._paused
    @paused.setter
    def paused(self, value):
        self._paused = value

    @property
    def scrobblingEnabled(self):
        """Boolean, for determining if scrobbling is Enabled"""
        return self._scrobblingEnabled
    @scrobblingEnabled.setter
    def scrobblingEnabled(self, value):
        self._scrobblingEnabled = value

    def update(self):
        #if the playback is over half way (last.fm regulation) then scrobble it
        if self.currentTrack != None and mixer.music.get_pos() / 1000  >= self.currentTrack.length/2:
            if not self.currentTrack.scrobbled:
                self.last.scrobble(self.currentTrack.artist, self.currentTrack.title, self.currentTrack.time)
                self.currentTrack.scrobbled = True
        """Checks if the playing track is over and if so, changes it. returns changed if the track has changed"""
        if self.currentTrack != None and (mixer.music.get_pos() / 1000 ) >= self.currentTrack.length:
            self.setNext()
            return 'changed'

    def setNext(self, event=None):
        if not self.playQueue.empty():
            if self.currentTrack != None:
                self.previous.append(self.currentTrack.path)

            trackname = self.playQueue.get()
            self.currentTrack = Track(trackname)
            mixer.music.load(trackname)
            self.offset = 0
            self.play()

    def setPrevious(self, event=None):
        if len(self.previous) > 0:
            trackname = self.previous.pop()
            self.currentTrack = Track(trackname)
            mixer.music.load(trackname)
            self.play()

    def play(self):
        try:
            if self.currentTrack != None:
                if not self.paused:
                    mixer.music.play()
                else:
                    mixer.music.unpause()
                    self._paused = False
                self.last.nowPlaying(self.currentTrack.artist, self.currentTrack.title)
            else:
                raise Exception("No track loaded")

        except pygame.error as error:
             raise error

    def pause(self):
        if mixer.music.get_busy() and not self.paused:
         mixer.music.pause()
         self._paused = True

    def stop(self):
        mixer.music.stop()

    def seek(self, position):
        if self.currentTrack != None:
            self.stop()
            self.offset = position
            pygame.mixer.music.play(0, position)

    def setVolume(self, vol):
        mixer.music.set_volume(vol)

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

    def getPos(self):
        return  mixer.music.get_pos() + self.offset

    def quit(self):
        pygame.quit()

if __name__ == '__main__':
    print("You need to open the main.pyw file")