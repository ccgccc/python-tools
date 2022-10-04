from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from spotifyFunc import *

# ******************************
#     Playlist remove items
# ******************************

# Define playlist id here
playlistId = "0Ip5YtkmYoouZ0YjALg1QA"  # Beyond Most Played Songs


def main():
    # Get accessToken
    accessToken = getAccessToken(clientID, clientSecret)
    # Get spotify authorization token by scope
    scope = "playlist-modify-public"
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)
    playlistRemoveAllItems(accessToken, spotify, authorizeToken, playlistId)


def playlistRemoveAllItems(accessToken, spotify, authorizeToken, playlistId):
    playlist = getPlaylistAndAllTracks(accessToken, playlistId)
    trackItems = playlist['tracks']['items']

    trackUriList = []
    for track in trackItems:
        trackUriList.append(track['track']['uri'])
    resJson = removePlayListTracks(
        spotify, authorizeToken, playlistId, trackUriList)
    print('Response:', resJson)


if __name__ == '__main__':
    main()
