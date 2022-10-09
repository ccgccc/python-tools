import time
from common import *

playlistId = 553778357
# Liked songs playlist id
# playlistId = 553778357

# Use right cookie to retrive private playlists
headers['cookie'] = readFileContent('cookie.txt')

playlist = getPlaylist(playlistId)
playlistSongs = getPlaylistSongs(playlistId)

fileName = 'playlists/playlist_songs_' + \
    playlist['playlist']['name'] + '_by ' + \
    playlist['playlist']['creator']['nickname'] + \
    '_bak_' + time.strftime("%Y-%m-%d")
writeJsonToFile(playlistSongs, fileName)

printPlaylists([playlist['playlist']])
# printSongs(playlistSongs['songs'], fileName)
printSongs(reversed(playlistSongs['songs']), fileName)
