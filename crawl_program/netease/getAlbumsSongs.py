from datetime import datetime
from artists import *
from common import *


def main():
    # Get artist albums
    allAlbums = loadJsonFromFile('albums/' + artistToCrawl + '_albums')

    # Get all songs & write to file
    getAlbumsSongs(allAlbums)


def getAlbumsSongs(allAlbums, mustMainArtist=False):
    # Get all albums tracks
    allSongs = []
    albumCount = 0
    # for album in allAlbums[0:5]:
    for album in allAlbums:
        print('--------------------')
        albumCount = albumCount + 1
        albumId = album['id']
        albumName = album['name']
        albumAlias = album['alias']
        albumType = album['type']
        albumSubType = album['subType']
        albumSize = album['size']
        albumArtists = '_'.join(
            list(map(lambda artist: artist['name'], album['artists'])))
        publishMs = album.get('publishTime')
        publishTime = datetime.fromtimestamp(
            publishMs / 1000).strftime('%Y-%m-%d') if publishMs != None else '--'
        company = album['company']
        print(str(albumCount) + ': ' + albumName)
        print('Album Id: ' + str(albumId))
        print('Album Artist: ' + albumArtists)
        print('Release Date: ' + publishTime)
        print('Total Tracks: ' + str(albumSize))

        # API requests
        albumSongs = getAlbum(albumId)
        # printAlbums([albumSongs['album']])
        allSongs.extend(albumSongs['songs'])
        printSongs(albumSongs['songs'])
    # Write json to file
    fileName = 'songs/' + artistToCrawl + '_allsongs_raw'
    writeJsonToFile(allSongs, fileName)
    printSongs(allSongs, fileName, isWriteToConsole=False)
    return allSongs


if __name__ == '__main__':
    main()
