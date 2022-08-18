import json
from albumFunc import *
from secrets import *

# ******************************
#  Crawl spotify artist tracks
# ******************************

# Define artist id here
artistId = "2QcZxAgcs2I1q7CtCkl6MI"  # Eson Chan
# Token is retrived by spotify page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa,
# find https://api-partner.spotify.com/pathfinder/v1/query request and copy from its authorization header
spotifyToken = "BQDYCCxdzAWoHqQOsaEHiZWTplar8zwTl7_MKTMwfwZgcIDgWXX5f5cX5b6y4xLZHx33EG2Fl5rk4iUrgpTtYCRw9AL6DSeqDRK9SNZeqSVv3MXlNbQ-uL3iHtISUZgL5hOh8IL7XPJJMBgEIaqLAreJwPea875tMfm1v1eCUjYE2tNMUKRj0yuu2pwHGvggnhE8uFX-MiI9xndQ95c5xSUO45pj2G4-8r8ptLoDU7MZhOo7osn_Ww08mr9kCvmvz-9zck6_3WGBDE9oKQv2VsnS7QdoCCj0JJS721R5e3DtJ3tr34BEHS71198Ph6Z5saqC3Vpf_OoZkT5J-gYd1kk1WD6R"

allAblums = getArtistAllAlbums(artistId)

# Simple Output
albumCount = 0
for album in allAblums[0:10]:
    print('--------------------')
    albumCount = albumCount + 1
    print(str(albumCount) + ': ' + album['name'])
    print('AlbumId: ' + album['id'])
    print('Date: ' + album['release_date'])
    print('Tracks: ' + str(album['total_tracks']))
    albumTracks = getAlbumTracksByThirdPartyAPI(
        spotifyToken, album['id'])
    # print(albumTracks)
    trackCount = 0
    for track in albumTracks['data']['album']['tracks']['items']:
        trackCount = trackCount + 1
        print(str(trackCount) + ': ' + track['track']['name'] + ", " + track['track']['playcount'])

# # Get album tracks by spotify developer api, but this doesn't have play count info
# token = getAccessToken(clientID, clientSecret)
# limit = 50
# # albumTracks = getAlbumTracks(token, allAblums[0]['id'], limit, 0)
# # print(albumTracks)
# # Write json to file
# # with open('albumTracks.json', 'w') as f:
# #     json.dump(albumTracks, f)
# allTracks = []
# for album in allAblums[0:10]:
#     albumTracks = getAlbumTracks(token, album['id'], limit, 0)
#     # print(albumTracks)
#     print('--------------------')
#     print('Album: ' + album['name'] + ' (' + album['release_date'] + ')')
#     i = 0
#     for track in albumTracks['items']:
#         i = i + 1
#         print(str(i) + ': ' + track['name'])
#         # print('Id: ' + t['id'])
#         # print('Date: ' + t['release_date'])
#         # print('Tracks: ' + str(t['total_tracks']))
#         # not necessary, album info already has track info
#         track = getSingleTrack(token, track['id'])
#         allTracks.append(track)

# # Write json to file
# with open('allTracks.json', 'w') as f:
#     json.dump(allTracks, f)
