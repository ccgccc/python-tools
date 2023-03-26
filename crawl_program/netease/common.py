import os
import re
import sys
import json
import time
import requests
from datetime import datetime
from artists import *

# Define my user id
myUserId = 389958855
# Define my user name
myUserName = 'ccgccc'

# Define baseUrl
global baseUrl
baseUrl = 'https://service-4ipff8tq-1259202535.gz.apigw.tencentcs.com/release'
# baseUrl = 'https://netease-cloud-music-api-three-rose.vercel.app'

# Define headers to get private info in terminal
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
# First use https://service-4ipff8tq-1259202535.gz.apigw.tencentcs.com/release/qrlogin.html
#   in browser to log in,
# Then use https://service-4ipff8tq-1259202535.gz.apigw.tencentcs.com/release/login/status
#   and copy cookie from request.
# Define cookie in cookie.txt
os.chdir(os.path.dirname(__file__))
with open('cookie.txt') as f:
    headers['cookie'] = f.read()


def setBaseUrl(needCheck=False):
    global baseUrl
    baseUrl = 'https://netease-cloud-music-api-three-rose.vercel.app'
    if needCheck:
        print('\nBaseUrl changed:', baseUrl)
        msg = input('Set proxy to global mode. Press Y to continue: ')
        if msg != 'y' and msg != 'Y':
            sys.exit()


def setBaseUrl2(needCheck=False):
    global baseUrl
    baseUrl = 'https://service-4ipff8tq-1259202535.gz.apigw.tencentcs.com/release'
    if needCheck:
        print('BaseUrl changed:', baseUrl)
        msg = input('Set proxy to pac mode. Press Y to continue: ')
        if msg != 'y' and msg != 'Y':
            sys.exit()


def getBaseUrl():
    return baseUrl


def getAlbum(id):
    url = baseUrl + '/album'
    params = {
        'id': id
    }
    album = requests.get(url, params=params).json()
    return album


def getArtistAlbums(artistId):
    url = baseUrl + '/artist/album'
    limit = 100
    params = {
        'id': artistId,
        'limit': limit,
        'offset': 0
    }
    resJson = requests.get(url, params=params).json()
    allAlbums = resJson['hotAlbums']
    # while allAlbums['more'] == True: # seems not working
    while len(resJson['hotAlbums']) == limit:
        params['offset'] = params['offset'] + limit
        print(params)
        resJson = requests.get(url, headers=headers, params=params).json()
        allAlbums.extend(resJson['hotAlbums'])
    return allAlbums


def getArtistSongs(artist):
    url = baseUrl + '/artist/songs'
    # url = baseUrl + '/artist/top/song'
    limit = 200  # max 200
    params = {
        'id': artists[artist]['artistId'],
        'limit': limit,
        'offset': 0
    }
    resJson = requests.get(url, headers=headers, params=params).json()
    allSongs = resJson
    while resJson['more'] == True:
        params['offset'] = params['offset'] + limit
        print(params)
        resJson = requests.get(url, headers=headers, params=params).json()
        allSongs['songs'].extend(resJson['songs'])
    return allSongs


def getSongLyric(songId):
    url = baseUrl + '/lyric'
    params = {
        'id': songId
    }
    lyric = requests.get(url, params=params).json()
    return lyric


def getSongComments(songId, limit=5):
    url = baseUrl + '/comment/music'
    params = {
        'id': songId,
        'limit': limit
    }
    comments = requests.get(url, params=params).json()
    return comments


def getPlaylist(playlistId):
    url = baseUrl + '/playlist/detail'
    params = {
        'id': playlistId,
        # 'timestamp': int(time.time() * 1000)
    }
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 401:
        print('请求失败！返回信息：' + res.text)
        sys.exit()
    playlist = res.json()
    # print(json.dumps(playlist, ensure_ascii=False))
    return playlist


def getPlaylistSongs(playlistId, addTs=False):
    url = baseUrl + '/playlist/track/all'
    limit = 500
    params = {
        'id': playlistId,
        'limit': limit,
        'offset': 0
    }
    if addTs:
        params['timestamp'] = int(time.time() * 1000)
    # print('Request start time(playlist tracks):', time.strftime("%H:%M:%S"))
    # print('Url:', url)
    # print('Params:', params)
    res = requests.get(url, headers=headers, params=params)
    # print('Request end time:', time.strftime("%H:%M:%S"), '\n')
    if res.status_code == 401:
        print('请求失败！返回信息：' + res.text)
        sys.exit()
    try:
        resJson = res.json()
    except:
        print(res)
        print(res.text)
        print('Request error, exit...')
        sys.exit()
    playlistSongs = resJson
    # print(json.dumps(resJson, ensure_ascii=False))
    while len(resJson['songs']) == limit:
        params['offset'] = params['offset'] + limit
        # print(params)
        resJson = requests.get(url, headers=headers, params=params).json()
        playlistSongs['songs'].extend(resJson['songs'])
        playlistSongs['privileges'].extend(resJson['privileges'])
    return playlistSongs


