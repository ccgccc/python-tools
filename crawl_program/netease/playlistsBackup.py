import os
import time
from common import *

# ****************************************
#   Backup netease user's all playlists
# ****************************************
# Note: doesn't contain mv


playlistName = 'playlists/all_my_playlists'
playlists = loadJsonFromFile(playlistName)
playlists = list(filter(
    lambda playlist: playlist['userId'] == myUserId, playlists['playlist']))

backupDir = 'playlists/playlists_backup_' + time.strftime("%Y-%m-%d")
if os.path.isdir('files/' + backupDir) != True:
    os.mkdir('files/' + backupDir)

playlistCount = 0
# for playlist in playlists[0:5]:
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
    print('--------------------')
    print('Playlist:')
    print(playlistCount, playlistId, playlistName, creator, privacy, trackCount,
          playCount, createTime, updateTime, trackUpdateTime, trackNumberUpdateTime, sep=', ')

    playlistSongs = getPlaylistSongs(playlistId)
    fileName = backupDir + '/' + \
        '{:03d}'.format(playlistCount) + '_' + playlistName + \
        '_by ' + creator + '_' + str(playlistId)
    writeJsonToFile(playlistSongs, fileName)
    printSongs(playlistSongs['songs'], fileName)
