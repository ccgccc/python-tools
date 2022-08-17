from platform import release
import requests
import json
from utils.auth import *
from secrets import *

# ******************************
#    抓取 Spotify 艺人专辑
# ******************************

# 此处定义播放列表id
artistId = "2QcZxAgcs2I1q7CtCkl6MI"


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
            artists = artists + artistsList[i]['name'] + (', ' if i < len(artistsList) - 1 else '')
        print(albumName, albumGroup, albumType, releaseDate, tracksNum, artists, sep='\n')


# API requests
token = getAccessToken(clientID, clientSecret)
limit = 50
artistAlbums = getArtistAlbums(token, artistId, limit, 0)
allAblums = artistAlbums['items']
printAlbums(artistAlbums, 0)

moreRequestTimes = artistAlbums['total'] // limit
for i in range(moreRequestTimes):
    offset = limit * (i + 1)
    moreArtistAlbums = getArtistAlbums(token, artistId, limit, offset)
    allAblums.extend(moreArtistAlbums['items'])
    printAlbums(moreArtistAlbums, offset)

# print(tracklist)
# Write json to file
# with open('albums.json', 'w') as f:
#     # json.dump(artistAlbums, f)
#     json.dump(allAblums, f)

# i = 0
# for t in allAblums:
#     print('--------------------')
#     i = i + 1
#     print(str(i) + ': ' + t['name'])
#     print('Date: ' + t['release_date'])
#     print('Tracks: ' + str(t['total_tracks']))

# print('--------------------')
# print('Album Statistic:')

