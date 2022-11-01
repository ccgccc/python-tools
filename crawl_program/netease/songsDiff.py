from common import *

# ******************************
#  Like vs Playlists difference
# ******************************

# Define cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


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
playlists = {
    "Netease Liked_Playable": 7721015504
}
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
print('Only in Playlists:')
playlistOnlySongIds = []
for song in playlistSongs:
    if song['id'] not in songIds:
        print(song['name'])
        playlistOnlySongIds.append(song['id'])
if len(playlistOnlySongIds) > 0:
    print('\nSong ids:', len(playlistOnlySongIds))
    print(','.join(playlistOnlySongIds))
print('--------------------')
