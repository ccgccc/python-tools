from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from spotifyFunc import *

# ******************************
#     Playlists difference
# ******************************


scope = [
    "user-library-read"
]
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
tracks = getUserAllLikedSongs(spotify, token)
trackItems = tracks['items']
trackIds = set(map(lambda track: track['track']['id'], trackItems))
# print(trackIds)


playlistIDs = [
    "7J6PrVFDlPWiQe0m6NF2ie",  # Favorite
    "2QBH6yCLDJhTiXKqDfCtOA"  # Like
]
trackItems2 = []
token2 = getAccessToken(clientID, clientSecret)
for playlistID in playlistIDs:
    playlist = getPlaylistAndAllTracks(token2, playlistID)
    trackItems2.extend(playlist['tracks']['items'])
trackIds2 = set(map(lambda track: track['track']['id'], trackItems2))
# print(trackIds2)


print('--------------------')
print('Only in Like:')
for track in trackItems:
    if track['track']['id'] not in trackIds2:
        print(track['track']['name'])
print('--------------------')
print('Only in Playlists:')
for track in trackItems2:
    if track['track']['id'] not in trackIds:
        print(track['track']['name'])
print('--------------------')
