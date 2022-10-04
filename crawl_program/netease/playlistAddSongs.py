import time
from artists import *
from common import *
from syncSongs import getSyncSongs


def main():
    headers['cookie'] = readFileContent('cookie.txt')

    playlist = loadJsonFromFile(
        'playlists/generated_playlists/' + artistToCrawl + '_playlist')
    playlistId = playlist['playlist']['id']

    syncSongs, missingSongs = getSyncSongs(artistToCrawl, isRemoveAlias=True)

    playlistAddSongs(playlistId, syncSongs, missingSongs)


def playlistAddSongs(playlistId, syncSongs, missingSongs, isPromptDescMissing=True, confirmOnceMode=False):
    syncSongIds = ','.join(
        reversed(list(map(lambda song: str(list(song.values())[0]), syncSongs))))
    # print(syncSongIds)
    addSongsToPlayList(playlistId, syncSongIds)

    # Update playlist description
    print()
    isDescMissingSongs = True
    if isPromptDescMissing:
        while True:
            if len(missingSongs) > 0:
                continueMsg = input(
                    'Do you want to add missing songs to playlist description? (y/n): ')
            else:
                break
            if continueMsg == 'y' or continueMsg == 'Y':
                isDescMissingSongs = True
                break
            elif confirmOnceMode or continueMsg == 'n' or continueMsg == 'N':
                isDescMissingSongs = False
                break
    # isDescMissingSongs = True
    missingSongsPart = ('，Missing: ' + '、'.join(missingSongs)
                        if isDescMissingSongs else '')
    playlistDescription = artists[artistToCrawl]['name'] + '播放最多歌曲，根据Spotify播放量数据自动生成' + \
        missingSongsPart + '。Generated on ' + \
        time.strftime("%Y-%m-%d") + ' by ccg.'
    # print(playlistDescription)
    updatePlaylistDesc(playlistId, playlistDescription)


if __name__ == '__main__':
    main()
