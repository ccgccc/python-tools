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
        crawlAlbums(artists, artist)


def crawlAlbums(artists, artist):
    artistId = artists[artist]['artistId']
    token = getAccessToken(clientID, clientSecret)
    #  Get artist albums
    allAblums = getArtistAllAlbums(token, artistId)
    # Write json to file
    with open('./files/albums/' + artist + '_albums.json', 'w') as f:
        json.dump(allAblums, f, ensure_ascii=False)

    # Process albums
    count = 0
    # albumFile = open('./files/albums/' + artist + '_albums.txt', 'w')
    albumCsvFile = open('./files/albums/' + artist + '_albums.csv', 'w')
    print('AlbumName', 'AlbumId', 'AlbumGroup', 'AlbumType',
          'ReleaseDate', 'TracksNum', 'Artists', sep=', ', file=albumCsvFile)
    for album in allAblums:
        seperation = '--------------------'
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
        # print(seperation, str(count) + ': ' + albumName, 'Id: ' + albumId, 'Group: ' + albumGroup,
        #       'Type:  ' + albumType, 'Date:  ' + releaseDate, 'Tracks: ' + tracksNum, 'Artists: ' + artists, sep='\n')
        # print(seperation, albumName, albumId, albumGroup, albumType,
        #       releaseDate, tracksNum, artists, sep='\n', file=albumFile)
        print(re.sub(r'\,', '，', albumName), albumId, albumGroup, albumType,
              releaseDate, tracksNum, artists, sep=', ', file=albumCsvFile)
    # albumFile.close()
    albumCsvFile.close()

    print('--------------------')
    print('Album Statistic:')
    albumGroupStat = dict()
    albumTypeStat = dict()
    albumGroupTypeStat = dict()
    for t in allAblums:
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
        albumGroupType = albumGroup + ', ' + albumType
        if albumGroupType not in albumGroupTypeStat:
            albumGroupTypeStat[albumGroupType] = 1
        else:
            albumGroupTypeStat[albumGroupType] = albumGroupTypeStat[albumGroupType] + 1
    print(albumGroupStat.items())
    print(albumTypeStat.items())
    print(albumGroupTypeStat.items())


if __name__ == '__main__':
    main()
