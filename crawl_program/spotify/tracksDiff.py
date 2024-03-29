from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from spotifyFunc import *

# ******************************
#  Like vs Playlists difference
# ******************************


# Get liked songs
scope = [
    "user-library-read",
    "user-library-modify"
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
seen = set()
dupes = [x['track']['name'] for x in trackItems2
         if x['track']['id'] in seen or seen.add(x['track']['id'])]
print('Dupes:', dupes)
print('Total:', totalTrack)
trackIds2 = set(map(lambda track: track['track']['id'], trackItems2))
# print(trackIds2)


# Only in Like
print('\n--------------------')
# print('Only in Like:')
print('Only in \u2764\uFE0F:')  # heart symbol
likeOnlyTrackIds = []
for track in trackItems:
    trackId = track['track']['id']
    if trackId not in trackIds2:
        likeOnlyTrackIds.append(trackId)
        print(track['track']['name'])
if len(likeOnlyTrackIds) > 0:
    print('\nTrack ids:', len(likeOnlyTrackIds))
    print(likeOnlyTrackIds)

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
sureCheck()
# API requests
if len(likeOnlyTrackIds) > 0:
    print('Unsaving tracks...')
    unSaveUserTracks(spotify, token, ','.join(likeOnlyTrackIds))
if len(playlistOnlyTrackIds) > 0:
    print('Saving tracks...')
    saveUserTracks(spotify, token, ','.join(playlistOnlyTrackIds))
print('Done!')
