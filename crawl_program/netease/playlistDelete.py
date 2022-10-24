import os
from os import listdir
from os.path import isfile, join
from artists import *
from common import *

# **************************************************
#     Delete netease most played songs playlist
# **************************************************

# Defin cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


# Sure check
sureCheck()
# Check playlsit exist
if not isfile('./files/playlists/generated_playlists/' + artistToCrawl + '_playlist.json'):
    print('Playlist doesn\'t exitst. Exit...')
    sys.exit()

# Get playlistId
playlist = loadJsonFromFile(
    'playlists/generated_playlists/' + artistToCrawl + '_playlist')
playlistId = playlist['playlist']['id']

# Delete playlist
deletePlaylist(playlistId)

# Remove playlist file
os.remove(dir + artistToCrawl + '_playlist.json')
