from common import *

# ******************************
#   Get netease playlist by id
# ******************************

# Define palylist id
playlistId = 7673625615  # Favorite
# Liked songs playlist id
# playlistId = 553778357


playlist = getPlaylist(playlistId)

writeJsonToFile(playlist, 'playlists/playlist_' +
                playlist['playlist']['name'] + '_by ' + playlist['playlist']['creator']['nickname'])

printPlaylists([playlist['playlist']])
print('Track Ids:' +
      ', '.join(map(lambda track: str(track['id']), playlist['playlist']['trackIds'])))
printSongs(playlist['playlist']['tracks'])
