import os
from common import *

# ****************************************
#    Get netease playlist songs by id
# ****************************************

# Defin palylist id
playlistIds = [
    # 553778357,  # 我喜欢的音乐
    7673625615,  # Favorite
    7673790351,  # Like
    7680312360,  # Nice
    # 7722735074,  # Hmm
    # 7741781941,  # One Hit
    # 7759490556,  # More Hits - 民谣
    # 7759804520,  # More Hits - 流行
    # 7690539370,  # Listening Artist
    # 7674298063,  # To Listen
]
# # Liked songs playlist id
# playlistIds = [553778357]

# Read parameters from command line
os.chdir(os.path.dirname(__file__))
if len(sys.argv) >= 2:
    playlistNames = sys.argv[1:]
    playlistIds = []
    for playlistName in playlistNames:
        with open('./files/playlists/playlist_songs_' + playlistName + '_by ccgccc.json') as f:
            playlist = json.load(f)
            playlistIds.append(playlist['playlist']['playlist']['id'])

# Define cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


for playlistId in playlistIds:
    playlist = getPlaylist(playlistId)
    playlistSongs = getPlaylistSongs(playlistId)
    playlistSongs['playlist'] = playlist

    fileName = 'playlists/playlist_songs_' + \
        playlist['playlist']['name'] + '_by ' + \
        playlist['playlist']['creator']['nickname']
    # + '_bak_' + time.strftime("%Y-%m-%d")
    writeJsonToFile(playlistSongs, fileName)

    printPlaylists([playlist['playlist']])
    # printSongs(playlistSongs['songs'], fileName)
    printSongs(reversed(playlistSongs['songs']), fileName)
