from artists import *
from common import *

# ******************************
#    Get netease all albums
# ******************************


def main():
    crawlAlbums(artists, artistToCrawl)


def crawlAlbums(artists, artistToCrawl):
    allAlbums = getArtistAlbums(artists[artistToCrawl]['artistId'])
    # allAlbums = loadJsonFromFile('albums/' + artistToCrawl + '_albums')
    allAlbums.sort(key=lambda album: (album['publishTime'], album['name']))

    fileName = 'albums/' + artistToCrawl + '_albums'
    writeJsonToFile(allAlbums, fileName)
    printAlbums(allAlbums, fileName)
    return allAlbums


if __name__ == '__main__':
    main()
