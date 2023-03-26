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
# Read parameters from command line
if len(sys.argv) >= 2:
    artistToCrawlList = sys.argv[1:]


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
    # Get artist albums
    allAlbums = getArtistAllAlbums(token, artistId)
    print('Total albums: ' + str(len(allAlbums)))
    # Write json to file
    with open('./files/albums/' + artist + '_albums_raw.json', 'w') as f:
        json.dump(allAlbums, f, ensure_ascii=False)
    # with open('./files/albums/' + artist + '_albums_raw.json') as f:
    #     allAlbums = json.load(f)
    # Only US market
    allAlbums = [album for album in allAlbums
                 if 'US' in album['available_markets']]
    print('Total albums(US): ' + str(len(allAlbums)))

    # Filter albums type to album and single
    filterdAlbums = []
    for album in allAlbums:
        if artists[artist].get('excludeAlbums') != None and \
                album['id'] in artists[artist]['excludeAlbums'].keys():
            continue
        if artists[artist].get('includeAlbums') != None and \
                album['id'] in artists[artist]['includeAlbums'].keys():
            filterdAlbums.append(album)
            continue
        if filterAlbums:
            if album['album_type'] == 'album' or album['album_type'] == 'single':
                if not includeFeatureOn:
                    if album['album_group'] != 'appears_on':
                        filterdAlbums.append(album)
                else:
                    filterdAlbums.append(album)
        else:
            filterdAlbums.append(album)
    filterRule = 'None' if not filterAlbums else 'albumtype=album|single' + \
        ('' if includeFeatureOn else ' & album_group!=appears_on')
    print('Filtered albums:', str(len(filterdAlbums)),
          '(filter: ' + filterRule + ')')

    # Request includeAlbums
    if artists[artist].get('includeAlbums') != None:
        filterdAlbumIds = {album['id'] for album in filterdAlbums}
        for albumId in artists[artist]['includeAlbums'].keys():
            if albumId in filterdAlbumIds:
                continue
            album = getSingleAlbum(token, albumId)
            filterdAlbums.append(album)

    # Sort albums by release date
    filterdAlbums.sort(key=lambda album: (
        album['release_date'], album['name']))
    # Write json to file
    with open('./files/albums/' + artist + '_albums.json', 'w') as f:
        json.dump(filterdAlbums, f, ensure_ascii=False)

    # Process albums
    count = 0
    # albumFile = open('./files/albums/' + artist + '_albums.txt', 'w')
    albumCsvFile = open('./files/albums/' + artist + '_albums.csv', 'w')
    print('AlbumName', 'AlbumId', 'AlbumType', 'AlbumGroup',
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
        # print(seperation, albumName, albumId, albumType, albumGroup,
        #       releaseDate, tracksNum, artists, sep='\n', file=albumFile)
        print(re.sub(r'\,', '，', albumName), albumId, albumType, albumGroup,
              releaseDate, tracksNum, artists, sep=', ', file=albumCsvFile)
    # albumFile.close()
    albumCsvFile.close()

    print('--------------------')
    print('Album Statistic:', len(allAlbums))
    albumGroupStat = dict()
    albumTypeStat = dict()
    albumTypeGroupStat = dict()
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
        albumTypeGroup = albumType + ', ' + albumGroup
        if albumTypeGroup not in albumTypeGroupStat:
            albumTypeGroupStat[albumTypeGroup] = 1
        else:
            albumTypeGroupStat[albumTypeGroup] = albumTypeGroupStat[albumTypeGroup] + 1
    print(json.dumps(albumTypeStat))
    print(json.dumps(albumGroupStat))
    print(json.dumps(albumTypeGroupStat))
    return filterdAlbums


if __name__ == '__main__':
    main()
