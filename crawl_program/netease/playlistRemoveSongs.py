from artists import *
from common import *

# **************************************************
#  Remove netease most played songs playlist songs
# **************************************************


def main():
    # Set baseUrl
    setBaseUrl()

    playlist = loadJsonFromFile(
        'playlists/generated_playlists/' + artistToCrawl + '_playlist')
    playlistId = playlist['playlist']['id']

    # Liked songs playlist id
    # playlistId = 553778357

    playlistRomoveSongs(playlistId, isSureCheck=True)


def playlistRomoveSongs(playlistId, isSureCheck=False):
    print("\n--------------------")
    # print(getBaseUrl())
    print('Crawling netease playlist current songs...')
    playlistSongs = getPlaylistSongs(playlistId, addTs=True)
    if (len(playlistSongs['songs']) == 0):
        print('Nothing to delete, continue...')
        return
    removeSongIds = ','.join(
        reversed(list(map(lambda song: str(song['id']), playlistSongs['songs']))))
    print('To delete: ', len(
        playlistSongs['songs']), '\n', removeSongIds, sep='')

    if isSureCheck:
        # sureCheck()
        # Set baseUrl
        setBaseUrl(needCheck=True)

    deleteSongsToPlayList(playlistId, removeSongIds)


if __name__ == '__main__':
    main()
