import json
from utils.secrets import clientID, clientSecret
from artists import artists, artistToCrawl
from spotifyFunc import *

# ******************************
#  Crawl spotify artist tracks
# ******************************

# Define artist to crawl here
artistToCrawlList = [artistToCrawl]
# Crawl all artists
# artistToCrawlList = artists.keys()
# Spotify developer api doesn't provide track playcount info, so use spotify's own api to get it.
# This workaround needs getting an accesstoken from spotify web page.
# Token is retrived by spotify web page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa (最偉大的作品).
# Find https://api-partner.spotify.com/pathfinder/v1/query request (search 'query') and copy token from its authorization headers.
# Then paste it in utils/spotifyToken.txt.
spotifyToken = readFileContent('utils/spotifyToken.txt')


def main():
    for artist in artistToCrawlList:
        print('--------------------')
        print('Processing ' + artists[artist]['name'] + '...')
        crawlRawTracks(spotifyToken, artist)


def crawlRawTracks(spotifyToken, artist):
    # Get artist albums
    allAlbums = []
    with open('./files/albums/' + artist + '_albums.json') as f:
        allAlbums = json.load(f)
    # token = getAccessToken(clientID, clientSecret)
    # allAlbums = getArtistAllAlbums(token, artistId)

    # Get all tracks & write to file
    allTracks = getAllAlbumsTracks(spotifyToken, artist, allAlbums)
    return allTracks


def getAllAlbumsTracks(spotifyToken, artist, allAlbums):
    # Get all albums tracks
    allTracks = []
    albumCount = 0
    allAlbumTracks = []
    for album in allAlbums:
        print('--------------------')
        albumCount = albumCount + 1
        albumId = album['id']
        albumName = album['name']
        albumArtistsList = album['artists']
        albumArtists = ''
        for i in range(len(albumArtistsList)):
            albumArtists = albumArtists + albumArtistsList[i]['name'] + \
                (', ' if i < len(albumArtistsList) - 1 else '')
        releaseDate = album['release_date']
        totalTracks = album['total_tracks']
        print(str(albumCount) + ': ' + albumName)
        print('Album Id: ' + albumId)
        print('Album Artist: ' + albumArtists)
        print('Release Date: ' + releaseDate)
        print('Total Tracks: ' + str(totalTracks))
        albumTracks = getAlbumTracksByThirdPartyAPI(
            spotifyToken, albumId)
        albumTracks = albumTracks['data']['album']
        albumTracks['album'] = album
        allAlbumTracks.append(albumTracks)
    with open('./files/tracks/' + artist + '_alltracks_raw.json', 'w') as f:
        json.dump(allAlbumTracks, f, ensure_ascii=False)
    return allTracks


if __name__ == '__main__':
    main()
