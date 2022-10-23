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
# artist = 'nobody'
artist = artistToCrawl

# Define minimum playcount to add tracks
playcount = 5000000

# # Generate playlist
# # Define if playlist is private
# isPrivate = False
# # Define if update description
# isUpdateDesc = True
# # Define playlist id
# playlistID = None

# Specify playlist
# Define if playlist is private
isPrivate = True
# Define if update description
isUpdateDesc = False
# Define playlist id
playlistID = '2R48aLSO7QmOaHAGaV0zIM'  # Listening Artist


def main():
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
        scope = "playlist-modify-public"
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)
    playlistRemoveAllItems(accessToken, spotify,
                           authorizeToken, playlistId, isPrivate=isPrivate)
    playlistAddTracksByPlaycount(
        spotify, authorizeToken, playlistId, artist, allTracks, playcount, isUpdateDesc=isUpdateDesc)
    # Get new playlist info
    if playlistID != None:
        crawlSinglePlaylist(accessToken, playlistId,
                            './files/playlists/', isPrivate=isPrivate, spotify=spotify)


def playlistAddTracksByPlaycount(spotify, token, playlistId, artist, allTracks, playcount, isUpdateDesc=True):
    resJson = addTracksToPlaylistByPlaycount(
        spotify, token, playlistId, allTracks, playcount)
    print('Response:', json.dumps(resJson, ensure_ascii=False))

    if isUpdateDesc:
        # Playlist name & description
        playlistName = artists[artist]['name'] + ' Most Played Songs'
        playlistDescription = artists[artist]['name'] + ' most played songs (playcount > ' + \
            (str(playcount // 1000000) + ' million' if playcount >= 1000000 else str(playcount)) + ').' + \
            ' Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
        res = updatePlayList(spotify, token, playlistId,
                             playlistName, playlistDescription, True)
        print('Response:', res)


if __name__ == '__main__':
    main()
