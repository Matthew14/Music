import os
import pylast
import json

class LastFM(object):
    """This class uses the last.fm api to 'scrobble' tracks to the last.fm service"""
    def __init__(self):
        self.apiKey = 'eb1f248f2a3dd23c0d321448d1b74c8a'
        self.secret =  'bfd72e05278afbd59b4b27e62036a115'
        self.getInfo()
        self.network = pylast.LastFMNetwork(api_key = self.apiKey, api_secret = self.secret,
            username = self.username, password_hash = self.password)
        sg = pylast.SessionKeyGenerator(self.network)
        self.scrobbler = self.network.get_scrobbler('tst', '1.0')

    def getInfo(self):
        """opens the settings json file and gets the username and password"""

        with open( os.path.abspath(os.path.dirname(__file__)) + '\\settings.json', 'r') as f:
            settings = json.load(f)
        self.enabled = settings[0]['scrobblingEnabled']
        self.username = settings[0]['username']
        self.password = settings[0]['password']
        self.password = pylast.md5(self.password)

    def nowPlaying(self, artist, track):
        """Sends the now playing information to last.fm. See http://www.last.fm/api/show/track.updateNowPlaying"""
        if self.enabled:
            self.network.update_now_playing(artist, track)

    def scrobble(self, artist, track, startTime, album=None, duration=0):
        if self.enabled:
            if album == None:
                album = ''
            """Scrobbles the track. See http://www.last.fm/api/show/track.scrobble"""
            self.network.scrobble(artist, track, startTime, pylast.SCROBBLE_SOURCE_USER, pylast.SCROBBLE_MODE_PLAYED,
                duration, album)