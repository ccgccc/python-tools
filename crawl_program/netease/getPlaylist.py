from common import *

playlistId = 627791787

playlist = getPlaylist(playlistId)

writeJsonToFile(playlist, 'playlists/playlist_' +
                playlist['playlist']['name'] + '_by ' + playlist['playlist']['creator']['nickname'])

printPlaylists([playlist['playlist']])
print('Track Ids:' +
      ', '.join(map(lambda track: str(track['id']), playlist['playlist']['trackIds'])))
printSongs(playlist['playlist']['tracks'])