def createPlaylist(name, isPrivate=False):
    url = baseUrl + '/playlist/create'
    params = {
        'name': name
    }
    if isPrivate:
        params['privacy'] = 10
    else:
        params['privacy'] = 0
    res = requests.get(url, headers=headers, params=params)
    resJson = res.json()
    if res.status_code == 200 and resJson['code'] == 200:
        print('\n**********')
        print('Successfully created playlist.')
        print('**********\n')
        print(resJson)
        return resJson
    else:
        print('\n**********')
        print('Creating playlist failed.')
        print('**********\n')
        print(resJson)
        sys.exit()


def updatePlaylistDesc(playlistId,  description):
    url = baseUrl + '/playlist/desc/update'
    params = {
        'id': playlistId,
        'desc': description
    }
    res = requests.get(url, headers=headers, params=params)
    resJson = res.json()
    if res.status_code == 200:
        print('\n**********')
        print('Successfully updated playlist description.')
        print('Playlist description:', description)
        print('**********\n')
        print(resJson)
        return resJson
    else:
        print('\n**********')
        print('Updating playlist description failed.')
        print('Playlist description:', description)
        print('**********\n')
        print(resJson)
        sys.exit()


def deletePlaylist(playlistIds):
    url = baseUrl + '/playlist/delete'
    params = {
        'id': playlistIds
    }
    res = requests.get(url, headers=headers, params=params)
    resJson = res.json()
    if res.status_code == 200 and resJson['code'] == 200:
        print('\n**********')
        print('Successfully deleted playlist.')
        print('**********\n')
        print(resJson)
        return resJson
    else:
        print('\n**********')
        print('Deleting playlist failed.')
        print('**********\n')
        print(resJson)
        sys.exit()


def addSongsToPlayList(playlistId, tracks, addTs=True):
    res = addOrDeleteSongsToPlayList('add', playlistId, tracks, addTs=addTs)
    resJson = res.json()
    if res.status_code == 200 and resJson.get('body') != None and resJson['body']['code'] == 200:
        print('\n**********')
        print('Successfully added songs to playlist.')
        print('**********\n')
        print(resJson)
        return resJson
    else:
        print('\n**********')
        print('Adding songs to playlist failed.')
        print('**********\n')
        print(resJson)
        sys.exit()


def deleteSongsToPlayList(playlistId, tracks, addTs=True):
    res = addOrDeleteSongsToPlayList('del', playlistId, tracks, addTs=addTs)
    resJson = res.json()
    if res.status_code == 200 and resJson.get('body') != None \
            and resJson['body']['code'] == 200:
        print('\n**********')
        print('Successfully removed playlist songs.')
        print('**********\n')
        print(resJson)
        return resJson
    else:
        print('\n**********')
        print('Removing playlist songs failed.')
        print('**********\n')
        print(resJson)
        sys.exit()


def addOrDeleteSongsToPlayList(opeartion, playlistId, tracks, addTs=True):
    url = baseUrl + '/playlist/tracks'
    params = {
        'op': opeartion,
        'pid': playlistId,
        'tracks': tracks,
        'timestamp': int(time.time() * 1000)
    }
    if addTs:
        params['timestamp'] = int(time.time() * 1000)
    print('\nRequest time:', time.strftime("%H:%M:%S"))
    return requests.get(url, headers=headers, params=params)


def getFollows(userId):
    url = baseUrl + '/user/follows'
    limit = 500
    params = {
        'uid': userId,
        'limit': limit,
        'offset': 0
    }
    follows = requests.get(url, headers=headers, params=params).json()
    return follows


def followUser(followUserId):
    return followOrUnfollow(1, followUserId)


def unfollowUser(unfollowUserId):
    return followOrUnfollow(0, unfollowUserId)


def followOrUnfollow(operation, followUserId):
    url = baseUrl + '/follow'
    params = {
        'id': followUserId,
        't': operation
    }
    res = requests.get(url, headers=headers, params=params)
    return res


def likeSong(songId):
    url = baseUrl + '/like'
    params = {
        'id': songId
    }
    return requests.get(url, headers=headers, params=params)


def searchArtist(keywords):
    return search(100, keywords, limit=3)


def searchSong(keywords):
    return search(1, keywords)


def search(type, keywords, limit=None):
    url = baseUrl + '/cloudsearch'
    params = {
        'type': type,
        'keywords': keywords
    }
    if limit != None:
        params['limit'] = limit
    return requests.get(url, params=params).json()


