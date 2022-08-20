import json
import time
from utils.auth import *
from utils.secrets import clientID, clientSecret
from artists import *
from spotifyFunc import *

# **************************************************
#     Create spotify most played songs playlist
# **************************************************

# Define artist here
# artist = 'jacky_cheung'
# artist = 'jay_chou'
# artist = 'eason_chan'
# artist = 'bruno_mars'
artist = 'Nobody'

# Define my user id here
myUserId = '31jvwpn5kplbtp4sqdqaol2x5mcy'  # ccg ccc


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
with open('./files/' + artist + '_playlist.json', 'w') as f:
    print('Response:')
    print(json.dumps(playlist, ensure_ascii=False))
    json.dump(playlist, f, ensure_ascii=False)
