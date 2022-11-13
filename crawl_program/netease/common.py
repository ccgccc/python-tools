import re
import sys
import json
import requests
from datetime import datetime


myUserId = 389958855

baseUrl = 'https://netease-cloud-music-api-three-rose.vercel.app'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


def getAlbum(id):
    url = baseUrl + '/album'
    params = {
        'id': id
    }
    album = requests.get(url, headers=headers, params=params).json()
    # print(json.dumps(album, ensure_ascii=False))
    return album


def getArtistAlbums(artistId):
    url = baseUrl + '/artist/album'
    limit = 100
    params = {
        'id': artistId,
        'limit': limit,
        'offset': 0
    }
    resJson = requests.get(url, headers=headers, params=params).json()
    allAlbums = resJson['hotAlbums']
    # while allAlbums['more'] == True: # seems not working
    while len(resJson['hotAlbums']) == limit:
        params['offset'] = params['offset'] + limit
        print(params)
        resJson = requests.get(url, headers=headers, params=params).json()
        allAlbums.extend(resJson['hotAlbums'])
    return allAlbums


def getPlaylist(playlistId):
    url = baseUrl + '/playlist/detail'
    params = {
        'id': playlistId
    }
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 401:
        print('请求失败！返回信息：' + res.text)
        sys.exit()
    playlist = res.json()
    # print(json.dumps(playlist, ensure_ascii=False))
    return playlist


def getPlaylistSongs(playlistId):
    url = baseUrl + '/playlist/track/all'
    limit = 500
    params = {
        'id': playlistId,
        'limit': limit,
        'offset': 0
    }
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 401:
        print('请求失败！返回信息：' + res.text)
        sys.exit()
    resJson = res.json()
    playlistSongs = resJson
    # print(json.dumps(resJson, ensure_ascii=False))
    while len(resJson['songs']) == limit:
        params['offset'] = params['offset'] + limit
        print(params)
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
        print('**********\n')
        print(resJson)
        return resJson
    else:
        print('\n**********')
        print('Updating playlist description failed.')
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


def addSongsToPlayList(playlistId, tracks):
    res = addOrDeleteSongsToPlayList('add', playlistId, tracks)
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


def deleteSongsToPlayList(playlistId, tracks):
    res = addOrDeleteSongsToPlayList('del', playlistId, tracks)
    resJson = res.json()
    if res.status_code == 200 and resJson['body']['code'] == 200:
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


def addOrDeleteSongsToPlayList(opeartion, playlistId, tracks):
    url = baseUrl + '/playlist/tracks'
    params = {
        'op': opeartion,
        'pid': playlistId,
        'tracks': tracks
    }
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
    return requests.get(url, headers=headers, params=params).json()


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


def printSongs(songs, csvFileName=None, isWriteToConsole=True):
    isWriteToFile = csvFileName != None
    if isWriteToConsole:
        print('----------')
        print('Songs:')
    if isWriteToFile:
        csvFile = open('files/' + csvFileName + '.csv', 'w')
        csvFile.write('songCount, songId, songName, songArtists, ' +
                      'genre, duration, publishTime, popularity, albumName\n')
    songCount = 0
    for song in songs:
        songCount = songCount + 1
        songId = song['id']
        songName = re.sub(r'\,', '，', song['name'])
        songAlias = song['alia']
        songArtists = '_'.join(
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
        if isWriteToConsole:
            print(songCount, songId, songName, songArtists, genre,
                  duration, publishTime, popularity, albumName, sep=', ')
        if isWriteToFile:
            print(songCount, songId, songName, songArtists, genre,
                  duration, publishTime, popularity, albumName, sep=', ', file=csvFile)
    if isWriteToFile:
        csvFile.close()


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


def readFileContent(fileName):
    with open(fileName) as f:
        return f.read()


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
