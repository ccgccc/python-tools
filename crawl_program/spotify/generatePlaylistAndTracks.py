import os
import sys
import json
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from artists import artists, artistToCrawl
from spotifyFunc import *
from playlistAddItemsByNumber import playlistAddTracksByNumber
from playlistAddItemsByPlaycount import playlistAddTracksByPlaycount
from playlistRemoveItems import playlistRemoveAllItems
from crawlPlaylists import crawlSinglePlaylist

# **********************************************************************
#    Create or update spotify most played songs playlist & add tracks
# **********************************************************************

# Define artist here
artist = artistToCrawl

# Define create playlist or update playlist
isCreate = True

# Define generate method: 1 - by number, 2 - by playcount
generateMethod = 1
# generateMethod = 2
# For method 1: Define track number to add tracks
tracksNumber = 20
# For method 2: Define minimum playcount to add tracks
playcount = 5000000

# Define my user id here
myUserId = '31jvwpn5kplbtp4sqdqaol2x5mcy'  # ccg ccc


# Prepare check
if artists.get(artist) == None:
    print(artist + ' is not defined in artist.py, please define it first.')
    sys.exit()
generateDir = './files/playlists/generated_playlists/'
if isCreate and os.path.isfile(generateDir + artist + '_playlist.json'):
    print('Alreay created playlist. Exit...')
    sys.exit()
if generateMethod != 1 and generateMethod != 2:
    print('generate method not supported.')
    sys.exit()

# Get accessToken
accessToken = getAccessToken(clientID, clientSecret)
# Get spotify authorization authorizeToken by scope
scope = "playlist-modify-public"
spotify, authorizeToken = getAuthorizationToken(clientID, clientSecret, scope)
if isCreate:
    # Playlist name
    playlistName = artists[artist]['name'] + ' Most Played Songs'
    # Create playlist
    playlist = createPlayList(spotify, authorizeToken, userId=myUserId, name=playlistName,
                              description='playlist description', ispublic=True)
    playlistId = playlist['id']

    # Write json to file
    with open(generateDir + artist + '_playlist.json', 'w') as f:
        print('Response:')
        print(json.dumps(playlist, ensure_ascii=False))
        json.dump(playlist, f, ensure_ascii=False)
else:
    with open(generateDir + artist + '_playlist.json') as f:
        playlist = json.load(f)
    playlistId = playlist['id']
    playlistRemoveAllItems(accessToken, spotify, authorizeToken, playlistId)

# Get all tracks
allTracks = []
with open('./files/tracks/' + artist + '_alltracks.json') as f:
    allTracks = json.load(f)
# print(allTracks)
# Add tracks
if generateMethod == 1:
    playlistAddTracksByNumber(
        spotify, authorizeToken, playlistId, artist, allTracks, tracksNumber)
elif generateMethod == 2:
    playlistAddTracksByPlaycount(
        spotify, authorizeToken, playlistId, artist, allTracks, playcount)

# Get new playlist info
crawlSinglePlaylist(accessToken, playlistId,
                    './files/playlists/generated_playlists_info/')
