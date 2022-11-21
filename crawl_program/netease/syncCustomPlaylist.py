import os
import sys
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from spotify.artists import artists as spotifyArtists
from netease.common import *
from netease.syncSongs import *
from netease.playlistRemoveSongs import playlistRomoveSongs

# **************************************************
#    Sync spotify custom playlists to netease
# **************************************************

# Define create playlist or update playlist
isCreate = False
# Define cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


def main():
    # Read parameters from command line
    if len(sys.argv) < 2:
        print('Missing playlist name parameter. Exit...')
        sys.exit()
    # Read playlist name
    playlistName = sys.argv[1]
    # Define isPrivate & private playlist name
    isPrivate = False
    # Define is incremental
    isIncremental = True
    # Define is reversed (usually same as isIncremental)
    isReversed = True
    if playlistName in {'Nice', 'One Hit', 'To Listen', 'Netease Non-playable'}:
        isPrivate = True
    elif playlistName in {'Listening Artist'}:
        isPrivate = True
        isIncremental = False
        isReversed = False
    print('--------------------')
    print('*** Sync Info ***')
    print('Playlist:', playlistName)
    print('IsPrivate:', isPrivate)
    print('IsIncremental:', isIncremental)
    print('IsReversed:', isReversed)
    print('--------------------')

    # Prepare check
    neteasePlaylistFileName = 'playlists/custom_playlists/playlist_' + playlistName
    if isCreate:
        if os.path.isfile('./files/' + neteasePlaylistFileName + '.json'):
            print('Alreay created playlist. Exit...')
            sys.exit()

    # Get spotify playlist
    with open('../spotify/files/playlists/playlist_' + playlistName + '_by ccg ccc.json') as f:
        spotifyPlaylist = json.load(f)

    # Get songs to sync
    # Classify playlist tracks by artist
    spotifyArtistTrackIdNames = getSpotifyArtistTrackIdNames(
        playlistName, spotifyPlaylist['tracks'], spotifyArtists)
    # Get netease sync songs from spotify for every artist & merge all sync songs
    syncSongs, missingSongs, missingSongsStr = getSpotifyToNeteaseSongs(
        spotifyArtistTrackIdNames, spotifyArtists, isNeedMissingPrompt=False)

    # Create or clear playlist
    if isCreate:
        print('--------------------')
        print('isCreate:', isCreate)
        print('IsIncremental:', isIncremental)
        print('IsReversed:', isReversed)
        sureCheck()
        # Create netease playlist
        playlist = createPlaylist(playlistName, isPrivate=isPrivate)
        playlistId = playlist['playlist']['id']
    else:
        # Get netease playlist
        if not os.path.isfile('./files/' + neteasePlaylistFileName + '.json'):
            print('Playlist not created yet. Please set isCreate to True.')
            sys.exit()
        playlist = loadJsonFromFile(neteasePlaylistFileName)
        playlistId = playlist['playlist']['id']
        if isIncremental:
            playlistSongs = getPlaylistSongs(playlistId)['songs']
            playlistSongIdsSet = {song['id']
                                  for song in playlistSongs}
            # Find not added songs
            syncSongs = [song for song in syncSongs
                         if list(song.values())[0] not in playlistSongIdsSet]
            print('Playlist ' + playlistName + ' songs:', len(playlistSongs))
            print('Incremental sync songs: ', len(
                syncSongs), '\n', syncSongs, '\n', sep='')
            if (len(syncSongs) == 0):
                print('Nothing to sync. Exiting...')
                sys.exit()
        print('--------------------')
        print('isCreate:', isCreate)
        print('IsIncremental:', isIncremental)
        print('IsReversed:', isReversed)
        sureCheck()
        if not isIncremental:
            # Remove playlist songs
            playlistRomoveSongs(playlistId)

    # Add songs & update playlist description
    if not isReversed:
        syncSongs = list(reversed(syncSongs))
    syncSongIds = ','.join([str(list(song.values())[0]) for song in syncSongs])
    addSongsToPlayList(playlistId, syncSongIds)

    playlistDescription = 'Sync between spotify and netease.' + \
        ((' Missing songs: ' + ', '.join(missingSongsStr) +
         '.') if len(missingSongsStr) > 0 else '')
    updatePlaylistDesc(playlistId, playlistDescription)

    # Get new playlist Info
    playlist = getPlaylist(playlistId)
    writeJsonToFile(playlist, neteasePlaylistFileName)


if __name__ == '__main__':
    main()
