import time
from artists import *
from common import *
from syncSpotifyPlaylist import getSyncSongs

headers['cookie'] = readFileContent('cookie.txt')

playlist = loadJsonFromFile(
    'playlists/generated_playlists/' + artistToCrawl + '_playlist')
playlistId = playlist['playlist']['id']

syncSongs, missingSongs = getSyncSongs(artistToCrawl)
syncSongIds = ','.join(
    reversed(list(map(lambda song: str(list(song.values())[0]), syncSongs))))
# print(syncSongIds)

# update playlist description
isDescMissingSongs = False
playlistDescription = artists[artistToCrawl]['name'] + '播放最多歌曲，根据Spotify播放量数据自动生成' + ('，Missing: ' + '、'.join(
    missingSongs) if isDescMissingSongs else '') + '。Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
print(playlistDescription)
updatePlaylistDesc(playlistId, playlistDescription)

# addSongsToPlayList(playlistId, syncSongIds)
