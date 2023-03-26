
import os
import sys
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from common import *
from netease.syncSongs import *

# **************************************************
#    Get netease no copyright songs in playlists
# **************************************************

# Define netease playlist name
playlistNames = [
    'Favorite',
    'Like',
    'Nice',
]
# playlistName = 'Like'
# playlistName = 'Nice'
# playlistName = 'To Listen'


# Get netease playlist
playlists = []
for playlistName in playlistNames:
    playlistFileName = 'playlists/playlist_songs_' + \
        playlistName + '_by ' + myUserName
    if not os.path.isfile('./files/' + playlistFileName + '.json'):
        print('Playlist not created yet. Please set isCreate to True.')
        sys.exit()
    playlist = loadJsonFromFile(playlistFileName)
    newPlaylist = playlist['playlist']['playlist']
    newPlaylist['songs'] = list(reversed(playlist['songs']))
    newPlaylist['privileges'] = list(reversed(playlist['privileges']))
    # playlist['playlist']['privileges'] = playlist['privileges']
    playlists.append(newPlaylist)
printPlaylists(playlists)

# Ger playlistSongs & playlistPrivileges
print('--------------------')
mergedPlaylist = playlists[0]
for i in range(1, len(playlists)):
    # print(i, len(playlists[i]['songs']))
    mergedPlaylist['songs'].extend(playlists[i]['songs'])
    mergedPlaylist['privileges'].extend(playlists[i]['privileges'])
print('Total Songs:', len(mergedPlaylist['songs']), '\n')
# playlistSongs = mergedPlaylist['tracks']
# playlistPrivileges = mergedPlaylist['privileges']
# Get netease no copyright songs
# noCopyrightSongs = [song for song in playlistSongs if song['fee'] == 0 and
#                     playlist['privileges'][playlistSongs.index(song)]['st'] < 0]
# noCopyrightSongs = [song for song in playlistSongs if
#                     playlist['privileges'][playlistSongs.index(song)]['st'] < 0]
# noCopyrightSongs = []
# for i in range(len(playlistSongs)):
#     if playlistPrivileges[i]['st'] < 0:
#         noCopyrightSongs.append(playlistSongs[i])
# printSongs(noCopyrightSongs)

neteaseNoCopyrightSongs, neteaseNeedPurchaseSongs = getNeteaseNoCopyrightSongs(
    mergedPlaylist)
allNonPlayableSongs = []
allNonPlayableSongs.extend(neteaseNoCopyrightSongs)
allNonPlayableSongs.extend(neteaseNeedPurchaseSongs)
print('Non-playable Songs:', len(allNonPlayableSongs))
print('No copyright Songs:', len(neteaseNoCopyrightSongs))
print('Need purchase Songs:', len(neteaseNeedPurchaseSongs), '\n')

artistIds = list(reversed([artistInfo['artistId']
                 for artistKey, artistInfo in artists.items()]))
allNonPlayableSongs.sort(key=lambda song: (artistIds.index(
    [ar['id'] for ar in song['ar'] if ar['id'] in artistIds][0]),
    # song['al']['id']))
    song['publishTime']))
printSongs(allNonPlayableSongs, reverse=False)
