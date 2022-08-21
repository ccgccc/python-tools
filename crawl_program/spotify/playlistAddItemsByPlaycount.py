import json
import time
from artists import *
from spotifyFunc import *

# **************************************************
#  Add tracks to spotify most played songs playlist
# **************************************************

# Define artist here
# artist = 'jay_chou'
# artist = 'eason_chan'
artist = 'nobody'

# Define track number to add
playcount = 5000000


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

resJson = addTracksToPlaylistByPlaycount(
    spotify, token, playlistId, allTracks, playcount)
print('Response:')
print(json.dumps(resJson, ensure_ascii=False))

# playlist name & description
playlistName = artists[artist]['name'] + ' Most Played Songs'
playlistDescription = artists[artist]['name'] + ' most played songs (playcount > ' + \
    (str(playcount // 1000000) + ' million' if playcount >= 1000000 else str(playcount)) + ').' + \
    ' Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
res = updatePlayList(spotify, token, playlistId,
                     playlistName, playlistDescription, True)
print('Response:')
print(res)
