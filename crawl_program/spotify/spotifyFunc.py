import sys
import json
import requests
from utils.auth import getHeader, postHeader


# ******************************
#    Client Credentials Flow
# ******************************
# Get artist all albums, filtered and sorted
def getArtistAllAlbums(token, artistId):
    # First request
    limit = 50
    albumsEndPoint = f"https://api.spotify.com/v1/artists/{artistId}/albums?limit={limit}&offset=0"
    getHeaders = getHeader(token)
    artistAlbums = requests.get(albumsEndPoint, headers=getHeaders).json()
    allAlbums = artistAlbums['items']
    # More requests
    moreAlbumUri = artistAlbums['next']
    while moreAlbumUri != None:
        albumRes = requests.get(moreAlbumUri, headers=getHeaders).json()
        allAlbums.extend(albumRes['items'])
        moreAlbumUri = albumRes['next']
    return allAlbums


# Get artist albums by request once
def getArtistAlbumsOnce(token, artistId, limit, offset):
    albumsEndPoint = f"https://api.spotify.com/v1/artists/{artistId}/albums?limit={limit}&offset={offset}"
    getHeaders = getHeader(token)
    res = requests.get(albumsEndPoint, headers=getHeaders)
    albumsObject = res.json()
    return albumsObject


# Get one album's tracks
def getAlbumTracks(token, albumId, limit, offset):
    albumTracksEndPoint = f"https://api.spotify.com/v1/albums/{albumId}/tracks?limit={limit}&offset={offset}"
    getHeaders = getHeader(token)
    res = requests.get(albumTracksEndPoint, headers=getHeaders)
    albumTracksObject = res.json()
    return albumTracksObject


# Get single track
def getSingleTrack(token, trackId):
    trackEndPoint = f"https://api.spotify.com/v1/tracks/{trackId}"
    getHeaders = getHeader(token)
    res = requests.get(trackEndPoint, headers=getHeaders)
    atrackObject = res.json()
    return atrackObject


# Get artists info
def getArtistInfo(token, artistList, language=None):
    artistsEndPoint = "https://api.spotify.com/v1/artists?ids=" + \
        ','.join(artistList)
    getHeaders = {
        "Authorization": "Bearer " + token
    }
    if language != None:
        getHeaders["accept-language"] = language
    res = requests.get(artistsEndPoint, headers=getHeaders)
    artistsObject = res.json()
    return artistsObject


# Get playlist and all its tracks
def getPlaylistAndAllTracks(token, playlistID, isPrivate=False, spotify=None):
    playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}?offset=100&limit=100"
    getHeaders = getHeader(token)
    if isPrivate:
        res = spotify.get(playlistEndPoint)
    else:
        res = requests.get(playlistEndPoint, headers=getHeaders)
    playlistObject = res.json()
    # Request more if there is more tracks
    moreTracksUri = playlistObject['tracks']['next']
    while moreTracksUri != None:
        if isPrivate:
            tracksRes = spotify.get(moreTracksUri).json()
        else:
            tracksRes = requests.get(moreTracksUri, headers=getHeaders).json()
        playlistObject['tracks']['items'].extend(tracksRes['items'])
        moreTracksUri = tracksRes['next']
    return playlistObject


# Get playlist's tracks by request once
def getPlaylistTracks(token, playlistID, limit, offset):
    playlistTracksEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?limit={limit}&offset={offset}"
    getHeaders = getHeader(token)
    res = requests.get(playlistTracksEndPoint, headers=getHeaders)
    playlistTracksObject = res.json()
    return playlistTracksObject


# ******************************
#       Third Party API
# ******************************
# Get one album's tracks by third party api
def getAlbumTracksByThirdPartyAPI(token, albumId):
    albumTracksEndPoint = f"https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryAlbumTracks"\
        f"&variables=%7B%22uri%22%3A%22spotify%3Aalbum%3A{albumId}%22%2C%22offset%22%3A0%2C%22limit%22%3A300%7D"\
        f"&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2217a905fd6424e17cef6d815704aaae8e11c0cfa54a998a09e8690fe7f4f09878%22%7D%7D"
    getHeaders = getHeader(token)
    res = requests.get(albumTracksEndPoint, headers=getHeaders)
    if (res.status_code == 401):
        print('\n**********')
        print('Spotify token expired, please retrive a new token.')
        print('**********\n')
        sys.exit()
    albumTracksObject = res.json()
    return albumTracksObject


