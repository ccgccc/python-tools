import re
import json
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken
from artists import artists, artistToCrawl
from spotifyFunc import *

# ******************************
#  Crawl spotify artist albums
# ******************************

# Define artist to crawl here
artistToCrawlList = [artistToCrawl]
# Crawl all artists
# artistToCrawlList = artists.keys()


def main():
    for artist in artistToCrawlList:
        print('--------------------')
        print('Processing ' + artists[artist]['name'] + '...')
        token = getAccessToken(clientID, clientSecret)
        crawlAlbums(token, artists, artist, includeFeatureOn=True)


def crawlAlbums(token, artists, artist, filterAlbums=True, includeFeatureOn=True):
    print('--------------------')
    print('Crawling Albums...')
    artistId = artists[artist]['artistId']
    #  Get artist albums
    allAlbums = getArtistAllAlbums(token, artistId)
    print('Total albums: ' + str(len(allAlbums)))
    # Write json to file
    with open('./files/albums/' + artist + '_albums_raw.json', 'w') as f:
        json.dump(allAlbums, f, ensure_ascii=False)

    # Filter albums type to album and single
    if filterAlbums:
        filterdAlbums = []
        for album in allAlbums:
            if album['album_type'] == 'album' or album['album_type'] == 'single':
                if not includeFeatureOn:
                    if album['album_group'] != 'appears_on':
                        filterdAlbums.append(album)
                else:
                    filterdAlbums.append(album)
        print('Filtered albums:', str(len(filterdAlbums)), '(albumtype=album|single' +
              (')' if includeFeatureOn else ' & album_group!=appears_on)'))
    else:
        filterdAlbums = allAlbums
    # Sort albums by release date
    filterdAlbums = sorted(
        filterdAlbums, key=lambda album: album['release_date'])
    # Write json to file
    with open('./files/albums/' + artist + '_albums.json', 'w') as f:
        json.dump(filterdAlbums, f, ensure_ascii=False)

    # Process albums
    count = 0
    # albumFile = open('./files/albums/' + artist + '_albums.txt', 'w')
    albumCsvFile = open('./files/albums/' + artist + '_albums.csv', 'w')
    print('AlbumName', 'AlbumId', 'AlbumGroup', 'AlbumType',
          'ReleaseDate', 'TracksNum', 'Artists', sep=', ', file=albumCsvFile)
    for album in filterdAlbums:
        count = count + 1
        albumName = album['name']
        albumId = album['id']
        albumGroup = album['album_group']
        albumType = album['album_type']
        releaseDate = album['release_date']
        tracksNum = str(album['total_tracks'])
        albumArtistsList = list(
            map(lambda artist: artist['name'], album['artists']))
        artists = '，'.join(albumArtistsList)
        # seperation = '--------------------'
        # print(seperation, str(count) + ': ' + albumName, 'Id: ' + albumId, 'Group: ' + albumGroup,
        #       'Type:  ' + albumType, 'Date:  ' + releaseDate, 'Tracks: ' + tracksNum, 'Artists: ' + artists, sep='\n')
        # print(seperation, albumName, albumId, albumGroup, albumType,
        #       releaseDate, tracksNum, artists, sep='\n', file=albumFile)
        print(re.sub(r'\,', '，', albumName), albumId, albumGroup, albumType,
              releaseDate, tracksNum, artists, sep=', ', file=albumCsvFile)
    # albumFile.close()
    albumCsvFile.close()

    print('--------------------')
    print('Album Statistic:', len(allAlbums))
    albumGroupStat = dict()
    albumTypeStat = dict()
    albumGroupTypeStat = dict()
    for t in allAlbums:
        albumGroup = 'AlbumGroup: ' + t['album_group']
        if albumGroup not in albumGroupStat:
            albumGroupStat[albumGroup] = 1
        else:
            albumGroupStat[albumGroup] = albumGroupStat[albumGroup] + 1
        albumType = 'AlbumType: ' + t['album_type']
        if albumType not in albumTypeStat:
            albumTypeStat[albumType] = 1
        else:
            albumTypeStat[albumType] = albumTypeStat[albumType] + 1
        albumGroupType = albumType + ', ' + albumGroup
        if albumGroupType not in albumGroupTypeStat:
            albumGroupTypeStat[albumGroupType] = 1
        else:
            albumGroupTypeStat[albumGroupType] = albumGroupTypeStat[albumGroupType] + 1
    print(json.dumps(albumGroupStat))
    print(json.dumps(albumTypeStat))
    print(json.dumps(albumGroupTypeStat))
    return filterdAlbums


if __name__ == '__main__':
    main()
