from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken
from artists import artists, artistToCrawl
from spotifyFunc import *
from crawlAlbums import crawlAlbums
from crawlRawTracks import getAllAlbumsTracks
from processTracks import processTracks

# ****************************************
#   Crawl spotify artist albums & tracks
# ****************************************


# Define artist here
artist = artistToCrawl
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


if artist in {'beyond', 'kare_mok'}:
    mustMainArtist = True
# Get all albums
token = getAccessToken(clientID, clientSecret)
allAlbums = crawlAlbums(token, artists, artist)
# Get all albums tracks
allAlbumsTracks = getAllAlbumsTracks(spotifyToken, artist, allAlbums)
# Process tracks
processTracks(artists, artist, allAlbumsTracks,
              mustMainArtist=mustMainArtist, filterTrackByName=False, printInfo=True)
print('--------------------')
print('Done!')
