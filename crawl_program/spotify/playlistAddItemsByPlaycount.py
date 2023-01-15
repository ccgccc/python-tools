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
# Define if playlist is private
isPrivate = True
# Define if update description
isUpdateDesc = False
# Define playlist id
playlistID = '2R48aLSO7QmOaHAGaV0zIM'  # Listening Artist


def main():
    # Read parameters from command line
    if len(sys.argv) >= 2:
        if len(artistToCrawlList) > 1:
            print('Can\'t specify tracknumber for multi artists.')
            sys.exit()
        playCount = int(sys.argv[1].replace(',', ''))

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

    for artist in artistToCrawlList:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Updating ' + artists[artist]['name'] + '...')
        generateInfo = artists[artist].get('generateInfo')
        if generateInfo != None:
            generateMethod = generateInfo['generateMethod']
            playCount = generateInfo['number']
            if generateMethod != 2:
                print('GenerateMethod != 2, continue\n')
                continue
        elif len(artistToCrawlList) > 1:
            print('Can\'t find generate info in artists.py.')
            sys.exit()
        playlistAddItemsByPlaycount(
            artist, playCount, accessToken, spotify, authorizeToken)


def playlistAddItemsByPlaycount(
        artist, playCount, accessToken, spotify, authorizeToken):
    if playCount < 100000:
        print('Playcount too small.')
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
    playlistAddTracksByPlaycount(spotify, authorizeToken, playlistId,
                                 playlist, artist, allTracks, playCount, isUpdateDesc=isUpdateDesc)
    # Get new playlist info
    if playlistID == None:
        crawlSinglePlaylist(accessToken, playlistId,
                            './files/playlists/generated_playlists_info/', isPrivate=isPrivate)
    else:
        crawlSinglePlaylist(accessToken, playlistId,
                            './files/playlists/', isPrivate=isPrivate, spotify=spotify)


def playlistAddTracksByPlaycount(spotify, token, playlistId, playlist, artist, allTracks, playcount, isUpdateDesc=True):
    addTracksToPlaylistByPlaycount(
        spotify, token, playlistId, artist, allTracks, playcount)

    if isUpdateDesc:
        # Playlist name & description
        playlistName = artists[artist]['name'] + ' Most Played Songs'
        maximumPlaycountStr = getPlaycountStr(allTracks[0]['playcount'])
        oldDescription = playlist['description']
        playlistDescription = artists[artist]['name'] + ' most played songs (playcount > ' + \
            (str(playcount // 1000000) + ' million' if playcount >= 1000000 else str(playcount)) + \
            ', maxPlay: ' + maximumPlaycountStr + '). ' + \
            'Generated on ' + re.match(r'.*Generated on (.*)by ccg.*', oldDescription).group(1) + ' by ccg. '\
            'Updated on ' + time.strftime("%Y-%m-%d") + '.'
        res = updatePlayList(spotify, token, playlistId,
                             playlistName, playlistDescription, True)
        print('Response:', res)


if __name__ == '__main__':
    main()
