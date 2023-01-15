from common import *

# Define cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


def main():
    # getPlaylistSongs()
    addPlaylistSongs()
    # LikeSongs()


# ********** Get playlist songs **********
def getPlaylistSongs():
    playlistName = 'Collection 1'

    fileName = 'playlists/playlist_songs_' + playlistName + '_by ccgccc'
    playlist = loadJsonFromFile(fileName)
    print({song['name']: str(song['id']) for song in playlist['songs']})
    print([song['name'] for song in playlist['songs']])
    print([str(song['id']) for song in playlist['songs']])


# ********** Add playlist songs **********
def addPlaylistSongs():
    syncSongIds = ['307679', '1411752556']

    # Playlist id
    # playlistId = 7673625615,  # Favorite
    # playlistId = 7673790351,  # Like
    playlistId = 7680312360,  # Nice
    addSongsToPlayList(playlistId, ','.join(syncSongIds))


# ********** Like songs **********
def LikeSongs():
    syncSongIds = ['1335640448', '1334799022', '1335640447']

    # My like songs playlist id
    likePlaylistId = 553778357
    addSongsToPlayList(likePlaylistId, ','.join(syncSongIds))


if __name__ == '__main__':
    main()
