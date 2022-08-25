import json
from spotifyFunc import *
from artists import artists, artistToCrawl
from utils.secrets import clientID, clientSecret

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
    'BQC-P1vkbG4gjg1wyiMaX50QlzcxxwFq393bD7SHOlEjo6iXkppaO1ew9ibtQEA6ZTgFaE2xx-UXJ820_Wpm11HyELgS_rHpdHmK-w1ND4EhzyVZJNEiFC63Z6t14b7hbDZGzKA9tjD5z9QG4ywrZD0z_BUrWimq0geWM4s5pB3yWZBOkG8iij8VfM2zVCsO2HcWP_Hw_xRPNrpGxzXtfwBGDiZtKQqVlZglO6XvPSgs-pWK1lRt96VNkO5zd5xYILr-N0mdK4kwyLb6s3tG8yy5rFkVqszHXHHMkQiY4ddV4Ph5Vo2MaDqUT-d_rBsSa3TwrnzjFukALoinF-7Bu_4NmQo5'


# Get artist albums
artistId = artists[artist]['artistId']
token = getAccessToken(clientID, clientSecret)
allAblums = getArtistAllAlbums(token, artistId)
# Get all albums tracks
allTracks = []
albumCount = 0
# for album in allAblums[0:5]:
for album in allAblums:
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
    albumAlbumGroup = album['album_group']
    albumAlbumType = album['album_type']
    albumType = album['type']
    totalTracks = album['total_tracks']
    print(str(albumCount) + ': ' + albumName)
    print('Album Id: ' + albumId)
    print('Album Artist: ' + albumArtists)
    print('Release Date: ' + releaseDate)
    print('Total Tracks: ' + str(totalTracks))
    albumTracks = getAlbumTracksByThirdPartyAPI(
        spotifyToken, albumId)
    # print(albumTracks)
    trackCount = 0
    for track in albumTracks['data']['album']['tracks']['items']:
        trackCount = trackCount + 1
        trackUid = track['uid']
        trackUri = track['track']['uri']
        trackName = track['track']['name']
        trackPlaycount = track['track']['playcount']
        durationMs = track['track']['duration']['totalMilliseconds']
        duration = str(durationMs // 60000) + "m " + \
            "{:02d}".format(durationMs // 1000 % 60) + "s"
        playable = 'Y' if track['track']['playability']['playable'] == True else 'N'
        # concatenate artists & filter other artists
        artistsList = track['track']['artists']['items']
        containsArtist = False
        allArtists = ''
        for i in range(len(artistsList)):
            if artistsList[i]['uri'].find(artistId) >= 0:
                containsArtist = True
            allArtists = allArtists + artistsList[i]['profile']['name'] + \
                (', ' if i < len(artistsList) - 1 else '')
        if not containsArtist:
            continue
        print(str(trackCount) + ': ' + trackName + ", " + trackPlaycount)
        allTracks.append(
            {'trackUid': trackUid, 'trackUri': trackUri, 'trackName': trackName, 'artists': allArtists,
             'durationMs': durationMs, 'duration': duration, 'playcount': int(trackPlaycount), 'playable': playable,
             'albumId': albumId, 'albumName': albumName, 'albumArtists': albumArtists, 'releaseDate': releaseDate,
             'albumAlbumGroup': albumAlbumGroup, 'albumAlbumType': albumAlbumType, 'albumType': albumType, 'totalTracks': totalTracks})
# Sort all tracks by playcount
# allTracks = sorted(
#     allTracks, key=lambda track: track['playcount'], reverse=True)
# print(allTracks)

# Write json to file
with open('./files/' + artist + '_alltracks_raw.json', 'w') as f:
    json.dump(allTracks, f, ensure_ascii=False)
