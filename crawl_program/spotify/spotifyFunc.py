import sys
import json
import requests
from utils.auth import getHeader, postHeader
from artists import artists


# ******************************
#    Client Credentials Flow
# ******************************
# Get artist all albums, filtered and sorted
def getArtistAllAlbums(token, artistId, market=None):
    # First request
    limit = 50
    albumsEndPoint = f"https://api.spotify.com/v1/artists/{artistId}/albums?limit={limit}&offset=0"
    getHeaders = getHeader(token)
    if market != None:
        getHeaders['market'] = market
    # print(getHeaders)
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


# Get single album
def getSingleAlbum(token, albumId):
    albumEndPoint = f"https://api.spotify.com/v1/albums/{albumId}"
    getHeaders = getHeader(token)
    res = requests.get(albumEndPoint, headers=getHeaders)
    atrackObject = res.json()
    return atrackObject


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
    getHeaders = {
        "Authorization": "Bearer " + token
    }
    if language != None:
        getHeaders["accept-language"] = language
    allArtists = {'artists': []}
    for i in range(0, len(artistList), 50):
        artistsEndPoint = "https://api.spotify.com/v1/artists?ids=" + \
            ','.join(artistList[i:i+50])
        artistsObject = requests.get(
            artistsEndPoint, headers=getHeaders).json()
        allArtists['artists'].extend(artistsObject['artists'])
    return allArtists


# Get playlist and all its tracks
def getPlaylistAndAllTracks(token, playlistID, isPrivate=False, spotify=None):
    playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}?offset=100&limit=100"
    if isPrivate:
        res = spotify.get(playlistEndPoint, headers={
                          "accept-language": "zh-CN"})
    else:
        res = requests.get(playlistEndPoint, headers=getHeader(token))
    playlistObject = res.json()
    if res.status_code != 200:
        print('Get playlist error:', res, playlistObject)
        print('playlistID:', playlistID)
        print('isPrivate:', isPrivate)
        print('playlistEndPoint:', playlistEndPoint)
        sys.exit()
    # Request more if there is more tracks
    moreTracksUri = playlistObject['tracks']['next']
    while moreTracksUri != None:
        if isPrivate:
            tracksRes = spotify.get(
                moreTracksUri, headers={"accept-language": "zh-CN"}).json()
        else:
            tracksRes = requests.get(
                moreTracksUri, headers=getHeader(token)).json()
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
# Get my following artists
def getFollowingArtists(spotify, token, limit, language=None):
    followingArtistsEndPoint = f"https://api.spotify.com/v1/me/following?type=artist&limit={limit}"
    if language == None:
        res = spotify.get(followingArtistsEndPoint)
    else:
        res = spotify.get(followingArtistsEndPoint, headers={
            "accept-language": language})
    artists = res.json()
    # Request more if there is more tracks
    moreArtistsUri = artists['artists']['next']
    while moreArtistsUri != None:
        if language == None:
            artistsRes = spotify.get(moreArtistsUri).json()
        else:
            artistsRes = spotify.get(moreArtistsUri, headers={
                "accept-language": language}).json()
        artists['artists']['items'].extend(artistsRes['artists']['items'])
        moreArtistsUri = artistsRes['artists']['next']
    return artists


# Get my all liked songs
def getUserAllLikedSongs(spotify, token):
    userTracksEndPoint = f"https://api.spotify.com/v1/me/tracks?limit=50&offset=0"
    res = spotify.get(userTracksEndPoint, headers={"accept-language": "zh-CN"})
    userTracksObject = res.json()
    # Request more if there is more tracks
    moreTracksUri = userTracksObject['next']
    while moreTracksUri != None:
        tracksRes = spotify.get(moreTracksUri, headers={
                                "accept-language": "zh-CN"}).json()
        userTracksObject['items'].extend(tracksRes['items'])
        moreTracksUri = tracksRes['next']
    return userTracksObject


# Get my liked songs by request once
def getUserSavedTracks(spotify, token, limit=50, offset=0):
    userTracksEndPoint = f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}"
    res = spotify.get(userTracksEndPoint, headers={"accept-language": "zh-CN"})
    userTracksObject = res.json()
    return userTracksObject


# Get my liked songs by request once
def saveUserTracks(spotify, token, idStr):
    userTracksEndPoint = f"https://api.spotify.com/v1/me/tracks?ids={idStr}"
    res = spotify.put(userTracksEndPoint)
    return res


# Get my liked songs by request once
def unSaveUserTracks(spotify, token, idStr):
    userTracksEndPoint = f"https://api.spotify.com/v1/me/tracks?ids={idStr}"
    res = spotify.delete(userTracksEndPoint)
    return res


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
        "public": ispublic
    }
    if name != None:
        postData['name'] = name
    if description != None:
        postData['description'] = description
    res = spotify.put(updatePlaylistEndPoint,
                      headers=postHeaders, data=json.dumps(postData))
    print('\n**********')
    print("Updating playlist info...")
    if res.status_code == 200:
        print('Successfully updated playlist.')
    else:
        print('Updating playlist failed.')
    if name != None:
        print('Playlist name:', name)
    if description != None:
        print('Playlist description:', description)
    print('Response:', res.text if res.text else 'ok.')
    print('**********\n')
    return res


