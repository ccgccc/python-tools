import json
import time
import sys
from utils.secrets import clientID, clientSecret
from artists import artists, artistToCrawl
from spotifyFunc import *

# **************************************************
#     Create spotify most played songs playlist
# **************************************************

# Define artist here
# artist = 'jacky_cheung'
# artist = 'jay_chou'
# artist = 'eason_chan'
# artist = 'bruno_mars'
artist = 'nobody'
# artist = artistToCrawl

# Define my user id here
myUserId = '31jvwpn5kplbtp4sqdqaol2x5mcy'  # ccg ccc


if artists.get(artist) == None:
    print(artist + ' is not defined in artist.py, please define it first.')
    sys.exit()
# playlist name & description
playlistName = artists[artist]['name'] + ' Most Played Songs'
playlistDescription = artists[artist]['name'] + ' most played songs.' + \
    ' Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
# get spotify authorization token by scope
scope = "playlist-modify-public"
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
playlist = createPlayList(spotify, token, userId=myUserId, name=playlistName,
                          description=playlistDescription, ispublic=True)

# Write json to file
with open('./files/playlists/' + artist + '_playlist.json', 'w') as f:
    print('Response:')
    print(json.dumps(playlist, ensure_ascii=False))
    json.dump(playlist, f, ensure_ascii=False)
