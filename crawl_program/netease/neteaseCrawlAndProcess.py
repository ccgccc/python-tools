from artists import *
from common import *
from getArtistAlbums import crawlAlbums
from getAlbumsSongs import getAlbumsSongs
from processSongs import processSongs

# ****************************************
#   Crawl netease artist albums & tracks
# ****************************************


# Get artist all albums
allAlbums = crawlAlbums(artists, artistToCrawl)

# Get all albums songs & write to file
allSongs = getAlbumsSongs(allAlbums)

# Process songs
allSongs = processSongs(allSongs)

print('--------------------')
print('Done!')
