from common import *
from syncCustomPlaylist import getSpotifyToNeteaseSongs, getSpotifyArtistTrackNames
from playlistRemoveSongs import playlistRomoveSongs

# **********************************************************************
#    Sync spotify Favorite & Like playlists to netease liked songs
# **********************************************************************

# My like songs playlist id
likePlaylistId = 553778357
# Define is incremental
isIncremental = True
# Define cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


# Sync from spotify Favorite & Like playlist
# Get spotify Favorite playlist
with open('../spotify/files/playlists/playlist_' + 'Favorite' + '_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
spotifyArtistTrackNames = getSpotifyArtistTrackNames(
    spotifyPlaylist['tracks'])
# Get spotify Like playlist
with open('../spotify/files/playlists/playlist_' + 'Like' + '_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
spotifyArtistTrackNames2 = getSpotifyArtistTrackNames(
    spotifyPlaylist['tracks'])

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

syncSongs, missingSongs, missingSongsStr = getSpotifyToNeteaseSongs(
    spotifyArtistTrackNames, isNeedMissingPrompt=False)

syncSongIds = ','.join([str(list(song.values())[0]) for song in syncSongs])
print('To sync: ', len(syncSongs), '\n', syncSongIds, sep='')

sureCheck()

if not isIncremental:
    # Remove playlist songs
    playlistRomoveSongs(likePlaylistId)

addSongsToPlayList(likePlaylistId, syncSongIds)
