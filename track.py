import eyed3
import os
import glob

class Track(object):
    def __init__(self, trackname):
        self.coverNames = ['folder.jpg', 'Folder.jpg', 'cover.jpg', 'Cover.jpg', 'front.jpg'] #common artwork filenames
        self.setCurrent(trackname)

    def setCurrent(self, trackname):
        self.path = trackname
        try:
            audioFile = eyed3.core.load(trackname)
            af = eyed3.core.AudioInfo()
        except IOError as error:
            raise(error)
        else:
            self.artwork = os.path.abspath(os.path.dirname(__file__)) + '\img\unknownArt.jpg' #default if none is found
            self.artist = audioFile.tag.artist
            self.album = audioFile.tag.album
            self.title = audioFile.tag.title
            self.length = audioFile.info.time_secs
            self.trackNumber =  audioFile.tag.track_num #tuple, (trackNum, noTracks)
            for filen in glob.glob('*.jpg'):
                if filen in self.coverNames:
                    self.artwork = filen
                    break

if __name__ == '__main__':
    print("You need to open the main.pyw file")