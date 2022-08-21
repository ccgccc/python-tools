import requests
import json
import sys
from utils.auth import *
from utils.secrets import clientID, clientSecret


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
    # Filter ablums type to album and single
    for album in allAblums[::-1]:
        if (album['album_type'] != 'album' and album['album_type'] != 'single'):
            allAblums.remove(album)
    # Sort albums by release date
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


# Get one album's tracks by third party api
def getAlbumTracksByThirdPartyAPI(token, albumId):
    albumTracksEndPoint = f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryAlbumTracks"\
        f"&variables=%7B%22uri%22%3A%22spotify%3Aalbum%3A{albumId}%22%2C%22offset%22%3A0%2C%22limit%22%3A300%7D"\
        f"&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2217a905fd6424e17cef6d815704aaae8e11c0cfa54a998a09e8690fe7f4f09878%22%7D%7D"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(albumTracksEndPoint, headers=getHeader)
    if (res.status_code == 401):
        print('\n**********')
        print('Spotify token expired, please retrive a new token.')
        print('**********\n')
        sys.exit()
    albumTracksObject = res.json()
    return albumTracksObject


def getAlbumTracks(token, albumId, limit, offset):  # Get one album's tracks
    albumTracksEndPoint = f"https://api.spotify.com/v1/albums/{albumId}/tracks?limit={limit}&offset={offset}"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    # print(albumTracksEndPoint)
    res = requests.get(albumTracksEndPoint, headers=getHeader)
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


def getPlaylistAndAllTracks(playlistID):  # Get playlist and all its tracks
    token = getAccessToken(clientID, clientSecret)
    playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}?offset=100&limit=100"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(playlistEndPoint, headers=getHeader)
    playlistObject = res.json()
    # request more if there is more tracks
    moreTracksUri = playlistObject['tracks']['next']
    while moreTracksUri != None:
        tracksRes = requests.get(moreTracksUri, headers=getHeader).json()
        # print(tracksRes)
        playlistObject['tracks']['items'].extend(tracksRes['items'])
        moreTracksUri = tracksRes['next']
    return playlistObject


def getPlaylistTracks(token, playlistID, limit, offset):  # Get playlist's tracks
    playlistTracksEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?limit={limit}&offset={offset}"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(playlistTracksEndPoint, headers=getHeader)
    playlistTracksObject = res.json()
    return playlistTracksObject


def createPlayList(spotify, token, userId, name, description, ispublic):  # Create playlist
    createPlaylistEndPoint = f"https://api.spotify.com/v1/users/{userId}/playlists"
    postHeader = {
        "Content-Type": "application/json"
    }
    postData = {
        "name": name,
        "description": description,
        "public": ispublic
    }
    res = spotify.post(createPlaylistEndPoint,
                       headers=postHeader, data=json.dumps(postData))
    # print(res)
    if res.status_code == 201:
        print('\n**********')
        print('Successfully created playlist.')
        print('**********\n')
    else:
        print('\n**********')
        print('Creating playlist failed.')
        print('**********\n')
    playlistObject = res.json()
    return playlistObject


def updatePlayList(spotify, token, playlistId, name, description, ispublic):  # Create playlist
    updatePlaylistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistId}"
    postHeader = {
        "Content-Type": "application/json"
    }
    postData = {
        "name": name,
        "description": description,
        "public": ispublic
    }
    res = spotify.put(updatePlaylistEndPoint,
                      headers=postHeader, data=json.dumps(postData))
    # print(res)
    if res.status_code == 200:
        print('\n**********')
        print('Successfully updated playlist.')
        print('**********\n')
    else:
        print('\n**********')
        print('Updating playlist failed.')
        print('**********\n')
    return res


def addTracksToPlayList(spotify, token, playlistId, trackUriList):  # Add tracks to playlist
    playlistAddTracksEndPoint = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    postHeader = {
        "Content-Type": "application/json"
    }
    postData = {
        "uris": trackUriList
    }
    res = spotify.post(playlistAddTracksEndPoint,
                       headers=postHeader, data=json.dumps(postData))
    # print(res)
    if res.status_code == 201:
        print('\n**********')
        print('Successfully add tracks to playlist.')
        print('**********\n')
    else:
        print('\n**********')
        print('Add tracks to playlist failed.')
        print('**********\n')
    resJson = res.json()
    return resJson


# Add tracks to playlist by number
def addTracksToPlaylistByNumber(spotify, token, playlistId, allTracks, tracksNumber):
    toAddTracks = allTracks[0:tracksNumber] if tracksNumber < len(
        allTracks) else allTracks
    # query string format, not recommended
    # trackUris = ''
    # i = 0
    # for i in range(len(toAddTracks)):
    #     trackUris = trackUris + \
    #         toAddTracks[i]['trackUri'] + \
    #         (',' if i < len(toAddTracks) - 1 else '')
    # print(trackUris)
    # post json format
    trackUriList = []
    for track in toAddTracks:
        trackUriList.append(track['trackUri'])
    resJson = addTracksToPlayList(spotify, token, playlistId, trackUriList)
    return resJson


# Add tracks to playlist by playcount
def addTracksToPlaylistByPlaycount(spotify, token, playlistId, allTracks, playcount):
    trackUriList = []
    for track in allTracks:
        if track['playcount'] < playcount:
            break
        else:
            trackUriList.append(track['trackUri'])
    resJson = addTracksToPlayList(spotify, token, playlistId, trackUriList)
    return resJson


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
