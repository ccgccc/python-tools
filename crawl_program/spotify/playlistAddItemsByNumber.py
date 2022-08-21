import json
import time
from artists import *
from spotifyFunc import *

# **************************************************
#  Add tracks to spotify most played songs playlist
# **************************************************

# Define artist here
# artist = 'jacky_cheung'
# artist = 'bruno_mars'
artist = 'nobody'

# Define track number to add
tracksNumber = 20


# get playlist
playlist = []
with open('./files/' + artist + '_playlist.json') as f:
    playlist = json.load(f)
# print(playlist)
playlistId = playlist['id']
# print(playlistId)

# get all tracks
allTracks = []
with open('./files/' + artist + '_alltracks.json') as f:
    allTracks = json.load(f)
# print(allTracks)

# get spotify authorization token by scope
scope = "playlist-modify-public"
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)

resJson = addTracksToPlaylistByNumber(spotify, token, playlistId, allTracks, tracksNumber)
print('Response:')
print(json.dumps(resJson, ensure_ascii=False))

# playlist name & description
playlistName = artists[artist]['name'] + ' Most Played Songs'
playlistDescription = artists[artist]['name'] + ' most played songs (top ' + str(tracksNumber) + ').' + \
    ' Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
res = updatePlayList(spotify, token, playlistId,
                     playlistName, playlistDescription, True)
print('Response:')
print(res)
