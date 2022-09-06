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
# Spotify developer api doesn't provide track playcount info, so use spotify's own api to get it.
# This workaround needs getting an accesstoken from spotify web page.
# Token is retrived by spotify web page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa (最偉大的作品).
# Find https://api-partner.spotify.com/pathfinder/v1/query request (search 'query') and copy token from its authorization headers.
spotifyToken = \
    'BQBCI_Wi0kIuvZy-SZbcrTtJUNueQMmX3IKfRXPAOERFI1N2Sdf9t4vYBq6LTok6oIY-T_MLCuTAGIJCwLmshcQ1NI7vGxJ6DFl694GShPe9zybB6bvdHyb5nWhgFPZODfEcKstT9gVDHGHcyBMrStTD32FKl0NO6Uu6xK3fV3iV8sq502KKM-ZqrpPQJXZpnl3TpD4jRpVThj0kel3NDMFpkO1lHtTtyuDlR2j0VCuLD1xlsKOHko9kYbEsgcU3S4P2OWO8ZzEgrh3aLz4TI7wmC9VtGBwuk9roS1bsL7kyqqVXvd9ZiWp4Rt_WDc_2gzVGWALPX6_to6-By-WbjRPsFqGP'
# Filter track by track name or not
filterTrackByName = False


# Get artist albums
artistId = artists[artist]['artistId']
allAblums = []
with open('./files/albums/' + artist + '_albums.json') as f:
    allAblums = json.load(f)
# token = getAccessToken(clientID, clientSecret)
# allAblums = getArtistAllAlbums(token, artistId)

# Get all albums tracks
allTracks = getAllTracks(spotifyToken, artistId, allAblums)
# Write json to file
with open('./files/tracks/' + artist + '_alltracks_raw.json', 'w') as f:
    json.dump(allTracks, f, ensure_ascii=False)

# Process tracks
processedTracks = processTracks(allTracks)
writeToXlsx(processedTracks, './files/' + artists[artist]['name'] +
            '_All Tracks_Generated on ' + time.strftime("%Y-%m-%d") + '.xlsx')
print('--------------------')
print('Done!')
