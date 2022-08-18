import requests
from utils.auth import *
from secrets import *


def getArtistAllAlbums(artistId):  # Get artist all albums, filtered and sorted
    token = getAccessToken(clientID, clientSecret)
    limit = 50
    artistAlbums = getArtistAlbums(token, artistId, limit, 0)
    allAblums = artistAlbums['items']
    # printAlbums(artistAlbums, 0)
    moreRequestTimes = artistAlbums['total'] // limit
    for i in range(moreRequestTimes):
        offset = limit * (i + 1)
        moreArtistAlbums = getArtistAlbums(token, artistId, limit, offset)
        allAblums.extend(moreArtistAlbums['items'])
        # printAlbums(moreArtistAlbums, offset)
    # Filter ablums to album and single
    for album in allAblums[::-1]:
        if (album['album_type'] != 'album' and album['album_type'] != 'single'):
            allAblums.remove(album)
    # Sort albums
    allAblums = sorted(allAblums, key=lambda a: a['release_date'])
    return allAblums


def getArtistAlbums(token, artistId, limit, offset):  # Get artist albums by one request
    albumsEndPoint = f"https://api.spotify.com/v1/artists/{artistId}/albums?limit={limit}&offset={offset}"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(albumsEndPoint, headers=getHeader)
    albumsObject = res.json()
    return albumsObject


def printAlbums(artistAlbums, count):  # Print albums info
    for t in artistAlbums['items']:
        print('--------------------')
        count = count + 1
        albumName = str(count) + ': ' + t['name']
        albumGroup = 'Group: ' + t['album_group']
        albumType = 'Type:  ' + t['album_type']
        releaseDate = 'Date:  ' + t['release_date']
        tracksNum = 'Tracks: ' + str(t['total_tracks'])
        artists = 'Artists: '
        artistsList = t['artists']
        for i in range(len(artistsList)):
            artists = artists + artistsList[i]['name'] + \
                (', ' if i < len(artistsList) - 1 else '')
        print(albumName, albumGroup, albumType,
              releaseDate, tracksNum, artists, sep='\n')


def getAlbumTracks(token, albumId, limit, offset):  # Get one album's tracks
    albumTracksEndPoint = f"https://api.spotify.com/v1/albums/{albumId}/tracks?limit={limit}&offset={offset}"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    # print(albumTracksEndPoint)
    res = requests.get(albumTracksEndPoint, headers=getHeader)
    albumTracksObject = res.json()
    return albumTracksObject


# Get one album's tracks by third party api
# Token is retrived by spotify page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa,
# find https://api-partner.spotify.com/pathfinder/v1/query request and copy from its authorization header
def getAlbumTracksByThirdPartyAPI(token, albumId):
    albumTracksEndPoint = f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryAlbumTracks"\
        f"&variables=%7B%22uri%22%3A%22spotify%3Aalbum%3A{albumId}%22%2C%22offset%22%3A0%2C%22limit%22%3A300%7D"\
        f"&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2217a905fd6424e17cef6d815704aaae8e11c0cfa54a998a09e8690fe7f4f09878%22%7D%7D"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    # print(albumTracksEndPoint)
    res = requests.get(albumTracksEndPoint, headers=getHeader)
    # print(type(res))
    # print(res)
    if (res.status_code == 401):
        print('**********')
        print('Spotify token expired, please retrive a new token.')
        print('**********')
        raise
    albumTracksObject = res.json()
    return albumTracksObject


def getSingleTrack(token, trackId):  # Get single track
    trackEndPoint = f"https://api.spotify.com/v1/tracks/{trackId}"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    # print(albumTracksEndPoint)
    res = requests.get(trackEndPoint, headers=getHeader)
    atrackObject = res.json()
    return atrackObject
