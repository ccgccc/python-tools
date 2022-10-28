from utils.secrets import clientID, clientSecret
from utils.auth import getAuthorizationToken
from spotifyFunc import *

# ******************************
#   Save spotify liked tracks
# ******************************

# Define track ids, comma separated
trackIds = readFileContent('saveTracks.txt')


scope = [
    "user-library-modify"
]
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
# API requests
res = saveUserTracks(spotify, token, trackIds)
print(res)
