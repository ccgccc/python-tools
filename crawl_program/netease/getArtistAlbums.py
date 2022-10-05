from artists import *
from common import *


def main():
    crawlAlbums(artists, artistToCrawl)


def crawlAlbums(artists, artistToCrawl):
    allAlbums = getArtistAlbums(artists[artistToCrawl]['artistId'])
    allAlbums = sorted(allAlbums, key=lambda album: album['publishTime'])

    fileName = 'albums/' + artistToCrawl + '_albums'
    writeJsonToFile(allAlbums, fileName)
    printAlbums(allAlbums, fileName)
    return allAlbums


if __name__ == '__main__':
    main()
