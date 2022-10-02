import json
import time
from utils.secrets import clientID, clientSecret
from artists import artists, artistToCrawl
from spotifyFunc import *
from crawlRawTracks import getAllTracks
from processTracks import processTracks, writeToXlsx

# ******************************
#  Crawl spotify artist tracks
# ******************************

# Define artist here
artist = artistToCrawl
# Filter track by track name or not
filterTrackByName = False
# Spotify developer api doesn't provide track playcount info, so use spotify's own api to get it.
# This workaround needs getting an accesstoken from spotify web page.
# Token is retrived by spotify web page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa (最偉大的作品).
# Find https://api-partner.spotify.com/pathfinder/v1/query request (search 'query') and copy token from its authorization headers.
# Then paste it in utils/spotifyToken.txt.
spotifyToken = readFileContent('utils/spotifyToken.txt')


# Get artist albums
artistId = artists[artist]['artistId']
allAlbums = []
with open('./files/albums/' + artist + '_albums.json') as f:
    allAlbums = json.load(f)
# token = getAccessToken(clientID, clientSecret)
# allAlbums = getArtistAllAlbums(token, artistId)

# Get all albums tracks
allTracks = getAllTracks(spotifyToken, artistId, allAlbums)

# Process tracks
processedTracks = processTracks(allTracks)
writeToXlsx(processedTracks, './files/' + artists[artist]['name'] +
            '_All Tracks_Generated on ' + time.strftime("%Y-%m-%d") + '.xlsx')
print('--------------------')
print('Done!')
