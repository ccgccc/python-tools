from utils.secrets import clientID, clientSecret
from spotifyFunc import *

# ******************************
#     Playlist remove items
# ******************************

# Define playlist id here
playlistID = "0Ip5YtkmYoouZ0YjALg1QA"  # Beyond Most Played Songs


# API requests
token = getAccessToken(clientID, clientSecret)
playlist = getPlaylistAndAllTracks(token, playlistID)
trackItems = playlist['tracks']['items']

# Get spotify authorization token by scope
scope = "playlist-modify-public"
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
trackUriList = []
for track in trackItems:
    trackUriList.append(track['track']['uri'])
removePlayListTracks(spotify, token, playlistID, trackUriList)
