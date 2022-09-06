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
    'BQCZWMvIBHyif_pQSkiMgq6yQuO1l5OUqBPsLiNJ9gNBbirWdDlD7T2042AXNsFdYCTgNHHwkjVsh1k_RLs_1fYLYV1KT_NSWjMBdwMyDJ7CY--jz-xN94ezNt1AeBPowDNRsPvGX8wz4Ec4Jfn27EawsDt8BJjtic0RwDVr05TgoEsB643-qQwNH6ptHocNlcU5rc0WgQf-0pzrcvGc51efI-fua9usICMsM5omFRYJ9lSegwAPjwP1u_ACk1E_b1oKEz0YfapB6DhQML3_j91a3unq-Z_LOcm6WDsKsu8EIg8re7T_Lrs80rf8ctl8xqDorf-L0RdLEBypgLKYT54xpdmZ'
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

# Process tracks
processedTracks = processTracks(allTracks)
writeToXlsx(processedTracks, './files/' + artists[artist]['name'] +
            '_All Tracks_Generated on ' + time.strftime("%Y-%m-%d") + '.xlsx')
print('--------------------')
print('Done!')
