import urllib2
import json
import socket

AUDIO_DB = 'http://www.theaudiodb.com/api/v1/json/'
API_KEY = 1

class TheAudioDbWrapper(object):

    '''
    wpapper for fetching theaudiodb.com using the JSON API
    '''

    def __init__(self):

        self.artistname = None
        self.artistid = None
        self.artistmbid = None

        self.albumname = None
        self.albumid = None
        self.albummbid = None


    def clearAttr(self):

        self.__init__()

    def fetchAudioDB(self, query):

        if query:
            try:
                data = urllib2.urlopen('%s/%s%s' % (AUDIO_DB, API_KEY, query), None, timeout=3)
            except (urllib2.URLError, socket.timeout):
                return None
            return json.loads(data.read())
            if data and (data.get('artists', False) or data.get('album', False)): return data[0][0]
        return None


    def getArtistDetails(self):
        '''
        reads MBID (MusicBrainz), ID (TheAudioDB) or name of artist from class property
        :return: Detailed info of artist as dict
        '''

        _query = None
        if self.artistmbid: _query = '/artist-mb.php?i=%s' % (self.artistmbid)
        elif self.artistid: _query = '/artist.php?i=%s' % (self.artistid)
        elif self.artistname: _query = '/search.php?s=%s' % (urllib2.quote(self.artistname))

        data = self.fetchAudioDB(_query)
        if data and data.get('artists', False): return data['artists'][0]
        return None


    def getArtistArtwork(self):
        '''
        reads MBID (MusicBrainz), ID (TheAudioDB) or name of artist from class property
        :return: artwork selected from getArtistDetails as subset (dict):
            banner, fanart, clearart, thumb, logo
        '''

        artist_artwork = dict()
        data = self.getArtistDetails()
        if data:
            artist_artwork.update({'banner': data.get('strArtistBanner', None), 'fanart': data.get('strArtistFanart', None),
                            'clearart': data.get('strArtistClearart', None), 'thumb': data.get('strArtistThumb', None),
                            'widethumb': data.get('strArtistWideThumb', None), 'logo': data.get('strArtistLogo', None)})
            return artist_artwork
        return None


    def getAlbumDetails(self):
        '''
        reads MBID (MusicBrainz), ID (TheAudioDB) or name (needs additional artist name)of Album from class property
        :return: detailed info of album as dict
        '''

        _query = None
        if self.albummbid: _query = '/album-mb.php?i=%s' % (self.albummbid)
        elif self.albumid: _query = '/album.php?m=%s' % (self.albumid)
        elif self.artistname and self.albumname:
            _query = '/searchalbum.php?s=%s&a=%s' % (urllib2.quote(self.artistname), urllib2.quote(self.albumname))

        data = self.fetchAudioDB(_query)
        if data and data.get('album', False): return data['album'][0]
        return None


    def getAlbumArtwork(self):

        album_artwork = dict()
        data = self.getAlbumDetails()
        if data:
            album_artwork.update({'CDart': data.get('strAlbumCDart', None), 'thumb': data.get('strAlbumThumb', None),
                                  'thumbback': data.get('strAlbumThumbBack', None)})
            return album_artwork
        return None
