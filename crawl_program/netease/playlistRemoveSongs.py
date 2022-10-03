from artists import *
from common import *

headers['cookie'] = readFileContent('cookie.txt')

playlist = loadJsonFromFile(
    'playlists/generated_playlists/' + artistToCrawl + '_playlist')
playlistId = playlist['playlist']['id']

playlistSongs = getPlaylistSongs(playlistId)
removeSongIds = ','.join(
    reversed(list(map(lambda song: str(song['id']), playlistSongs['songs']))))
print(removeSongIds)

deleteSongsToPlayList(playlistId, removeSongIds)
