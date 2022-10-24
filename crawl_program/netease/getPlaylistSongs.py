from common import *

# ****************************************
#    Get netease playlist songs by id
# ****************************************

# Defin palylist id
playlistIds = [
    7673625615,  # Favorite
    7673790351,  # Like
    7680312360,  # Nice
    7690539370  # Listening Artist
]

# # Liked songs playlist id
# playlistIds = [553778357]

# Defin cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


for playlistId in playlistIds:
    playlist = getPlaylist(playlistId)
    playlistSongs = getPlaylistSongs(playlistId)

    fileName = 'playlists/playlist_songs_' + \
        playlist['playlist']['name'] + '_by ' + \
        playlist['playlist']['creator']['nickname']
    # + '_bak_' + time.strftime("%Y-%m-%d")
    writeJsonToFile(playlistSongs, fileName)

    printPlaylists([playlist['playlist']])
    # printSongs(playlistSongs['songs'], fileName)
    printSongs(reversed(playlistSongs['songs']), fileName)
