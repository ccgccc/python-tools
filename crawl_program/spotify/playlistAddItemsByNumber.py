import json
import time
from utils.secrets import clientID, clientSecret
from artists import artists, artistToCrawl
from spotifyFunc import *

# **************************************************
#  Add tracks to spotify most played songs playlist
# **************************************************

# Define artist here
artist = 'nobody'
# artist = artistToCrawl

# Define track number to add
tracksNumber = 25


# Get playlist
playlist = []
with open('./files/playlists/' + artist + '_playlist.json') as f:
    playlist = json.load(f)
# print(playlist)
playlistId = playlist['id']
# print(playlistId)

# Get all tracks
allTracks = []
with open('./files/tracks/' + artist + '_alltracks.json') as f:
    allTracks = json.load(f)
# print(allTracks)

# Get spotify authorization token by scope
scope = "playlist-modify-public"
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
resJson = addTracksToPlaylistByNumber(
    spotify, token, playlistId, allTracks, tracksNumber)
print('Response:')
print(json.dumps(resJson, ensure_ascii=False))

# Playlist name & description
playlistName = artists[artist]['name'] + ' Most Played Songs'
playlistDescription = artists[artist]['name'] + ' most played songs (top ' + str(tracksNumber) + ').' + \
    ' Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
res = updatePlayList(spotify, token, playlistId,
                     playlistName, playlistDescription, True)
print('Response:')
print(res)
