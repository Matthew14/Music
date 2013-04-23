import urllib2
class LastFM(object):
    """This class uses the last.fm api to 'scrobble' tracks to the last.fm service"""
    def __init__(self, username, password):
        self.apiKey = 'eb1f248f2a3dd23c0d321448d1b74c8a'

    def nowPlaying(self, artist, track):
        """Sends the now playing information to last.fm. See http://www.last.fm/api/show/track.updateNowPlaying"""
        pass

    def scrobble(self, artist, track, startTime, album=None):
        """Scrobbles the track. See http://www.last.fm/api/show/track.scrobble"""
        postData = {'artist' : artist, 'track' : track, 'timestamp' : startTime}
        if album != None:
            postData = {'artist' : artist, 'track' : track, 'timestamp' : startTime, 'album' : album}

