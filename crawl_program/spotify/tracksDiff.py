from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from spotifyFunc import *

# ******************************
#  Like vs Playlists difference
# ******************************


# Get liked songs
scope = [
    "user-library-read"
]
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
tracks = getUserAllLikedSongs(spotify, token)
trackItems = tracks['items']
trackIds = set(map(lambda track: track['track']['id'], trackItems))
# print(trackIds)
print('--------------------')
print('\u2764\uFE0F:', len(trackItems))  # heart symbol

# Get playlist songs
playlists = {
    "Favorite": "7J6PrVFDlPWiQe0m6NF2ie",
    "Like": "2QBH6yCLDJhTiXKqDfCtOA",
    "Nice": '4SqLcwtjZJXdkH8twICyOa',
}
trackItems2 = []
token2 = getAccessToken(clientID, clientSecret)
print('--------------------')
totalTrack = 0
for playlistName, playlistId in playlists.items():
    playlist = getPlaylistAndAllTracks(token2, playlistId)
    curTrackItems = playlist['tracks']['items']
    trackItems2.extend(curTrackItems)
    totalTrack = totalTrack + len(curTrackItems)
    print(playlistName + ':', len(curTrackItems))
print('Total:', totalTrack)
trackIds2 = set(map(lambda track: track['track']['id'], trackItems2))
# print(trackIds2)


# Only in Like
print('\n--------------------')
# print('Only in Like:')
print('Only in \u2764\uFE0F:')  # heart symbol
for track in trackItems:
    if track['track']['id'] not in trackIds2:
        print(track['track']['name'])

# Only in Playlists
print('--------------------')
print('Only in Playlists:')
playlistOnlyTrackIds = []
for track in trackItems2:
    if track['track']['id'] not in trackIds:
        print(track['track']['name'])
        playlistOnlyTrackIds.append(track['track']['id'])
if len(playlistOnlyTrackIds) > 0:
    print('\nTrack ids:', len(playlistOnlyTrackIds))
    print(','.join(playlistOnlyTrackIds))
print('--------------------')