# Add tracks to playlist
def addTracksToPlayList(spotify, token, playlistId, trackUriList):
    playlistAddTracksEndPoint = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    postHeaders = postHeader(token)
    print('\n**********')
    print("Adding tracks to playlist...")
    if (len(trackUriList) == 0):
        print('Nothing to add...')
        return None
    for i in range(0, len(trackUriList), 100):
        postData = {
            "uris": trackUriList[i:i+100]
        }
        res = spotify.post(playlistAddTracksEndPoint,
                           headers=postHeaders, data=json.dumps(postData))
        resJson = res.json()
        if res.status_code == 201:
            print('Successfully add tracks to playlist.')
        else:
            print('\n**********')
            print('Adding tracks to playlist failed.')
            print(resJson)
    print('Response:', resJson)
    print('**********\n')
    return resJson


# Add tracks to playlist by number
def addTracksToPlaylistByNumber(spotify, token, playlistId, artist, allTracks, tracksNumber):
    if artists[artist].get('excludeTracks') != None:
        allTracks = [track for track in allTracks if track['trackUri'] not in
                     ['spotify:track:' + trackId for trackId in list(artists[artist]['excludeTracks'].keys())]]
    toAddTracks = allTracks[0:tracksNumber] if tracksNumber < len(
        allTracks) else allTracks
    trackUriList = [track['trackUri'] for track in toAddTracks]
    specialAddingTracks = {}
    if artists[artist].get('includeTracks') != None:
        for trackId, trackName in artists[artist]['includeTracks'].items():
            trackUri = 'spotify:track:' + trackId
            if trackUri in trackUriList:
                continue
            trackUriList.append(trackUri)
            specialAddingTracks = specialAddingTracks | {trackId: trackName}
    resJson = addTracksToPlayList(spotify, token, playlistId, trackUriList)
    return resJson, specialAddingTracks


# Add tracks to playlist by playcount
def addTracksToPlaylistByPlaycount(spotify, token, playlistId, artist, allTracks, playcount):
    if artists[artist].get('excludeTracks') != None:
        allTracks = [track for track in allTracks if track['trackUri'] not in
                     ['spotify:track:' + trackId for trackId in list(artists[artist]['excludeTracks'].keys())]]
    trackUriList = []
    for track in allTracks:
        if track['playcount'] < playcount:
            break
        else:
            trackUriList.append(track['trackUri'])
    if artists[artist].get('includeTracks') != None:
        trackUriList.extend(['spotify:track:' + trackId
                             for trackId in list(artists[artist]['includeTracks'].keys())])
    resJson = addTracksToPlayList(spotify, token, playlistId, trackUriList)
    return resJson


# Remove playlist tracks
def removePlayListTracks(spotify, token, playlistId, trackUriList):
    playlistAddTracksEndPoint = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    postHeaders = postHeader(token)
    print('\n**********')
    print('Removing playlist tracks...')
    if (len(trackUriList) == 0):
        print('Nothing to remove...')
        return None
    for i in range(0, len(trackUriList), 100):
        postData = {
            "uris": trackUriList[i:i+100]
        }
        res = spotify.delete(playlistAddTracksEndPoint,
                             headers=postHeaders, data=json.dumps(postData))
        resJson = res.json()
        if res.status_code == 200:
            print('Successfully remove playlist tracks.')
        else:
            print('Removing playlist tracks failed.')
    print(resJson)
    print('**********\n')
    return resJson


# Unfollow playlist
def unfollowPlayList(spotify, token, playlistId):
    playlistAddTracksEndPoint = f"https://api.spotify.com/v1/playlists/{playlistId}/followers"
    postHeaders = postHeader(token)
    res = spotify.delete(playlistAddTracksEndPoint, headers=postHeaders)
    if res.status_code == 200:
        print('\n**********')
        print('Successfully unfollowed playlist.')
        print(res)
        # print(res.content)
        print('**********\n')
        return True
    else:
        print('\n**********')
        print('Unfollowing playlist tracks failed.')
        print(res)
        print(res.content)
        print('**********\n')
        return False


# ******************************
#         Util Function
# ******************************
# Read file content
def readFileContent(fileName):
    with open(fileName) as f:
        return f.read()


# Sure check
def sureCheck():
    msg = input('Are you sure? Press Y to continue: ')
    if msg != 'y' and msg != 'Y':
        sys.exit()


# Get playcount string
def getPlaycountStr(playcount):
    if playcount >= 10000000000:
        playcountStr = str(
            playcount // 1000000000) + ' billion'
    elif playcount >= 1000000000:
        playcountStr = str(
            playcount // 100000000 / 10) + ' billion'
    elif playcount >= 10000000:
        playcountStr = str(
            playcount // 1000000) + ' million'
    elif playcount >= 1000000:
        playcountStr = str(
            playcount // 100000 / 10) + ' million'
    else:
        playcountStr = str(playcount)
    return playcountStr


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
