import re
import json
import time
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from artists import *
from spotifyFunc import *
from playlistRemoveItems import playlistRemoveAllItems
from crawlPlaylists import crawlSinglePlaylist

# **************************************************
#  Add tracks to spotify most played songs playlist
# **************************************************

# Define artist here
artistToCrawlList = [artistToCrawl]
# artistToCrawlList = list(generateArtists.keys())

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
        if len(artistToCrawlList) > 1:
            print('Can\'t specify tracknumber for multi artists.')
            sys.exit()
        trackNumber = int(sys.argv[1])

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

    for artist in artistToCrawlList:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Updating ' + artists[artist]['name'] + '...')
        generateInfo = artists[artist].get('generateInfo')
        if generateInfo != None:
            generateMethod = generateInfo['generateMethod']
            trackNumber = generateInfo['number']
            if generateMethod != 1:
                print('GenerateMethod != 1, continue\n')
                continue
        elif len(artistToCrawlList) > 1:
            print('Can\'t find generate info in artists.py.')
            sys.exit()
        playlistAddItemsByNumber(
            artist, trackNumber, accessToken, spotify, authorizeToken)


def playlistAddItemsByNumber(artist, trackNumber, accessToken, spotify, authorizeToken):
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
        playlist = None
    # Get all tracks
    allTracks = []
    with open('./files/tracks/' + artist + '_alltracks.json') as f:
        allTracks = json.load(f)
    # print(allTracks)

    playlistRemoveAllItems(accessToken, spotify,
                           authorizeToken, playlistId, isPrivate=isPrivate)
    playlistAddTracksByNumber(spotify, authorizeToken, playlistId, playlist,
                              artist, allTracks, trackNumber, isUpdateDesc=isUpdateDesc)
    # Get new playlist info
    if playlistID == None:
        crawlSinglePlaylist(accessToken, playlistId,
                            './files/playlists/generated_playlists_info/', isPrivate=isPrivate)
    else:
        crawlSinglePlaylist(accessToken, playlistId,
                            './files/playlists/', isPrivate=isPrivate, spotify=spotify)


def playlistAddTracksByNumber(spotify, token, playlistId, playlist, artist, allTracks, trackNumber, isUpdateDesc=True):
    resJson = addTracksToPlaylistByNumber(
        spotify, token, playlistId, allTracks, trackNumber)
    print('Response:', json.dumps(resJson, ensure_ascii=False))

    if isUpdateDesc:
        # Playlist name & description
        playlistName = artists[artist]['name'] + ' Most Played Songs'
        maximumPlaycountStr = getPlaycountStr(
            allTracks[0]['playcount'])
        minimumPlaycountStr = getPlaycountStr(
            allTracks[trackNumber - 1]['playcount'])
        if playlist == None:  # Create playlist
            playlistDescription = artists[artist]['name'] \
                + ' most played songs (top ' + str(trackNumber) \
                + ', minimum playcount: ' + minimumPlaycountStr + '). ' + \
                'Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
        else:  # Update playlist
            oldDescription = playlist['description']
            playlistDescription = artists[artist]['name'] \
                + ' most played songs (top ' + str(trackNumber) \
                + ', maxPlay: ' + maximumPlaycountStr + ', minPlay: ' + minimumPlaycountStr + '). ' + \
                'Generated on ' + re.match(r'.*Generated on (.*)by ccg.*', oldDescription).group(1) + ' by ccg. ' + \
                'Updated on ' + time.strftime("%Y-%m-%d") + '.'
        res = updatePlayList(spotify, token, playlistId,
                             playlistName, playlistDescription, True)
        print('Response:', res)


if __name__ == '__main__':
    main()
