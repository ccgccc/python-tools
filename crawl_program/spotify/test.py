import os
import re
import sys
import json
import time
from utils.auth import getAccessToken, getAuthorizationToken
from utils.secrets import clientID, clientSecret
from artists import *
from spotifyFunc import *
from playlistRemoveItems import playlistRemoveAllItems
from crawlPlaylists import crawlSinglePlaylist


# =====
def main():
    # getArtistsFisrtAlbum()
    # printArtistsJson()
    # topPlayTracks()
    # countTracks()
    # getDiffTracks()
    # addPlaylistTracks()
    # addPlaylistDiffTracks()
    playlistResetTracks()
    # unSaveTracks()
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
    notCountArtists = []
    for file in files:
        artist = file.replace('_albums.json', '')
        if artists.get(artist) == None:
            notCountArtists.append(artist)
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
    print('Not count:', notCountArtists)
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


# === Get top play tracks by crawled Chinese artists
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


# === Count total tracks of all generated playlists
def countTracks():
    artistNames = list(reversed([artistInfo['name']
                                 for artist, artistInfo in generateArtists.items()]))
    # Generated playlists
    mypath = './files/playlists/generated_playlists_info/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f)) and f.endswith('.json')]
    files.sort(key=lambda file: artistNames.index(
        re.sub(".*playlist_(.*) Most.*", r'\1', file)))
    # Collections
    mypath2 = './files/playlists/'
    files2 = [mypath2 + f for f in os.listdir(mypath2)
              if os.path.isfile(os.path.join(mypath2, f)) and f.endswith('.json')
              and (f.find('Collection') > 0  # or f.find('Hit') > 0
                   or f.find('张学友') > 0 or f.find('周杰伦') > 0)]
    files2.sort()
    files.extend(files2)
    # Get all tracks
    allTracks = set()
    count = 0
    for file in files:
        with open(file) as f:
            playlist = json.load(f)
        tracksNum = len(playlist['tracks']['items'])
        count = count + tracksNum
        print(re.sub(".*playlist_(.*)_by ccg ccc\.json", r'\1', file) +
              ':  ' + str(tracksNum) + '  (Acc:' + str(count) + ')')
        allTracks = allTracks | {track['track']['id']
                                 for track in playlist['tracks']['items']}
    # plus 好歌拾遗
    playlistId = '4qaMezDPYbUUCUaKVuOa44'
    accessToken = getAccessToken(clientID, clientSecret)
    playlist = getPlaylistAndAllTracks(accessToken, playlistId)
    tracksNum = len(playlist['tracks']['items'])
    count = count + tracksNum
    print('好歌拾遗: ' + str(tracksNum) + '  (Acc:' + str(count) + ')')
    allTracks = allTracks | {track['track']['id']
                             for track in playlist['tracks']['items']}
    print('All: ', len(allTracks))
    return allTracks


# Get diff tracks
def getDiffTracks():
    # Get artirts all tracks
    allTracks = countTracks()
    # Get playlist songs
    print('--------------------')
    playlists = {
        "Listening Artist": '2R48aLSO7QmOaHAGaV0zIM',
        "Favorite": "7J6PrVFDlPWiQe0m6NF2ie",
        "Like": "2QBH6yCLDJhTiXKqDfCtOA",
        "Nice": '4SqLcwtjZJXdkH8twICyOa'
    }
    trackItems = []
    totalTrack = 0
    for playlistName, playlistId in playlists.items():
        with open('files/playlists/playlist_' + playlistName + '_by ccg ccc.json') as f:
            playlist = json.load(f)
        curTrackItems = playlist['tracks']['items']
        trackItems.extend(curTrackItems)
        totalTrack = totalTrack + len(curTrackItems)
        print(playlistName + ':', len(curTrackItems))
    print('Playlists total:', totalTrack)

    # Get artists diff tracks
    filterArtist = False
    artist = 'eason_chan'
    # filterArtist = True
    diffTrackIds = set()
    count = 0
    for trackItem in trackItems:
        track = trackItem['track']
        album = trackItem['track']['album']
        if filterArtist and track['artists'][0]['id'] != artists[artist]['artistId']:
            continue
        if track['id'] in allTracks or track['id'] in diffTrackIds:
            continue
        count = count + 1
        diffTrackIds.add(track['id'])
        trackArtists = '/'.join(list(
            map(lambda artist: artist['name'], track['artists'])))
        print((str(count) + ':\t' + track['id'] + ',\t' + track['name'] +
               ',  ' + trackArtists + ',  ' + album['name'] + ',  ' + album['release_date']).expandtabs(4))
        # print(count, track['id'], track['name'], trackArtists, sep=', ')
    print('Diff track ids:')
    print(','.join(diffTrackIds))


