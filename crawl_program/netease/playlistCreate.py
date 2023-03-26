import time
from os import listdir
from os.path import isfile, join
from artists import *
from common import *

# **************************************************
#     Create netease most played songs playlist
# **************************************************


def main():
    # Set baseUrl
    setBaseUrl()
    dir = './files/playlists/generated_playlists/'
    fileNames = [f for f in listdir(dir) if isfile(join(dir, f))]
    if artistToCrawl + '_playlist.json' in fileNames:
        print('Alreay created playlist. Exit...')
        sys.exit()

    generatePlaylist(artistToCrawl)


def generatePlaylist(artist, isUpdateDesc=True):
    # create playlist
    playlistName = artists[artist]['name'] + ' Most Played Songs'
    playlist = createPlaylist(playlistName)
    # print(playlist)
    writeJsonToFile(playlist, 'playlists/generated_playlists/' +
                    artist + '_playlist')

    if isUpdateDesc:
        # update playlist description
        playlistDescription = artists[artist]['name'] + '播放最多歌曲，根据Spotify播放量数据自动生成。' + \
            'Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.'
        updatePlaylistDesc(playlist['playlist']['id'], playlistDescription)
    return playlist


if __name__ == '__main__':
    main()
