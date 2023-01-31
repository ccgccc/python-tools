from common import *

# ******************************
#  Like vs Playlists difference
# ******************************


# Get liked songs
likePlaylistId = 553778357  # 我喜欢的音乐
likedSongs = getPlaylistSongs(likePlaylistId)['songs']
songIds = {song['id'] for song in likedSongs}
# print(songIds)
print('--------------------')
print('\u2764\uFE0F:', len(songIds))  # heart symbol

# Get playlist songs
playlists = {
    "Favorite": 7673625615,
    "Like": 7673790351
}
# playlists = {
#     "Netease Liked_Playable": 7721015504
# }
playlistSongs = []
print('--------------------')
totalSongs = 0
for playlistName, playlistId in playlists.items():
    curPlaylistSongs = getPlaylistSongs(playlistId)['songs']
    playlistSongs.extend(curPlaylistSongs)
    totalSongs = totalSongs + len(curPlaylistSongs)
    print(playlistName + ':', len(curPlaylistSongs))
print('Total:', totalSongs)
songIds2 = {song['id'] for song in playlistSongs}
# print(songIds2)


# Only in Like
print('\n--------------------')
likeOnlySongs = [song['name'] for song in likedSongs
                 if song['id'] not in songIds2]
print('Only in \u2764\uFE0F:', len(likeOnlySongs))
print(likeOnlySongs)


# Only in Playlists
print('--------------------')
playlistAllSongIds = []
playlistOnlySongs = []
for song in playlistSongs:
    playlistAllSongIds.append(song['id'])
    if song['id'] not in songIds:
        playlistOnlySongs.append({song['id']: song['name']})
print('Only in Playlists:', len(playlistOnlySongs))
print([list(dict.values())[0] for dict in playlistOnlySongs])
if len(playlistOnlySongs) > 0:
    print('Song ids:', len(playlistOnlySongs))
    print(','.join([str(list(dict.keys())[0]) for dict in playlistOnlySongs]))
seen = set()
dupes = [songId for songId in playlistAllSongIds
         if songId in seen or seen.add(songId)]
print('Dupes:', len(dupes))
if len(dupes) > 0:
    print('Dupes:', [song['name']
                     for song in playlistSongs if song['id'] in dupes])
print('--------------------')
