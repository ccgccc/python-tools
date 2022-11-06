import json
import time
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from artists import artists, artistToCrawl
from spotifyFunc import *
from playlistRemoveItems import playlistRemoveAllItems
from crawlPlaylists import crawlSinglePlaylist

# **************************************************
#  Add tracks to spotify most played songs playlist
# **************************************************

# Define artist here
artist = artistToCrawl
# Define track number to add
tracksNumber = 20

# # Generate playlist
# # Define if playlist is private
# isPrivate = False
# # Define if update description
# isUpdateDesc = True
# # Define playlist id
# playlistID = None

# Specify playlist
# Define playlist id
playlistID = '2R48aLSO7QmOaHAGaV0zIM'  # Listening Artist
# Define if playlist is private
isPrivate = True
# Define if update description
isUpdateDesc = False


def main():
    # Read parameters from command line
    if len(sys.argv) >= 2:
        trackNumber = int(sys.argv[1])
    else:
        trackNumber = tracksNumber
    if trackNumber > 100:
        print('Track number too big.')
        sys.exit()

    # Get playlist
    if playlistID == None:
        with open('./files/playlists/generated_playlists/' + artist + '_playlist.json') as f:
            playlist = json.load(f)
        # print(playlist)
        playlistId = playlist['id']
        # print(playlistId)
    else:
        playlistId = playlistID
    # Get all tracks
    allTracks = []
    with open('./files/tracks/' + artist + '_alltracks.json') as f:
        allTracks = json.load(f)
    # print(allTracks)

    # Get accessToken
    accessToken = getAccessToken(clientID, clientSecret)
    # Get spotify authorization authorizeToken by scope
    if isPrivate:
        scope = [
            "playlist-read-private",
            "playlist-modify-private"
        ]
    else:
        scope = [
            "playlist-modify-public"
        ]
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)
    playlistRemoveAllItems(accessToken, spotify,
                           authorizeToken, playlistId, isPrivate=isPrivate)
    playlistAddTracksByNumber(
        spotify, authorizeToken, playlistId, artist, allTracks, trackNumber, isUpdateDesc=isUpdateDesc)
    # Get new playlist info
    if playlistID == None:
        crawlSinglePlaylist(accessToken, playlistId,
                            './files/playlists/generated_playlists_info/')
    else:
        crawlSinglePlaylist(accessToken, playlistId,
                            './files/playlists/', isPrivate=isPrivate, spotify=spotify)


def playlistAddTracksByNumber(spotify, token, playlistId, artist, allTracks, tracksNumber, isUpdateDesc=True):
    resJson = addTracksToPlaylistByNumber(
        spotify, token, playlistId, allTracks, tracksNumber)
    print('Response:', json.dumps(resJson, ensure_ascii=False))

    if isUpdateDesc:
        # Playlist name & description
        playlistName = artists[artist]['name'] + ' Most Played Songs'
        minimumPlaycount = allTracks[tracksNumber - 1]['playcount']
        if minimumPlaycount >= 10000000:
            minimumPlaycountStr = str(minimumPlaycount // 1000000) + ' million'
        elif minimumPlaycount >= 1000000:
            minimumPlaycountStr = str(
                minimumPlaycount // 100000 / 10) + ' million'
        else:
            minimumPlaycountStr = str(minimumPlaycount)
        playlistDescription = artists[artist]['name'] \
            + ' most played songs (top ' + str(tracksNumber) \
            + ', minimum playcount: ' + minimumPlaycountStr + '). ' + \
            'Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
        res = updatePlayList(spotify, token, playlistId,
                             playlistName, playlistDescription, True)
        print('Response:', res)


if __name__ == '__main__':
    main()
