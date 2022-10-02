import json
from utils.secrets import clientID, clientSecret
from artists import artists, artistToCrawl
from spotifyFunc import *

# ******************************
#  Crawl spotify artist tracks
# ******************************

# Define artist here
artist = artistToCrawl
# Define must first artist
mustMainArtist = False
# Spotify developer api doesn't provide track playcount info, so use spotify's own api to get it.
# This workaround needs getting an accesstoken from spotify web page.
# Token is retrived by spotify web page, e.g. https://open.sqpotify.com/album/1rBr9FeLlp5ueSKtE89FZa (最偉大的作品).
# Find https://api-partner.spotify.com/pathfinder/v1/query request (search 'query') and copy token from its authorization headers.
# Then paste it in utils/spotifyToken.txt.
tokenFile = open('utils/spotifyToken.txt')
spotifyToken = tokenFile.read()
tokenFile.close()


def main():
    # Get artist albums
    artistId = artists[artist]['artistId']
    allAlbums = []
    with open('./files/albums/' + artist + '_albums.json') as f:
        allAlbums = json.load(f)
    # token = getAccessToken(clientID, clientSecret)
    # allAlbums = getArtistAllAlbums(token, artistId)

    # Get all tracks & write to file
    getAllTracks(spotifyToken, artistId, allAlbums, mustMainArtist)


def getAllTracks(spotifyToken, artistId, allAlbums, mustMainArtist=False):
    # Get all albums tracks
    allTracks = []
    albumCount = 0
    # for album in allAlbums[0:5]:
    for album in allAlbums:
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
            artistsList = track['track']['artists']['items']
            if mustMainArtist and artistsList[0]['uri'].find(artistId) < 0:
                continue
            # concatenate artists & filter other artists
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
    # Write json to file
    with open('./files/tracks/' + artist + '_alltracks_raw.json', 'w') as f:
        json.dump(allTracks, f, ensure_ascii=False)
    return allTracks


if __name__ == '__main__':
    main()
