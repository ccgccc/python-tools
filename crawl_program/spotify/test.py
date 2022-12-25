import os
import re
import sys
import json
from utils.auth import getAccessToken, getAuthorizationToken
from utils.secrets import clientID, clientSecret
from artists import *
from spotifyFunc import *


# =====
def main():
    # getArtistsFisrtAlbum()
    printArtistsJson()
    # countTracks()
    # topPlayTracks()
    # playlistAddTracks()
    # checkArtists()
    # renameTrackSheets()
    # removeTrackFiles()


# === Get artist first album release date
def getArtistsFisrtAlbum(printInfo=True):
    # ********** Get artists first album **********
    mypath = './files/albums/'
    files = [f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f)) and f.endswith('_albums.json')]
    artistAlbums = []
    for file in files:
        artist = file.replace('_albums.json', '')
        if artists.get(artist) == None:
            continue
        with open(mypath + file) as f:
            albums = json.load(f)
        artistAlbums.append({'artist': artist, 'name': artists[artist]['name'],
                            'firstAlbum': albums[0]['name'], 'releaseDate': albums[0]['release_date']})
        # print(artist, artists[artist]['name'], albums[0]
        #     ['name'], albums[0]['release_date'], sep=', ')

    artistAlbums = sorted(artistAlbums, key=lambda album: album['releaseDate'])
    if not printInfo:
        return artistAlbums
    f = open('./files/artists/artist_debuts.csv', 'w')
    print('ReleaseDate', 'Artist', ' Identifier',
          'First Album Name', sep=', ', file=f)
    for artistAlbum in artistAlbums:
        print(artistAlbum['releaseDate'], artistAlbum['name'],
              artistAlbum['artist'], artistAlbum['firstAlbum'], sep=', ')
        print(artistAlbum['releaseDate'], artistAlbum['name'],
              artistAlbum['artist'], '"' + artistAlbum['firstAlbum'] + '"', sep=', ', file=f)
    f.close()
    return artistAlbums


def printArtistsJson():
    artistAlbums = getArtistsFisrtAlbum(printInfo=False)
    releaseDates = {artistAlbum['artist']: artistAlbum['releaseDate']
                    for artistAlbum in artistAlbums}
    count = 0
    generateArtistKeys = list(generateArtists.keys())
    # artistKeys = generateArtistKeys  # all
    artistKeys = generateArtistKeys[1:15]  # foreign
    # artistKeys = generateArtistKeys[54:76]  # hongkong
    # artistKeys = generateArtistKeys[76:143]  # mainland
    # artistKeys = generateArtistKeys[141:218]  # taiwan
    for artistKey in artistKeys:
        print(count, artists[artistKey]['name'],
              releaseDates[artistKey], sep=', ')
        count = count + 1
    artistKeys.sort(key=lambda x: releaseDates[x], reverse=True)
    print('--------------------')
    print('{')
    for artistKey in artistKeys:
        artistJson = \
            '    "' + artistKey + '": {\n' + \
            '        "name": "' + artists[artistKey]['name'] + '",  # ' + releaseDates[artistKey] + '\n' + \
            '        "artistId": "' + artists[artistKey]['artistId'] + '"\n' + \
            '    },'
        print(artistJson)
    print('}')


# === Count total tracks of all generated playlists
def countTracks():
    artistNames = list(reversed([artistInfo['name']
                                 for artist, artistInfo in generateArtists.items()]))
    mypath = './files/playlists/generated_playlists_info/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f)) and f.endswith('.json')]
    files.sort(key=lambda file: artistNames.index(
        re.sub(".*playlist_(.*) Most.*", r'\1', file)))
    mypath2 = './files/playlists/'
    files2 = [mypath2 + f for f in os.listdir(mypath2)
              if os.path.isfile(os.path.join(mypath2, f)) and f.endswith('.json')
              and (f.find('Collection') > 0 or f.find('Hit') > 0)]
    files2.sort()
    files.extend(files2)
    count = 0
    allTracks = set()
    for file in files:
        with open(file) as f:
            playlist = json.load(f)
        tracksNum = len(playlist['tracks']['items'])
        count = count + tracksNum
        print(re.sub(".*playlist_(.*)_by ccg ccc\.json", r'\1', file) +
              ':  ' + str(tracksNum) + '  (Acc:' + str(count) + ')')
        allTracks = allTracks | {track['track']['id']
                                 for track in playlist['tracks']['items']}
    print('All: ', len(allTracks))


