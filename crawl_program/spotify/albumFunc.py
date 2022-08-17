import requests
from utils.auth import *
from secrets import *


def getArtistAlbums(token, artistId, limit, offset):
    albumsEndPoint = f"https://api.spotify.com/v1/artists/{artistId}/albums?limit={limit}&offset={offset}"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(albumsEndPoint, headers=getHeader)
    albumsObject = res.json()
    return albumsObject


def printAlbums(artistAlbums, count):
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


# API requests, get all albums
def getAllAlbums(artistId):
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
