import re
import sys
import json
import requests
from datetime import datetime


myUserId = 389958855

baseUrl = 'https://netease-cloud-music-api-three-rose.vercel.app'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}


def getAlbum(id):
    url = baseUrl + '/album'
    params = {
        'id': id
    }
    album = requests.get(url, headers=headers, params=params).json()
    # print(json.dumps(album, ensure_ascii=False))
    return album


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


def printAlbums(albums):
    print('--------------------')
    print('Albums:')
    albumCount = 0
    for album in albums:
        albumCount = albumCount + 1
        albumId = album['id']
        albumName = album['name']
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


def printSongs(songs, csvFileName=None):
    print('----------')
    print('Songs:')
    isWriteToFile = csvFileName != None
    if isWriteToFile:
        csvFile = open(csvFileName, 'w')
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
        csvFile = open(csvFileName, 'w')
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