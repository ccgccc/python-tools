from artists import *
from common import *
from syncSongs import getSyncSongs
from playlistCreate import generatePlaylist
from playlistAddSongs import playlistAddSongs


def main():
    headers['cookie'] = readFileContent('cookie.txt')
    syncSongs, missingSongs = getSyncSongs(artistToCrawl, isRemoveAlias=True)
    playlist = generatePlaylist(artistToCrawl, isUpdateDesc=False)
    playlistAddSongs(playlist['playlist']['id'],
                     syncSongs, missingSongs, isDescMissingSongs=True)


if __name__ == '__main__':
    main()
