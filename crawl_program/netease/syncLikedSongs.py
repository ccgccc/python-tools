from common import *
from syncCustomPlaylist import getSpotifyToNeteaseSongs, getSpotifyArtistTrackNames

# My like songs playlist id
likePlaylistId = 553778357
# Use right cookie to retrive private playlists
headers['cookie'] = readFileContent('cookie.txt')


# Not recommended, only like one song and constrain to copyright
# songId = 29822033
# # songId = 29822044
# res = likeSong(songId)
# print(res, res.text)

# Get spotify liked songs
# with open('../spotify/files/playlists/my_liked_songs.json') as f:
#     spotifyLikedTracks = json.load(f)
# syncSongs, missingSongs, missingSongsStr = getSpotifyToNeteaseSongs(
#     spotifyLikedTracks)

# Get spotify Favorite playlist
with open('../spotify/files/playlists/playlist_' + 'Favorite' + '_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
# Get songs to sync
spotifyArtistTrackNames = getSpotifyArtistTrackNames(
    spotifyPlaylist['tracks'])
# Get spotify Like playlist
with open('../spotify/files/playlists/playlist_' + 'Like' + '_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
# Get songs to sync
spotifyArtistTrackNames2 = getSpotifyArtistTrackNames(
    spotifyPlaylist['tracks'])


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

addSongsToPlayList(likePlaylistId, syncSongIds)
