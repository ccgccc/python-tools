import os
import sys
import time
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from spotify.artists import artists as spotifyArtists
from common import *
from netease.syncSongs import *
from playlistRemoveSongs import playlistRomoveSongs

# **************************************************
#    Sync spotify custom playlists to netease
# **************************************************

# Set baseUrl
setBaseUrl()

# Define create playlist or update playlist
isCreate = False


def main():
    # Read parameters from command line
    if len(sys.argv) < 2:
        print('Missing playlist name parameter. Exit...')
        sys.exit()
    # Read playlist name
    playlistName = sys.argv[1]
    # Define netease playlist is private or not
    isPrivate = False
    # Define is collection playlist
    isCollection = False
    # Define is incremental
    isIncremental = True
    # Define is reversed (usually same as isIncremental)
    isReversed = True
    # Define if add spotify missing songs
    addSpotifyMissing = False
    if playlistName in {'Favorite', 'Like'}:
        isPrivate = False
    elif playlistName in {'Nice', 'One Hit', 'To Listen', 'Netease Non-playable'}:
        isPrivate = True
    elif playlistName in {'Listening Artist', 'Listening'}:
        isPrivate = True
        isIncremental = False
        isReversed = False
    elif playlistName.startswith('Collection'):
        isCollection = True
        isPrivate = False
        isIncremental = False
        isReversed = False
        addSpotifyMissing = True
    print('--------------------')
    print('*** Sync Info ***')
    print('Playlist:', playlistName)
    print('IsPrivate:', isPrivate)
    print('IsIncremental:', isIncremental)
    print('IsReversed:', isReversed)
    print('--------------------')

    # Prepare check
    if playlistName.startswith('Collection'):
        playlistName = playlistName.split(' - ')[0]
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
    syncSongs, neteaseMissingSongs, neteaseMissingSongsStr, spotifyMissingSongsStr = getSpotifyToNeteaseSongs(
        spotifyArtistTrackIdNames, spotifyArtists, playlistName=playlistName, addSpotifyMissing=addSpotifyMissing, isNeedMissingPrompt=False)
    # if len(neteaseMissingSongs) > 0:
    #     sureCheck()

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
            print('Crawling netease playlist current songs...')
            playlistSongs = getPlaylistSongs(playlistId, addTs=True)['songs']
            playlistSongIdsSet = {song['id']
                                  for song in playlistSongs}
            # Find not added songs
            syncSongs = [song for song in syncSongs
                         if list(song.values())[0] not in playlistSongIdsSet]
            print('Playlist \'' + playlistName +
                  '\' songs:', len(playlistSongs))
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

    if not isCollection:
        playlistDescription = 'Sync between spotify and netease.' + \
            ((' Netease missing: ' + ', '.join(neteaseMissingSongsStr) +
              '.') if len(neteaseMissingSongsStr) > 0 else '') + \
            ((' Spotify Missing: ' + ', '.join(spotifyMissingSongsStr) +
              '.') if len(spotifyMissingSongsStr) > 0 else '') + \
            ' Updated on ' + time.strftime("%Y-%m-%d") + '.'
        # (updateMatch.group(0) if updateMatch != None else '')
    else:
        spotifyDesciption = spotifyPlaylist['description']
        datePart = re.sub(r'.*(Generated.*)', r'\1', spotifyDesciption)
        playlistDescription = 'Sync between spotify and netease.' + \
            ((' Netease missing: ' + ', '.join(neteaseMissingSongsStr) +
              '.') if len(neteaseMissingSongsStr) > 0 else '') + ' ' + datePart
    updatePlaylistDesc(playlistId, playlistDescription)

    # Get new playlist Info
    print('\nCrawling playlist new info...')
    playlist = getPlaylist(playlistId)
    writeJsonToFile(playlist, neteasePlaylistFileName)
    playlistSongs = getPlaylistSongs(playlistId)
    fileName = 'playlists/playlist_songs_' + playlistName + \
        '_by ' + playlist['playlist']['creator']['nickname']
    playlistSongs['playlist'] = playlist
    writeJsonToFile(playlistSongs, fileName)
    # printPlaylists([playlist['playlist']])
    # printSongs(playlistSongs['songs'], fileName)
    print('Done!')


if __name__ == '__main__':
    main()
