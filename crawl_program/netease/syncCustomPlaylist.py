import os
import sys
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from spotify.artists import artists as spotifyArtists
from artists import artists as neteaseArtists
from common import *
from syncSongs import getSyncSongs
from playlistRemoveSongs import playlistRomoveSongs

# **************************************************
#    Sync spotify custom playlists to netease
# **************************************************

# Define create playlist or update playlist
isCreate = False
# Define cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')

# Read parameters from command line
if len(sys.argv) < 2:
    print('Missing playlist name parameter.')
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


def main():
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
    spotifyArtistTrackNames = getSpotifyArtistTrackNames(
        spotifyPlaylist['tracks'])
    syncSongs, missingSongs, missingSongsStr = getSpotifyToNeteaseSongs(
        spotifyArtistTrackNames, isReversed, isNeedMissingPrompt=False)

    # Create or clear playlist
    if isCreate:
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

    playlistDescription = 'Synced from spotify. ' + \
        ('Missing songs: ' + ', '.join(missingSongsStr) +
         '.') if len(missingSongsStr) > 0 else ''
    updatePlaylistDesc(playlistId, playlistDescription)

    # Get new playlist Info
    playlist = getPlaylist(playlistId)
    writeJsonToFile(playlist, neteasePlaylistFileName)


def getSpotifyToNeteaseSongs(spotifyArtistTrackNames, isReversed, isNeedMissingPrompt=True):
    syncSongs = []
    missingSongs = []
    missingSongsStr = []
    # Get sync songs
    for artist, trackNames in spotifyArtistTrackNames.items():
        if len(trackNames) == 0:
            continue
        artist = artist.split('-')[0]
        artistName = neteaseArtists[artist]['name']
        print('\n************************************************************')
        print('************************************************************')
        print('Processing', artistName, '......')
        curSyncSongs, curMissingSongs = getSyncSongs(
            artist, {artist: trackNames}, isRemoveAlias=True, isNeedPrompt=False, isOkPrompt=False)
        syncSongs.extend(reversed(curSyncSongs)
                         if isReversed else curSyncSongs)
        missingSongs.extend(curMissingSongs)
        if len(curMissingSongs) > 0:
            missingSongsStr.append(
                '、'.join(curMissingSongs) + '(' + artistName + ')')
        print('Acc count:', len(syncSongs))
    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('All sync songs: ', len(syncSongs), '\n', json.dumps(
        syncSongs, ensure_ascii=False), '\n', sep='')
    print('All missing songs: ', len(missingSongs),
          '\n', json.dumps(missingSongs, ensure_ascii=False), '\n', sep='')
    if isNeedMissingPrompt and len(missingSongs) > 0:
        sureCheck()
    return syncSongs, missingSongs, missingSongsStr


def getSpotifyArtistTrackNames(spotifyPlaylistTracks):
    print('------------------------------')
    allPlaylistTrackNames = [track['track']['name']
                             for track in spotifyPlaylistTracks['items']]
    totalPlaylistTracks = len(allPlaylistTrackNames)
    print('Spotify playlist track names: ',
          '(Total ', totalPlaylistTracks, ')', sep='')
    print(allPlaylistTrackNames, '\n')

    # Get spotify artists IDs
    spotifyArtistIds = {v['artistId']: k for k, v in spotifyArtists.items()}
    spotifyArtistIdsSet = spotifyArtistIds.keys()
    # Initialize spotify artist track names, like this: {'artist': ['trackname', 'trackname2']}
    spotifyArtistTrackNames = {}
    artistsNotFound = set()
    seenTrackNames = set()
    for track in spotifyPlaylistTracks['items']:  # Iterate playlist tracks
        isArtistFound = False
        for trackArtist in track['track']['artists']:  # Iterate track artists
            trackArtistId = trackArtist['id']
            if trackArtist['id'] in spotifyArtistIdsSet:
                # Classify tracks to artists & rename duplicate track names
                artist = spotifyArtistIds.get(trackArtistId)
                if spotifyArtistTrackNames.get(artist) == None:
                    spotifyArtistTrackNames[artist] = []
                trackName = track['track']['name']
                if trackName not in seenTrackNames:
                    spotifyArtistTrackNames[artist].append(trackName)
                    seenTrackNames.add(trackName)
                else:
                    spotifyArtistTrackNames[artist].append(
                        trackName + '_2_' + track['track']['artists'][0]['name'])
                isArtistFound = True
                break
        if not isArtistFound:
            artistsNotFound.add(
                '_'.join([artists['name'] for artists in track['track']['artists']]))
    print('------------------------------')
    totalTrackNames = sum([len(v) for k, v in spotifyArtistTrackNames.items()])
    print('Spotify playlist track names(classified): ',
          '(Total ', totalTrackNames, ')', sep='')
    print(spotifyArtistTrackNames, '\n')

    if (len(artistsNotFound) > 0):
        print('------------------------------')
        print('These artists are not crawled yet, please crawl them first:',
              artistsNotFound, '\n')
        sys.exit()
    if (totalTrackNames != totalPlaylistTracks):
        print('------------------------------')
        print('Track numbers don\'t match, please check', artistsNotFound)
        sys.exit()
    return spotifyArtistTrackNames


if __name__ == '__main__':
    main()
