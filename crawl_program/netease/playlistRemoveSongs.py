from artists import *
from common import *


def main():
    headers['cookie'] = readFileContent('cookie.txt')

    playlist = loadJsonFromFile(
        'playlists/generated_playlists/' + artistToCrawl + '_playlist')
    playlistId = playlist['playlist']['id']

    playlistRomoveSongs(playlistId)


def playlistRomoveSongs(playlistId):
    playlistSongs = getPlaylistSongs(playlistId)
    if (len(playlistSongs['songs']) == 0):
        print('Nothing to delete, continue...')
        return
    removeSongIds = ','.join(
        reversed(list(map(lambda song: str(song['id']), playlistSongs['songs']))))
    print('To delete:', removeSongIds)

    deleteSongsToPlayList(playlistId, removeSongIds)


if __name__ == '__main__':
    main()
