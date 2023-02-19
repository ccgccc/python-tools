import os
from artists import *
from common import *

# **************************************************
#     Delete netease most played songs playlist
# **************************************************

# Set baseUrl
setBaseUrl()


# Sure check
sureCheck()
# Check playlsit exist
directory = 'playlists/generated_playlists/'
if not os.path.isfile('./files/' + directory + artistToCrawl + '_playlist.json'):
    print('Playlist doesn\'t exitst. Exit...')
    sys.exit()

# Get playlistId
playlist = loadJsonFromFile(directory + artistToCrawl + '_playlist')
playlistId = playlist['playlist']['id']

# Delete playlist
deletePlaylist(playlistId)

# Remove playlist file
os.remove('./files/' + directory + artistToCrawl + '_playlist.json')