# ******************************
#    Authorization Code Flow
# ******************************
# Get my all liked songs
def getUserAllLikedSongs(spotify, token):
    userTracksEndPoint = f"https://api.spotify.com/v1/me/tracks?limit=50&offset=0"
    res = spotify.get(userTracksEndPoint)
    userTracksObject = res.json()
    # Request more if there is more tracks
    moreTracksUri = userTracksObject['next']
    while moreTracksUri != None:
        tracksRes = spotify.get(moreTracksUri).json()
        userTracksObject['items'].extend(tracksRes['items'])
        moreTracksUri = tracksRes['next']
    return userTracksObject


# Get my liked songs by request once
def getUserSavedTracks(spotify, token, limit=50, offset=0):
    userTracksEndPoint = f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}"
    res = spotify.get(userTracksEndPoint)
    userTracksObject = res.json()
    return userTracksObject


# Create playlist
def createPlayList(spotify, token, userId, name, description, ispublic):
    createPlaylistEndPoint = f"https://api.spotify.com/v1/users/{userId}/playlists"
    postHeaders = postHeader(token)
    postData = {
        "name": name,
        "description": description,
        "public": ispublic
    }
    res = spotify.post(createPlaylistEndPoint,
                       headers=postHeaders, data=json.dumps(postData))
    if res.status_code == 201:
        print('\n**********')
        print('Successfully created playlist.')
        print('**********\n')
    else:
        print('\n**********')
        print('Creating playlist failed.')
        print('**********\n')
        print(res)
        sys.exit()
    playlistObject = res.json()
    return playlistObject


# Update playlist
def updatePlayList(spotify, token, playlistId, name, description, ispublic):
    updatePlaylistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistId}"
    postHeaders = postHeader(token)
    postData = {
        "name": name,
        "description": description,
        "public": ispublic
    }
    res = spotify.put(updatePlaylistEndPoint,
                      headers=postHeaders, data=json.dumps(postData))
    if res.status_code == 200:
        print('\n**********')
        print('Successfully updated playlist.')
        print('**********\n')
    else:
        print('\n**********')
        print('Updating playlist failed.')
        print('**********\n')
    return res


# Add tracks to playlist
def addTracksToPlayList(spotify, token, playlistId, trackUriList):
    playlistAddTracksEndPoint = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    postHeaders = postHeader(token)
    postData = {
        "uris": trackUriList
    }
    res = spotify.post(playlistAddTracksEndPoint,
                       headers=postHeaders, data=json.dumps(postData))
    resJson = res.json()
    if res.status_code == 201:
        print('\n**********')
        print('Successfully add tracks to playlist.')
        print('**********\n')
    else:
        print('\n**********')
        print('Adding tracks to playlist failed.')
        print(resJson)
        print('**********\n')
    return resJson


# Add tracks to playlist by number
def addTracksToPlaylistByNumber(spotify, token, playlistId, allTracks, tracksNumber):
    toAddTracks = allTracks[0:tracksNumber] if tracksNumber < len(
        allTracks) else allTracks
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


# Remove playlist tracks
def removePlayListTracks(spotify, token, playlistId, trackUriList):
    playlistAddTracksEndPoint = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    postHeaders = postHeader(token)
    postData = {
        "uris": trackUriList
    }
    res = spotify.delete(playlistAddTracksEndPoint,
                         headers=postHeaders, data=json.dumps(postData))
    resJson = res.json()
    if res.status_code == 200:
        print('\n**********')
        print('Successfully remove playlist tracks.')
        print('**********\n')
    else:
        print('\n**********')
        print('Removing playlist tracks failed.')
        print(resJson)
        print('**********\n')
    return resJson


# ******************************
#         Util Function
# ******************************
# Read file content
def readFileContent(fileName):
    with open(fileName) as f:
        return f.read()


# Print albums info
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
