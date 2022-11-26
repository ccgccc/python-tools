import os
import sys
import json
import time
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from artists import *
from spotifyFunc import *
from playlistAddItemsByNumber import playlistAddTracksByNumber
from playlistAddItemsByPlaycount import playlistAddTracksByPlaycount
from playlistRemoveItems import playlistRemoveAllItems
from crawlPlaylists import crawlSinglePlaylist

# **********************************************************************
#    Create or update spotify most played songs playlist & add tracks
# **********************************************************************

# Define artist here
artistToGenerateList = [artistToCrawl]

# Define create playlist or update playlist
isCreate = True
# Read parameters from command line
if len(sys.argv) >= 2 and sys.argv[1] == 'update':
    isCreate = False
    if len(sys.argv) >= 3:
        if sys.argv[2] == 'all':
            artistToGenerateList = list(generateArtists.keys())
        else:
            artistToGenerateList = [sys.argv[2]]

# Define if print playlists
printPlaylist = False

# Define my user id here
myUserId = '31jvwpn5kplbtp4sqdqaol2x5mcy'  # ccg ccc


def main():
    # Get accessToken
    accessToken = getAccessToken(clientID, clientSecret)
    # Get spotify authorization authorizeToken by scope
    scope = "playlist-modify-public"
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)

    for artist in artistToGenerateList:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Updating ' + artists[artist]['name'] + '...')
        generatePlaylistAndTracks(artist, accessToken, spotify, authorizeToken)


def generatePlaylistAndTracks(artist, accessToken, spotify, authorizeToken):
    generateInfo = artists[artist].get('generateInfo')
    if generateInfo != None:
        generateMethod = generateInfo['generateMethod']
        if generateMethod == 1:
            tracksNumber = generateInfo['number']
        else:
            playcount = generateInfo['number']
    else:
        print('Can\'t find generate info in artists.py.')
        sys.exit()

    # Prepare check
    print('--------------------')
    print('*** Generate Info ***')
    print('Artist:', artists[artist]['name'])
    print('IsCreate:', isCreate)
    print('Generate Method:', generateMethod)
    if generateMethod == 1:
        print('Tracks Number:', tracksNumber)
        if tracksNumber > 100:
            print('Generate Method 1: Track number too big.')
            sys.exit()
    elif generateMethod == 2:
        print('Playcount:', playcount)
        if playcount < 100000:
            print('Generate Method 2: Playcount too small.')
            sys.exit()
    else:
        print('Generate method not supported.')
        sys.exit()
    print('--------------------')

    if artists.get(artist) == None:
        print(artist + ' is not defined in artist.py, please define it first.')
        sys.exit()
    generateDir = './files/playlists/generated_playlists/'
    if isCreate and os.path.isfile(generateDir + artist + '_playlist.json'):
        print('Alreay created playlist. Exit...')
        sys.exit()

    if isCreate:
        # Playlist name
        playlistName = artists[artist]['name'] + ' Most Played Songs'
        # Create playlist
        playlistDescription = artists[artist]['name'] + ' most played songs.' + \
            ' Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
        playlist = createPlayList(spotify, authorizeToken, userId=myUserId, name=playlistName,
                                  description=playlistDescription, ispublic=True)
        playlistId = playlist['id']

        # Write json to file
        with open(generateDir + artist + '_playlist.json', 'w') as f:
            print('Response:')
            print(json.dumps(playlist, ensure_ascii=False))
            json.dump(playlist, f, ensure_ascii=False)
        # To identify creating playlist after
        playlist = None
    else:
        with open(generateDir + artist + '_playlist.json') as f:
            playlist = json.load(f)
        playlistId = playlist['id']
        playlistRemoveAllItems(accessToken, spotify,
                               authorizeToken, playlistId)

    # Get all tracks
    allTracks = []
    with open('./files/tracks/' + artist + '_alltracks.json') as f:
        allTracks = json.load(f)
    # print(allTracks)
    # Add tracks
    if generateMethod == 1:
        playlistAddTracksByNumber(
            spotify, authorizeToken, playlistId, playlist, artist, allTracks, tracksNumber)
    elif generateMethod == 2:
        playlistAddTracksByPlaycount(
            spotify, authorizeToken, playlistId, playlist, artist, allTracks, playcount)

    # Get new playlist info
    crawlSinglePlaylist(accessToken, playlistId, './files/playlists/generated_playlists_info/',
                        printPlaylist=printPlaylist, simplePrint=True)


if __name__ == '__main__':
    main()