def printAlbums(albums, csvFileName=None):
    print('--------------------')
    print('Albums:')
    isWriteToFile = csvFileName != None
    if isWriteToFile:
        csvFile = open('files/' + csvFileName + '.csv', 'w')
        csvFile.write('albumCount, albumId, albumName, albumArtists, ' +
                      'publishTime, albumType, albumSubType, albumSize, company\n')
    albumCount = 0
    for album in albums:
        albumCount = albumCount + 1
        albumId = album['id']
        albumName = re.sub(r'\,', '，', album['name'])
        albumAlias = album['alias']
        albumType = album['type']
        albumSubType = album['subType']
        albumSize = album['size']
        albumArtists = '_'.join(
            list(map(lambda artist: artist['name'], album['artists'])))
        publishMs = album.get('publishTime')
        publishTime = datetime.fromtimestamp(
            publishMs / 1000).strftime('%Y-%m-%d') if publishMs != None else '--'
        company = album['company']
        print(albumCount, albumId, albumName, albumArtists,
              publishTime, albumType, albumSubType, albumSize, company, sep=', ')
        if isWriteToFile:
            print(albumCount, albumId, albumName, albumArtists, publishTime,
                  albumType, albumSubType, albumSize, company, sep=', ', file=csvFile)
    if isWriteToFile:
        csvFile.close()


def printSongs(songs, reverse=False, csvFileName=None, isWriteToConsole=True):
    if reverse:
        songs.reverse()
    isWriteToFile = csvFileName != None
    if isWriteToConsole:
        print('----------')
        print('Songs:')
    if isWriteToFile:
        csvFile = open('files/' + csvFileName + '.csv', 'w')
        csvFile.write('songCount, songId, songName, songArtists, ' +
                      'genre, duration, publishTime, popularity, albumName\n')
    processedSongs = []
    songCount = 0
    artistDict = {v['artistId']: k for k, v in artists.items()}
    for song in songs:
        songCount = songCount + 1
        songId = song['id']
        songName = re.sub(r'\,', '，', song['name'])
        songAlias = song['alia']
        artistKeys = [artistDict[ar['id']]
                      for ar in song['ar'] if ar['id'] in artistDict]
        songArtists = '/'.join(
            list(map(lambda artist: re.sub(r'\,', '，', artist['name']), song['ar'])))
        durationMs = song['dt']
        duration = "{:02d}".format(durationMs // 60000) + ":" + \
            "{:02d}".format(durationMs // 1000 % 60)
        publishMs = song.get('publishTime')
        publishTime = datetime.fromtimestamp(
            publishMs / 1000).strftime('%Y-%m-%d') if publishMs != None else '--'
        genre = song.get('eq')
        genre = '--' if genre == None else genre
        popularity = song['pop']
        albumId = song['al']['id']
        albumName = re.sub(r'\,', '，', song['al']['name'])
        processedSongs.append({'song': song, 'id': songId, 'name': songName, 'artistKeys': artistKeys, 'artists': songArtists, 'genre': genre,
                              'duration': duration, 'publishTime': publishTime, 'popularity': popularity, 'albumId': albumId, 'albumName': albumName})
        if isWriteToConsole:
            print(songCount, songId, songName, songArtists, genre,
                  duration, publishTime, popularity, albumName, sep=', ')
        if isWriteToFile:
            print(songCount, songId, songName, songArtists, genre,
                  duration, publishTime, popularity, albumName, sep=', ', file=csvFile)
    if isWriteToFile:
        csvFile.close()
    return processedSongs


def printPlaylists(playlists, csvFileName=None):
    print('--------------------')
    print('Playlists:')
    isWriteToFile = csvFileName != None
    if isWriteToFile:
        csvFile = open('files/' + csvFileName + '.csv', 'w')
        csvFile.write('playlistCount, playlistId, playlistName, creator, privacy, trackCount, ' +
                      'playCount, createTime, updateTime, trackUpdateTime, trackNumberUpdateTime\n')
    playlistCount = 0
    for playlist in playlists:
        playlistCount = playlistCount + 1
        playlistId = playlist['id']
        playlistName = playlist['name']
        userId = playlist['userId']
        creator = playlist['creator']['nickname']
        privacy = playlist['privacy']
        trackCount = playlist['trackCount']
        playCount = playlist['playCount']

        def convertTime(timeTs): return datetime.fromtimestamp(
            timeTs / 1000).strftime('%Y-%m-%d %H:%M:%S')
        createTime = convertTime(playlist['createTime'])
        updateTime = convertTime(playlist['updateTime'])
        trackUpdateTime = convertTime(playlist['trackUpdateTime'])
        trackNumberUpdateTime = convertTime(playlist['trackNumberUpdateTime'])
        print(playlistCount, playlistId, playlistName, creator, privacy, trackCount,
              playCount, createTime, updateTime, trackUpdateTime, trackNumberUpdateTime, sep=', ')
        if isWriteToFile:
            print(playlistCount, playlistId, playlistName, creator, privacy, trackCount, playCount,
                  createTime, updateTime, trackUpdateTime, trackNumberUpdateTime, sep=', ', file=csvFile)
    if isWriteToFile:
        csvFile.close()


def writeJsonToFile(jsonObject, fileName):
    # Write json to file
    with open('./files/' + fileName + '.json', 'w') as f:
        json.dump(jsonObject, f, ensure_ascii=False)


def loadJsonFromFile(fileName):
    # Load json from file
    with open('./files/' + fileName + '.json') as f:
        return json.load(f)


def sureCheck():
    msg = input('Are you sure? Press Y to continue: ')
    if msg != 'y' and msg != 'Y':
        sys.exit()