# === Playlist add tracks
def addPlaylistTracks():
    # spotifyPlaylistId = '4lPnLfP0uTiEyfxlWW9eSu'  # 华语音乐TOP榜
    # spotifyPlaylistId = '4tJNCsjJQugmZwA72R2sJ0'  # Listening
    spotifyPlaylistId = '79YM0cmTgR3KPkAh3IXKGx'  # Favorite & Like
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
    accessToken = getAccessToken(clientID, clientSecret)
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)
    playlistRemoveAllItems(accessToken, spotify,
                           authorizeToken, spotifyPlaylistId, isPrivate=True)
    addTracksToPlayList(spotify, authorizeToken,
                        spotifyPlaylistId, trackUriList)


# === Playlist add diff tracks
def addPlaylistDiffTracks():
    spotifyPlaylistId = '2R48aLSO7QmOaHAGaV0zIM'  # Listening Artist
    accessToken = getAccessToken(clientID, clientSecret)
    # playlist 2 minus 1
    playlist1 = getPlaylistAndAllTracks(
        accessToken, '30snBIpQJ6Vu6kHPZOOR1A')  # 周杰伦 Most Played Songs
    playlist2 = getPlaylistAndAllTracks(
        accessToken, '7w3Y21vKZuLLq1huUuEWZZ')  # 周杰伦
    trackNames = {item['track']['name']
                  for item in playlist1['tracks']['items']}
    playlistOnlySongs = []
    for item in playlist2['tracks']['items']:
        if item['track']['name'] not in trackNames:
            playlistOnlySongs.append(
                {item['track']['id']: item['track']['name']})
    print('All:', len(playlistOnlySongs))
    print(playlistOnlySongs)
    trackUriList = ['spotify:track:' + str(list(dict.keys())[0])
                    for dict in playlistOnlySongs]
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


