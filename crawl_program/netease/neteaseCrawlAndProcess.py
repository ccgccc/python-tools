from artists import *
from common import *
from getArtistAlbums import crawlAlbums
from getAlbumsSongs import getAlbumsSongs
from processSongs import processSongs

# ****************************************
#   Crawl netease artist albums & tracks
# ****************************************

# Define artists here
artistToCrawlList = [artistToCrawl]
# artistToCrawlList = list(artists.keys())
# artistToCrawlList = list(generateArtists.keys())
# artistToCrawlList = list(otherArtists.keys())


for artist in artistToCrawlList:
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Crawling ' + artists[artist]['name'] + '...')
    # Get artist all albums
    allAlbums = crawlAlbums(artists, artist)
    # Get all albums songs & write to file
    allSongs = getAlbumsSongs(artist, allAlbums)
    # Process songs
    allSongs = processSongs(artist, allSongs)
    print('--------------------')
    print('Done!')

if len(artistToCrawlList) > 1:
    print('All Done!')