# === Get top play tracks by crawled artists
def topPlayTracks():
    topCount = 100
    printTrackId = False
    notForeignArtists = {'Twins', 'Beyond'}

    allTopTracks = []
    allTopTrackIds = set()
    for artist, artistInfo in artists.items():
        artistName = artistInfo['name']
        if re.match(r'^[a-zA-Z .é]+$', artistName) and artistName not in notForeignArtists:
            #     print(artistName)
            #     continue
            # else:
            continue
        with open('./files/tracks/' + artist + '_alltracks.json') as f:
            allTracks = json.load(f)
        filteredTracks = [track for track in allTracks
                          if track['playcount'] >= 1000000 and track['trackUri'] not in allTopTrackIds]
        allTopTracks.extend(filteredTracks)
        allTopTrackIds = allTopTrackIds | {
            track['trackUri'] for track in filteredTracks}
        # print(artistName + ':', end=' ')
        # print([track['trackName'] + '(' + str(track['playcount']) + ')'
        #        for track in filteredTracks])
    # Sort
    allTopTracks.sort(key=lambda track: track['playcount'], reverse=True)
    # Filter by playcount
    filteredTopTracks = []
    prePlaycount = 0
    for track in allTopTracks:
        if track['playcount'] == prePlaycount:
            continue
        filteredTopTracks.append(track)
        prePlaycount = track['playcount']
    # Print
    filteredTopTracks = filteredTopTracks[:topCount]
    stats = {}
    i = 0
    print('--------------------')
    for track in filteredTopTracks:
        i = i + 1
        print(i, end=': ')
        print(track['trackName'], track['artists'], track['releaseDate'],
              format(track['playcount'], ','), sep=' ~~~ ')
        artistName = track['artists'].split(',')[0]
        if stats.get(artistName) == None:
            stats[artistName] = 1
        else:
            stats[artistName] = stats[artistName] + 1
    if printTrackId:
        print('--------------------', len(stats))
        print('All TrackIds:')
        print(','.join([track['trackUri'].replace('spotify:track:', '')
                        for track in filteredTopTracks]))
    print('--------------------', len(stats))
    print(stats)
    print('--------------------', len(stats))
    stats = [{k: v} for k, v in stats.items()]
    stats.sort(key=lambda dict: list(dict.values())[0], reverse=True)
    print(stats)


# === Playlist add tracks
def playlistAddTracks():
    spotifyPlaylistId = '4lPnLfP0uTiEyfxlWW9eSu'  # 华语粤语TOP榜
    trackIds = readFileContent('saveTracks.txt')
    trackUriList = ['spotify:track:' + trackId
                    for trackId in trackIds.split(',')]
    # print(trackUriList)
    print('All Tracks:', len(trackUriList))
    sureCheck()
    scope = [
        "playlist-read-private",
        "playlist-modify-private",
        "playlist-modify-public"
    ]
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)
    addTracksToPlayList(spotify, authorizeToken,
                        spotifyPlaylistId, trackUriList)


# Check artist identifiers
def checkArtists():
    for artist, artistInfo in artists.items():
        if not re.match(r'^[a-z1-9_]+$', artist):
            if not artist.endswith('-2'):
                print(artistInfo['name'] + ': ' + artist + ' wrong.')
    print('All checked.')


def renameTrackSheets():
    mypath = './files/trackSheets/temp/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f))]
    print('Renaming:')
    print(files)
    sureCheck()
    for file in files:
        print(file)
        print(file.replace('_Generated on 2022-11-30', ''))
        os.rename(file, file.replace('_Generated on 2022-11-30', ''))


def removeTrackFiles():
    artist = 'dicky_cheung2'
    mypath = './files/'
    files = [os.path.join(dirpath, f)
             for (dirpath, dirnames, filenames) in os.walk(mypath)
             for f in filenames if f.startswith(artist) or f.startswith(artists[artist]['name'])]
    print('Removing:')
    print(files)
    sureCheck()
    if len(files) > 0:
        sureCheck()
        for file in files:
            os.remove(file)


def sureCheck():
    msg = input('Are you sure? Press Y to continue: ')
    if msg != 'y' and msg != 'Y':
        sys.exit()


if __name__ == '__main__':
    main()
