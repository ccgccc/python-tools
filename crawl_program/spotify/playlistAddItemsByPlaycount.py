import json
import time
from utils.secrets import clientID, clientSecret
from utils.auth import getAuthorizationToken
from artists import artists, artistToCrawl
from spotifyFunc import *

# **************************************************
#  Add tracks to spotify most played songs playlist
# **************************************************

# Define artist here
artist = 'nobody'
# artist = artistToCrawl

# Define minimum playcount to add tracks
playcount = 5000000


def main():
    # Get playlist
    playlist = []
    with open('./files/playlists/generated_playlists/' + artist + '_playlist.json') as f:
        playlist = json.load(f)
    # print(playlist)
    playlistId = playlist['id']
    # print(playlistId)
    # Get all tracks
    allTracks = []
    with open('./files/tracks/' + artist + '_alltracks.json') as f:
        allTracks = json.load(f)
    # print(allTracks)

    # Get spotify authorization token by scope
    scope = "playlist-modify-public"
    spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
    playlistAddTracksByPlaycount(
        spotify, token, playlistId, artist, allTracks, playcount)


def playlistAddTracksByPlaycount(spotify, token, playlistId, artist, allTracks, playcount):
    resJson = addTracksToPlaylistByPlaycount(
        spotify, token, playlistId, allTracks, playcount)
    print('Response:', json.dumps(resJson, ensure_ascii=False))

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
