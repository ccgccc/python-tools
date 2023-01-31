import os
import sys
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from spotify.artists import artists as spotifyArtists
from common import *
from netease.syncSongs import getSpotifyArtistTrackIdNames
from syncCustomPlaylist import getSpotifyToNeteaseSongs
from playlistRemoveSongs import playlistRomoveSongs

# **********************************************************************
#    Sync spotify Favorite & Like playlists to netease liked songs
# **********************************************************************

# My like songs playlist id
likePlaylistId = 553778357
# Define is incremental
isIncremental = True

# Sync from spotify Favorite & Like playlist
# Get spotify Favorite playlist
with open('../spotify/files/playlists/playlist_' + 'Favorite' + '_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
spotifyArtistTrackNames = getSpotifyArtistTrackIdNames(
    'Favorite', spotifyPlaylist['tracks'], spotifyArtists)
# Get spotify Like playlist
with open('../spotify/files/playlists/playlist_' + 'Like' + '_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
spotifyArtistTrackNames2 = getSpotifyArtistTrackIdNames(
    'Like', spotifyPlaylist['tracks'], spotifyArtists)

# Get spotify liked songs
# with open('../spotify/files/playlists/my_liked_songs.json') as f:
#     spotifyLikedTracks = json.load(f)
# syncSongs, missingSongs, missingSongsStr = getSpotifyToNeteaseSongs(
#     spotifyLikedTracks)

print('\n')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
for artist, trackNames in spotifyArtistTrackNames2.items():
    if spotifyArtistTrackNames.get(artist) != None:
        spotifyArtistTrackNames[artist].extend(trackNames)
    else:
        spotifyArtistTrackNames[artist] = trackNames
totalTrackNames = sum([len(v) for k, v in spotifyArtistTrackNames.items()])
print('Favorite & Like sync songs: ',
      '(Total ', totalTrackNames, ')', sep='')
print(spotifyArtistTrackNames, '\n')

syncSongs, missingSongs, neteaseMissingSongsStr, spotifyMissingTracksStr = getSpotifyToNeteaseSongs(
    spotifyArtistTrackNames, spotifyArtists, isNeedMissingPrompt=False)
syncSongDict = {str(list(song.values())[0]): list(song.keys())[0]
                for song in syncSongs}

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
if isIncremental:
    # Get liked songs
    likedSongs = getPlaylistSongs(likePlaylistId)['songs']
    syncSongIds = {str(list(song.values())[0]) for song in syncSongs}\
        - {str(song['id']) for song in likedSongs}
    if len(syncSongIds) > 0:
        syncSongIds = list(reversed(list(syncSongIds)))
else:
    syncSongIds = [str(list(song.values())[0])
                   for song in syncSongs]
print('To sync: ', len(syncSongIds))
print({k: v for k, v in syncSongDict.items() if k in syncSongIds})
print('\nIsIncremental:', isIncremental)
sureCheck()

if not isIncremental:
    # Remove playlist songs
    playlistRomoveSongs(likePlaylistId)
addSongsToPlayList(likePlaylistId, ','.join(syncSongIds))
