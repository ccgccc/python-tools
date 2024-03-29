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

# Define playlist id
playlistID = None  # Generated playlist (maybe multi playlists)
# Define if playlist is private
isPrivate = False
# Define is collection playlist
isCollection = False
# Define track number to add
trackNumber = -1
# Define if playlist is private
isIncremental = False
# Define if update description
isUpdateDesc = True
if len(sys.argv) > 1:
    if len(artistToCrawlList) > 1:
        print('Can\'t specify playlist for multi artists.')
        sys.exit()
    # Specify playlist
    playlistName = sys.argv[1]
    if playlistName in {'Listening Artist'}:
        playlistID = '2R48aLSO7QmOaHAGaV0zIM'  # Listening Artist
        isPrivate = True
        isIncremental = False
        isUpdateDesc = False
        if len(sys.argv) > 2:
            isCollection = True
            artistToCrawlList = sys.argv[2:]
    elif playlistName.startswith('Collection'):  # Collection
        isCollection = True
        isPrivate = False
        isIncremental = False
        isUpdateDesc = True
        if len(sys.argv) > 2:
            artistToCrawlList = sys.argv[2:]
        if playlistName.startswith('Collection 1'):
            playlistID = '5uo2JUVt9WQltVwijJzZmb'
        elif playlistName.startswith('Collection 2'):
            playlistID = '1flURo4qPHOPIKGVsHA8Wu'
        elif playlistName.startswith('Collection 3'):
            playlistID = '5LttjuXGEC9cpcphLK7TLi'
        elif playlistName.startswith('Collection 4'):
            playlistID = '2r9Iqy5D80rSs7QKmRnN6f'
        elif playlistName.startswith('Collection 5'):
            playlistID = '0sE2cDp3NTGmKzy64rr9mL'
        else:
            print('Collection not created yet...')
            sys.exit()


def main():
    # Get accessToken
    accessToken = getAccessToken(clientID, clientSecret)
    # Get spotify authorization authorizeToken by scope
    scope = [
        "playlist-read-private",
        "playlist-modify-private",
        "playlist-modify-public"
    ]
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)

    global trackNumber
    global isIncremental
    for i in range(len(artistToCrawlList)):
        artist = artistToCrawlList[i]
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Updating ' + artists[artist]['name'] + '...')
        generateInfo = artists[artist].get('generateInfo')
        if generateInfo != None:
            generateMethod = generateInfo['generateMethod']
            if len(artistToCrawlList) > 1 or trackNumber < 0:
                trackNumber = generateInfo['number']
            if generateMethod != 1:
                print('GenerateMethod != 1, continue\n')
                continue
        elif len(artistToCrawlList) > 1:
            print('Can\'t find generate info in artists.py.')
            sys.exit()

        playlistAddItemsByNumber(
            artist, trackNumber, accessToken, spotify, authorizeToken)
        if isCollection:
            # Set isIncremental = True from collection's second artist
            isIncremental = True
            # Update playlist description on last artsit
            if isUpdateDesc and i == len(artistToCrawlList) - 1:
                with open('./files/playlists/playlist_' + playlistName + '_by ccg ccc.json') as f:
                    playlist = json.load(f)
                playlistId = playlist['id']
                oldplaylistDescription = playlist['description']
                if oldplaylistDescription:
                    playlistDescription = re.sub(r'(.*?) ?Updated on.*', r'\1', oldplaylistDescription) \
                        + ' Updated on ' + time.strftime("%Y-%m-%d") + '.'
                else:
                    playlistDescription = 'Sync between spotify and netease. Generated on ' + \
                        time.strftime("%Y-%m-%d") + ' by ccg.'
                updatePlayList(spotify, authorizeToken, playlistId,
                               None, playlistDescription, True)
                crawlSinglePlaylist(accessToken, playlistId,
                                    './files/playlists/', isPrivate=isPrivate, spotify=spotify)


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

    if not isIncremental:
        playlistRemoveAllItems(accessToken, spotify,
                               authorizeToken, playlistId, isPrivate=isPrivate)
    playlistAddTracksByNumber(spotify, authorizeToken, playlistId, playlist, artist,
                              allTracks, trackNumber, isCollection=isCollection, isUpdateDesc=isUpdateDesc)
    # Get new playlist info
    if playlistID == None:
        crawlSinglePlaylist(accessToken, playlistId,
                            './files/playlists/generated_playlists_info/', isPrivate=isPrivate)
    else:
        playlist = crawlSinglePlaylist(accessToken, playlistId,
                                       './files/playlists/', isPrivate=isPrivate, spotify=spotify)


def playlistAddTracksByNumber(spotify, token, playlistId, playlist, artist, allTracks, trackNumber,
                              isCollection=False, isUpdateDesc=True):
    resJson, specialAddingTracks = addTracksToPlaylistByNumber(
        spotify, token, playlistId, artist, allTracks, trackNumber)

    if not isCollection and isUpdateDesc:
        # Playlist name & description
        playlistName = artists[artist]['name'] + ' Most Played Songs'
        maximumPlaycountStr = getPlaycountStr(
            allTracks[0]['playcount'])
        minimumPlaycountStr = getPlaycountStr(
            allTracks[trackNumber - 1]['playcount'])
        playlistDescription = artists[artist]['name'] + \
            ' most played songs (top ' + str(trackNumber) + \
            ', maxPlay: ' + maximumPlaycountStr + \
            ', minPlay: ' + minimumPlaycountStr + \
            (', special adding: ' + ','.join(specialAddingTracks.values())
             if len(specialAddingTracks) > 0 else '') + '). '
        if playlist == None:  # Create playlist
            playlistDescription = playlistDescription + \
                'Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
        else:  # Update playlist
            oldDescription = playlist['description']
            playlistDescription = playlistDescription + \
                'Generated on ' + re.match(r'.*Generated on (.*)by ccg.*', oldDescription).group(1) + ' by ccg. ' + \
                'Updated on ' + time.strftime("%Y-%m-%d") + '.'
        updatePlayList(spotify, token, playlistId,
                       playlistName, playlistDescription, True)


if __name__ == '__main__':
    main()
