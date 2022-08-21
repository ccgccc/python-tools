import json
import time
import sys
from utils.auth import *
from utils.secrets import clientID, clientSecret
from artists import *
from spotifyFunc import *

# ************************************************************
#    Create spotify most played songs playlist & add tracks
# ************************************************************

# Define artist here
# artist = 'jacky_cheung'
# artist = 'jay_chou'
# artist = 'eason_chan'
# artist = 'bruno_mars'
# artist = 'g_e_m'
artist = 'jj_lin'
# artist = 'nobody'

# Define create method: 1 - by number, 2 - by playcount
# createMethod = 1
createMethod = 2
# For method 1: Define track number to add tracks
tracksNumber = 30
# For method 2: Define minimum playcount to add tracks
playcount = 6000000

# Define my user id here
myUserId = '31jvwpn5kplbtp4sqdqaol2x5mcy'  # ccg ccc


if artists.get(artist) == None:
    print(artist + ' is not defined in artist.py, please define it first.')
    sys.exit()
if createMethod != 1 and createMethod != 2:
    print('create method not supported.')
    sys.exit()

# get spotify authorization token by scope
scope = "playlist-modify-public"
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)

# playlist name & description
playlistName = artists[artist]['name'] + ' Most Played Songs'
if createMethod == 1:
    playlistDescription = artists[artist]['name'] + ' most played songs (top ' + str(tracksNumber) + ').' + \
        ' Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
elif createMethod == 2:
    playlistDescription = artists[artist]['name'] + ' most played songs (playcount > ' + \
        (str(playcount // 1000000) + ' million' if playcount >= 1000000 else str(playcount)) + ').' + \
        ' Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
# create playlist
playlist = createPlayList(spotify, token, userId=myUserId, name=playlistName,
                          description=playlistDescription, ispublic=True)
playlistId = playlist['id']

# Write json to file
with open('./files/' + artist + '_playlist.json', 'w') as f:
    print('Response:')
    print(json.dumps(playlist, ensure_ascii=False))
    json.dump(playlist, f, ensure_ascii=False)


# get all tracks
allTracks = []
with open('./files/' + artist + '_alltracks.json') as f:
    allTracks = json.load(f)
# print(allTracks)

# add tracks
if createMethod == 1:
    resJson = addTracksToPlaylistByNumber(
        spotify, token, playlistId, allTracks, tracksNumber)
    print('Response:')
    print(json.dumps(resJson, ensure_ascii=False))
elif createMethod == 2:
    resJson = addTracksToPlaylistByPlaycount(
        spotify, token, playlistId, allTracks, playcount)
    print('Response:')
    print(json.dumps(resJson, ensure_ascii=False))
