import os
import sys
import json
from utils.secrets import clientID, clientSecret
from utils.auth import getAuthorizationToken
from artists import *
from spotifyFunc import *

# Read parameters from command line
if len(sys.argv) >= 2:
    artist = sys.argv[1]
else:
    print('Missing artist parameter. Exit...')
    sys.exit()


# Check artist exist
if artists.get(artist) == None:
    print('Artist \'' + artist + '\' not defined yet. Exit...')
    sys.exit()
# Check playlist exist
playlistFileName = './files/playlists/generated_playlists/' + \
    artist + '_playlist.json'
if not os.path.isfile(playlistFileName):
    print('Playlist doesn\'t exitst. Exit...')
    sys.exit()

# Load json from file
with open(playlistFileName) as f:
    playlist = json.load(f)
playlistId = playlist['id']

# Delete playlist
scope = [
    "playlist-modify-private",
    "playlist-modify-public"
]
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
seccess = unfollowPlayList(spotify, token, playlistId)

# Remove playlist file
if seccess:
    os.remove(playlistFileName)
    generatedPlaylistFile = './files/playlists/generated_playlists_info/playlist_' + \
        artists[artist]['name'] + ' Most Played Songs_by ccg ccc'
    os.remove(generatedPlaylistFile + '.json')
    os.remove(generatedPlaylistFile + '.csv')
