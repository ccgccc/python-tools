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
from playlistAddSongs import playlistAddSongs


# Define isPrivate & public playlist name
isPrivate = False
# playlistName = 'Favorite'
playlistName = 'Like'

# Define isPrivate & private playlist name
# isPrivate = True
# playlistName = 'To Listen'

# Define create playlist or update playlist
isCreate = False
# Define is incremental
isIncremental = True
# Defin cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


# Prepare check
playlistFileName = 'playlists/custom_playlists/playlist_' + playlistName
if isCreate:
    if os.path.isfile('./files/' + playlistFileName + '.json'):
        print('Alreay created playlist. Exit...')
        sys.exit()


# Get spotify playlist
with open('../spotify/files/playlists/playlist_' + playlistName + '_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
print('------------------------------')
allPlaylistTrackNames = [track['track']['name']
                         for track in spotifyPlaylist['tracks']['items']]
totalPlaylistTracks = len(allPlaylistTrackNames)
print('Spotify playlist track names: ',
      '(Total ', totalPlaylistTracks, ')', sep='')
print(allPlaylistTrackNames, '\n')

# Get spotify artists IDs
spotifyArtistIds = {v['artistId']: k for k, v in spotifyArtists.items()}
spotifyArtistIdsSet = spotifyArtistIds.keys()
# Initialize spotify artist track names, like this: {'artist': ['trackname', 'trackname2']}
spotifyArtistTrackNames = {k: [] for k, v in neteaseArtists.items()}
artistsNotFound = set()
for track in spotifyPlaylist['tracks']['items']:
    isArtistFound = False
    for trackArtist in track['track']['artists']:
        trackArtistId = trackArtist['id']
        if trackArtist['id'] in spotifyArtistIdsSet:
            artist = spotifyArtistIds.get(trackArtistId)
            if spotifyArtistTrackNames.get(artist) != None:
                spotifyArtistTrackNames[artist].append(track['track']['name'])
                isArtistFound = True
                break
    if not isArtistFound:
        artistsNotFound.add(
            '_'.join([artists['name'] for artists in track['track']['artists']]))
print('------------------------------')
totalTrackNames = sum([len(v) for k, v in spotifyArtistTrackNames.items()])
print('Spotify playlist track names: ',
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

syncSongs = {}
missingSongs = []
missingSongsStr = []
# Get sync songs
for artist, trackNames in spotifyArtistTrackNames.items():
    if len(trackNames) == 0:
        continue
    artistName = neteaseArtists[artist]['name']
    print('\n************************************************************')
    print('************************************************************')
    print('Processing', artistName, '......')
    curSyncSongs, curMissingSongs = getSyncSongs(
        artist, {artist: trackNames}, isRemoveAlias=True, isNeedPrompt=True, isOkPrompt=False)
    syncSongs = syncSongs | curSyncSongs
    missingSongs.extend(curMissingSongs)
    if len(curMissingSongs) > 0:
        missingSongsStr.append(
            '、'.join(curMissingSongs) + '(' + artistName + ')')
print('\n')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('All sync songs: ', len(syncSongs), '\n', syncSongs, '\n', sep='')
print('All missing songs: ', len(missingSongs),
      '\n', missingSongs, '\n', sep='')

# Create or clear playlist
if isCreate:
    # Create netease playlist
    playlist = createPlaylist(playlistName, isPrivate=isPrivate)
    playlistId = playlist['playlist']['id']
else:
    # Get netease playlist
    if not os.path.isfile('./files/' + playlistFileName + '.json'):
        print('Playlist not created yet. Please set isCreate to True.')
        sys.exit()
    playlist = loadJsonFromFile(playlistFileName)
    playlistId = playlist['playlist']['id']
    if not isIncremental:
        # Remove playlist songs
        playlistRomoveSongs(playlistId)
    else:
        playlistSongs = getPlaylistSongs(playlistId)
        playlistSongIdsSet = {song['id'] for song in playlistSongs['songs']}
        # Find not added songs
        syncSongs = {k: v for k, v in syncSongs.items()
                     if v not in playlistSongIdsSet}
        print('Incremental sync songs: ', len(
            syncSongs), '\n', syncSongs, '\n', sep='')
        if (len(syncSongs) == 0):
            print('Nothing to sync. Exiting...')
            sys.exit()


# Add songs & update playlist description
playlistAddSongs(playlistId, syncSongs, missingSongs,
                 spotifyPlaylist, isUpdateDesc=False)
playlistDescription = 'Synced from spotify.' + \
    ('Missing songs: ' + ', '.join(missingSongsStr) +
     '.') if len(missingSongsStr) > 0 else ''
updatePlaylistDesc(playlistId, playlistDescription)

# Get new playlist Info
playlist = getPlaylist(playlistId)
writeJsonToFile(playlist, playlistFileName)
