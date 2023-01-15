from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from spotifyFunc import *

# ******************************
#     Playlist remove items
# ******************************

# Define isPrivate & public playlist id here
# isPrivate = False
# playlistId = "0Ip5YtkmYoouZ0YjALg1QA"  # Beyond Most Played Songs

# Define isPrivate & private playlist id here
isPrivate = True
playlistId = '1cd55XqNdveVHn8DUJRJM1'  # To Listen

# Define tracks to keep
tracksToKeep = {
    '5LlhtR0dYQcYUTapamXiKU',
    '4ofmSKnAYj295dE0klRGQx',
    '6sPRQXpV0lW2MTNjaD1uDG',
    '3AUdVAMQ7ZLi7TPLy18ZBT',
}


def main():
    # Get accessToken
    accessToken = getAccessToken(clientID, clientSecret)
    # Get spotify authorization token by scope
    if isPrivate:
        scope = [
            "playlist-read-private",
            "playlist-modify-private"
        ]
    else:
        scope = "playlist-modify-public"
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)
    playlistRemoveAllItems(accessToken, spotify, authorizeToken,
                           playlistId, tracksToKeep=tracksToKeep, isPrivate=isPrivate)


def playlistRemoveAllItems(accessToken, spotify, authorizeToken, playlistId,
                           tracksToKeep=None, isPrivate=False):
    playlist = getPlaylistAndAllTracks(
        accessToken, playlistId, isPrivate=isPrivate, spotify=spotify)
    trackItems = playlist['tracks']['items']

    trackUriList = []
    for track in trackItems:
        trackUri = track['track']['uri']
        if tracksToKeep != None and trackUri.split(':')[-1] in tracksToKeep:
            continue
        trackUriList.append(trackUri)
    print('--------------------')
    print('To remove: ', len(trackUriList), '\n', trackUriList, sep='')
    if len(trackUriList) > 0:
        resJson = removePlayListTracks(
            spotify, authorizeToken, playlistId, trackUriList)


if __name__ == '__main__':
    main()