def playlistResetTracks():
    artist = 'zhengjun'

    resetPlaylistNames = [
        "Favorite",
        "Like",
        "Nice"
    ]

    mustMainArtist = True

    isCollection = False
    isCollection = True
    collection = 'Collection 1'

    # Get artist all tracks
    print('--------------------')
    if not isCollection:
        playlistNames = [
            artists[artist]['name'] + ' Most Played Songs',
            '好歌拾遗'
        ]
    else:
        playlistNames = [
            collection,
            '好歌拾遗'
        ]

    allTrackIds = set()
    count = 0
    for playlistName in playlistNames:
        if not isCollection:
            try:
                with open('files/playlists/playlist_' + playlistName + '_by ccg ccc.json') as f:
                    playlist = json.load(f)
            except:
                with open('files/playlists/generated_playlists_info/playlist_' + playlistName + '_by ccg ccc.json') as f:
                    playlist = json.load(f)
        else:
            with open('files/playlists/playlist_' + collection + '_by ccg ccc.json') as f:
                playlist = json.load(f)
        tracksNum = len(playlist['tracks']['items'])
        count = count + tracksNum
        print(re.sub(".*playlist_(.*)_by ccg ccc\.json", r'\1', playlistName) +
              ':  ' + str(tracksNum) + '  (Acc:' + str(count) + ')')
        allTrackIds = allTrackIds | {track['track']['id']
                                     for track in playlist['tracks']['items']}
    print('All tracks:', len(allTrackIds))

    spotify = None
    authorizeToken = None
    # Get artist playlist tracks
    for resetPlaylistName in resetPlaylistNames:
        print('--------------------')
        print('Playlist:', resetPlaylistName, '\n')
        with open('files/playlists/playlist_' + resetPlaylistName + '_by ccg ccc.json') as f:
            playlist = json.load(f)
            spotifyPlaylistId = playlist['id']
        artistTracks = []
        for trackItem in playlist['tracks']['items']:
            if mustMainArtist:
                if trackItem['track']['artists'][0]['id'] == artists[artist]['artistId']:
                    artistTracks.append({trackItem['track']['id']: trackItem['track']['name'] +
                                        '(' + '/'.join([artist['name'] for artist in trackItem['track']['artists']]) + ')'})
            else:
                for trackArtist in trackItem['track']['artists']:
                    if trackArtist['id'] == artists[artist]['artistId']:
                        artistTracks.append({trackItem['track']['id']: trackItem['track']['name'] +
                                            '(' + '/'.join([artist['name'] for artist in trackItem['track']['artists']]) + ')'})
                        continue
        print('Artist tracks:', len(artistTracks))
        print(artistTracks)

        # In playlist tracks
        artistInPlaylistsTracks = list(filter(
            lambda dict: list(dict.keys())[0] in allTrackIds, artistTracks))
        # artistInPlaylistsTracks = [{'3ftmO1Cwbew497pFiWiyAH': '浮誇(陳奕迅)'}, {'6akVETVeqqPVvuBS5e0EB1': '孤勇者 - 《英雄聯盟:雙城之戰》動畫劇集中文主題曲(陳奕迅)'}]
        print('\nArtist in playlist tracks:', len(artistInPlaylistsTracks))
        print(artistInPlaylistsTracks)
        # Not in playlist tracks
        artistNotInPlaylistsTracks = list(filter(
            lambda dict: list(dict.keys())[0] not in allTrackIds, artistTracks))
        # artistNotInPlaylistsTracks = [{'6LLyiqMoNoex4Zu0ka4iF2': '唯一(王力宏)'}, {
        #     '2fzf7AWpYMsW5xMOEaPvWc': '好心分手 (feat. Leehom Wang)(盧巧音/王力宏)'}]
        print('\nArtist not in playlist tracks:',
              len(artistNotInPlaylistsTracks))
        print(artistNotInPlaylistsTracks)

        print('--------------------')
        sureCheck()
        scope = [
            "playlist-read-private",
            "playlist-modify-private",
            "playlist-modify-public"
        ]
        if spotify == None:
            spotify, authorizeToken = getAuthorizationToken(
                clientID, clientSecret, scope)
        accessToken = getAccessToken(clientID, clientSecret)
        artistInPlaylistsTrackUris = [
            'spotify:track:' + list(dict.keys())[0] for dict in artistInPlaylistsTracks]
        removePlayListTracks(spotify, authorizeToken,
                             spotifyPlaylistId, artistInPlaylistsTrackUris)
        # addTracksToPlayList(spotify, authorizeToken,
        #                     spotifyPlaylistId, artistInPlaylistsTrackUris)
        # for dict in artistInPlaylistsTracks:
        #     addTracksToPlayList(spotify, authorizeToken,
        #                         spotifyPlaylistId, ['spotify:track:' + list(dict.keys())[0]])
        #     time.sleep(1)

        # sys.exit()
        time.sleep(2)
        artistNotInPlaylistsTrackUris = [
            'spotify:track:' + list(dict.keys())[0] for dict in artistNotInPlaylistsTracks]
        removePlayListTracks(spotify, authorizeToken,
                             spotifyPlaylistId, artistNotInPlaylistsTrackUris)
        # addTracksToPlayList(spotify, authorizeToken,
        #                     spotifyPlaylistId, artistNotInPlaylistsTrackUris)

        crawlSinglePlaylist(accessToken, spotifyPlaylistId,
                            './files/playlists/', spotify=spotify)


def unSaveTracks():
    trackIds = ['0RUGuh2uSNFJpGMSsD1F5C', '1wVuPmvt6AWvTL5W2GJnzZ', '4rmPQGwcLQjCoFq5NrTA0D', '4lLtanYk6tkMvooU0tWzG8',
                '2woOC3CRkSj2Mac0mazL7b', '5sYtvIl1mx9QuIgwC6FDU1', '7HQT2O80CCKp21UWD56xzh', '2bfchtbwde1S2PGsJ9uOyC']

    scope = [
        "user-library-modify"
    ]
    spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
    # API requests
    res = unSaveUserTracks(spotify, token, ','.join(trackIds))
    print(res, res.text)


# Check artist identifiers
def checkArtists():
    for artist, artistInfo in artists.items():
        if not re.match(r'^[a-z1-9_]+$', artist):
            if not artist.endswith('-2'):
                print(artistInfo['name'] + ': ' + artist + ' wrong.')
    print('All checked.')


def renameTrackSheets():
    mypath = './files/tracksheets/temp/'
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
