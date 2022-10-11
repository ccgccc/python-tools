
import os
from common import *


# Define netease playlist name
playlistName = 'Favorite'
# playlistName = 'Like'
# playlistName = 'Nice'
# playlistName = 'To Listen'


# Get netease playlist
playlistFileName = 'playlists/custom_playlists/playlist_' + playlistName
if not os.path.isfile('./files/' + playlistFileName + '.json'):
    print('Playlist not created yet. Please set isCreate to True.')
    sys.exit()
playlist = loadJsonFromFile(playlistFileName)
printPlaylists([playlist['playlist']])

# Ger playlistSongs & playlistPrivileges
playlistSongs = playlist['playlist']['tracks']
playlistPrivileges = playlist['privileges']
# Get netease no copyright songs
# noCopyrightSongs = [song for song in playlistSongs if song['fee'] == 0 and
#                     playlist['privileges'][playlistSongs.index(song)]['st'] < 0]
# noCopyrightSongs = [song for song in playlistSongs if
#                     playlist['privileges'][playlistSongs.index(song)]['st'] < 0]
noCopyrightSongs = []
for i in range(len(playlistSongs)):
    if playlistPrivileges[i]['st'] < 0:
        noCopyrightSongs.append(playlistSongs[i])
printSongs(noCopyrightSongs)
