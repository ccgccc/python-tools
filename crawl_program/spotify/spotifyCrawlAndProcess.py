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
if len(sys.argv) >= 2:
    if sys.argv[1] == 'generate':
        artistToCrawlList = list(generateArtists.keys())
    if sys.argv[1] == 'other':
        artistToCrawlList = list(otherArtists.keys())
    elif sys.argv[1] == 'all':
        artistToCrawlList = list(artists.keys())
    else:
        artistToCrawlList = [sys.argv[1]]

# Define if filter albums
filterAlbums = True
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
        if artist in {'eason_chan', 'suyunying'}:
            filterAlbums = False
        else:
            filterAlbums = True
        if artist in {'beyond', 'kare_mok'}:
            mustMainArtist = True
        else:
            mustMainArtist = False
        crawlAndProcess(artist, mustMainArtist,
                        filterAlbums, filterTrackByName)
    if len(artistToCrawlList) > 1:
        print('All Done!')


def crawlAndProcess(artist, mustMainArtist, filterAlbums=False, filterTrackByName=False):
    # Get all albums
    token = getAccessToken(clientID, clientSecret)
    allAlbums = crawlAlbums(token, artists, artist, filterAlbums=filterAlbums)
    # Get all albums tracks
    allAlbumsTracks = getAllAlbumsTracks(spotifyToken, artist, allAlbums)
    # Process tracks
    processTracks(artists, artist, allAlbumsTracks,
                  mustMainArtist=mustMainArtist, filterTrackByName=filterTrackByName, printInfo=True)
    print('--------------------')
    print('Done!')


if __name__ == '__main__':
    main()
