from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken
from artists import *
from spotifyFunc import *
from crawlAlbums import crawlAlbums
from crawlRawTracks import getAllAlbumsTracks
from processTracks import processTracks

# ****************************************
#   Crawl spotify artist albums & tracks
# ****************************************

# Define artist here
artistToCrawlList = [artistToCrawl]
# Define if overwrite tracksheets
overwriteTrackSheets = False
if len(sys.argv) >= 2:
    overwriteTrackSheets = True
    if sys.argv[1] == 'generate':
        artistToCrawlList = list(generateArtists.keys())
        if len(sys.argv) > 2 and sys.argv[-1] == 'false':
            overwriteTrackSheets = False
    elif sys.argv[1] == 'other':
        artistToCrawlList = list(otherArtists.keys())
    elif sys.argv[1] == 'all':
        artistToCrawlList = list(artists.keys())
    else:
        artistToCrawlList = sys.argv[1:]
        if len(sys.argv) > 2 and sys.argv[-1] == 'false':
            overwriteTrackSheets = False
            artistToCrawlList = sys.argv[1:-1]

# Define if filter albums
filterAlbums = False
# Define must first artist
mustMainArtist = False
# Filter track by track name or not
filterTrackByName = False
# Spotify developer api doesn't provide track playcount info, so use spotify's own api to get it.
# This workaround needs getting an accesstoken from spotify web page.
# Token is retrived by spotify web page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa (最偉大的作品).
# Find https://api-partner.spotify.com/pathfinder/v1/query request (search 'query') and copy token from its authorization headers.
# Then paste it in utils/spotifyToken.txt.
spotifyToken = readFileContent('utils/spotifyToken.txt')


def main():
    for artist in artistToCrawlList:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Crawling ' + artists[artist]['name'] + '...')
        curFilterAlbums = filterAlbums if artists[artist].get(
            'filterAlbums') == None else artists[artist]['filterAlbums']
        curMustMainArtist = mustMainArtist if artists[artist].get(
            'mustMainArtist') == None else artists[artist]['mustMainArtist']
        curFilterTrackByName = filterTrackByName if artists[artist].get(
            'filterTrackByName') == None else artists[artist]['filterTrackByName']
        curOverwriteTrackSheets = True if artist in otherArtists else overwriteTrackSheets
        crawlAndProcess(artist, filterAlbums=curFilterAlbums, mustMainArtist=curMustMainArtist,
                        filterTrackByName=curFilterTrackByName, overwriteTrackSheets=curOverwriteTrackSheets)
    if len(artistToCrawlList) > 1:
        print('All Done!')


def crawlAndProcess(artist, filterAlbums=False, mustMainArtist=False, filterTrackByName=False, overwriteTrackSheets=False):
    # Get all albums
    token = getAccessToken(clientID, clientSecret)
    allAlbums = crawlAlbums(token, artists, artist,
                            filterAlbums=filterAlbums, includeFeatureOn=True)
    # Get all albums tracks
    allAlbumsTracks = getAllAlbumsTracks(
        spotifyToken, artist, allAlbums, simplePrint=True)
    # Process tracks
    processTracks(artists, artist, allAlbumsTracks, mustMainArtist=mustMainArtist,
                  filterTrackByName=filterTrackByName, overwriteTrackSheets=overwriteTrackSheets, printInfo=True)
    print('--------------------')
    print('Done!')


if __name__ == '__main__':
    main()
