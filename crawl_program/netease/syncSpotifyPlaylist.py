import os
import sys
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from artists import *
from common import *
from netease.syncSongs import getSyncSongs
from playlistCreate import generatePlaylist
from playlistRemoveSongs import playlistRomoveSongs
from playlistAddSongs import playlistAddSongs

# ************************************************************
#     Sync spotify most played songs playlists to netease
# ************************************************************

# Define artist here
artistToSyncList = [artistToCrawl]
# Define create playlist or update playlist
isCreate = True
# Define if update description
isUpdateDesc = True
# Define if need prompt in getting sync songs
isSyncNeedPrompt = True
# Define if prompt no missing songs in getting sync songs
isOkPrompt = False
# Define if propmt updating missing description
isPromptDescMissing = True
# Read parameters from command line
if len(sys.argv) >= 2:
    if sys.argv[1] == 'update':
        isCreate = False
        if len(sys.argv) >= 3:
            if sys.argv[2] == 'all':
                artistToSyncList = list(generateArtists.keys())
                isSyncNeedPrompt = False
                isPromptDescMissing = False
            else:
                artistToSyncList = [sys.argv[2]]
    else:
        print('Parameter not supported. Exit...')
        sys.exit()


# Define cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


def main():
    for artist in artistToSyncList:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Updating ' + artists[artist]['name'] + '...')
        syncSpotifyPlaylist(artist)


def syncSpotifyPlaylist(artist):
    # Prepare check
    if isCreate:
        if os.path.isfile('./files/playlists/generated_playlists/' + artist + '_playlist.json'):
            print('Alreay created playlist. Exit...')
            sys.exit()

    # Get spotify playlist
    with open('../spotify/files/playlists/generated_playlists_info/playlist_' +
              artists[artist]['name'] + ' Most Played Songs_by ccg ccc.json') as f:
        spotifyPlaylist = json.load(f)
    # Get sync songs
    seen = set()
    spotifyTrackIdNames = []
    for track in spotifyPlaylist['tracks']['items']:
        trackUri = track['track']['uri']
        trackName = track['track']['name']
        if trackName not in seen:
            spotifyTrackIdNames.append({trackUri: trackName})
            seen.add(trackName)
        else:
            spotifyTrackIdNames.append({trackUri: trackName + '_2_' +
                                   track['track']['artists'][0]['name']})

    syncSongs, missingSongs = getSyncSongs(
        artist, spotifyTrackIdNames, isRemoveAlias=True, isNeedPrompt=isSyncNeedPrompt, isOkPrompt=isOkPrompt)

    # Create or clear playlist
    if isCreate:
        # Create netease playlist
        playlist = generatePlaylist(artist, isUpdateDesc=False)
        playlistId = playlist['playlist']['id']
    else:
        # Get netease playlist
        fileName = 'playlists/generated_playlists/' + artist + '_playlist'
        if not os.path.isfile('./files/' + fileName + '.json'):
            print('Playlist not created yet. Please set isCreate to True.')
            sys.exit()
        playlist = loadJsonFromFile(fileName)
        playlistId = playlist['playlist']['id']
        # Remove playlist songs
        playlistRomoveSongs(playlistId)

    # Add songs & update playlist description
    playlistAddSongs(artist, playlistId, syncSongs, missingSongs,
                     spotifyPlaylist, isUpdateDesc=isUpdateDesc, isPromptDescMissing=isPromptDescMissing)
    # Get new playlist Info
    playlist = getPlaylist(playlistId)
    writeJsonToFile(playlist, 'playlists/generated_playlists/' +
                    artist + '_playlist')


if __name__ == '__main__':
    main()
