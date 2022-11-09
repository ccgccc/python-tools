import os
import re
import copy
import json
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from spotifyFunc import *

# ******************************
#    Crawl spotify playlists
# ******************************

# Define playlistId:isPrivate here
playlistIDs = {
    "7J6PrVFDlPWiQe0m6NF2ie": False,  # Favorite
    "2QBH6yCLDJhTiXKqDfCtOA": False,  # Like
    '4SqLcwtjZJXdkH8twICyOa': False,  # Nice
    # '64s4sAZyFPc9v2siw2XdX7': True,  # Hmm
    # "6Ev0ju4qLsqSLznN7fjErt": False,  # 张学友
    # "7w3Y21vKZuLLq1huUuEWZZ": False,  # 周杰伦
    # "4DLB8que4WlMKhdg96wrvh": False,  # 五月天 Most Played Songs
    # '1cd55XqNdveVHn8DUJRJM1': True,  # To Listen
    # '2UuyNeehZW9HQXhTkmFKBj': True,  # Netease Non-playable
    # '2R48aLSO7QmOaHAGaV0zIM': True  # Listening Artist
}

# Define if simple print
simplePrint = True


def main():
    # Read parameters from command line
    os.chdir(os.path.dirname(__file__))
    if len(sys.argv) >= 2:
        playlistNames = sys.argv[1:]
        playlistIds = {}
        for playlistName in playlistNames:
            with open('./files/playlists/playlist_' + playlistName + '_by ccg ccc.json') as f:
                playlist = json.load(f)
                playlistIds[playlist['id']] = not playlist['public']
    else:
        playlistIds = playlistIDs
    # Playlist directory
    playlistDir = './files/playlists/'

    # API request
    if True in playlistIds.values():
        scope = "playlist-read-private"
        spotify, authorizeToken = getAuthorizationToken(
            clientID, clientSecret, scope)
    else:
        spotify = None
    accessToken = getAccessToken(clientID, clientSecret)
    crawlPlaylists(accessToken, playlistIds, playlistDir, spotify=spotify)


def crawlPlaylists(accessToken, playlistIds, playlistDir, isPrivate=False, spotify=None):
    allPlaylists = []
    mergedPlaylist = None
    for playlistID, isPrivate in playlistIds.items():
        curPlaylist = crawlSinglePlaylist(accessToken, playlistID, playlistDir,
                                          isPrivate=isPrivate, spotify=spotify)
        allPlaylists.append(curPlaylist)
        if mergedPlaylist == None:
            mergedPlaylist = copy.deepcopy(curPlaylist)
            mergedPlaylist['name'] = 'Merged_Playlist'
        else:
            mergedPlaylist['tracks']['items'].extend(
                curPlaylist['tracks']['items'])
    for playlist in allPlaylists:
        playlistStatistics(playlist)
    playlistStatistics(mergedPlaylist)


def crawlSinglePlaylist(accessToken, playlistID, playlistDir, isPrivate=False,
                        spotify=None, printPlaylist=True, simplePrint=True):
    # API request
    if isPrivate:
        playlist = getPlaylistAndAllTracks(
            accessToken, playlistID, isPrivate, spotify)
    else:
        playlist = getPlaylistAndAllTracks(accessToken, playlistID, isPrivate)
    fileName = playlistDir + 'playlist_' + \
        playlist['name'] + '_by ' + playlist['owner']['display_name']
    # Write json to file
    with open(fileName + '.json', 'w') as f:
        json.dump(playlist, f, ensure_ascii=False)
    # Write playlist tracks to csv file
    csvFileName = fileName + '.csv'
    writeToCsvFile(playlist, csvFileName,
                   printPlaylist=printPlaylist, simplePrint=simplePrint)
    return playlist


def writeToCsvFile(playlist, csvFileName, printPlaylist=True, simplePrint=True):
    with open(csvFileName, 'w') as f:
        f.write('Track Id, Track, Artists, Album, Album Artist, Release Date\n')
    file = open(csvFileName, 'a')
    if printPlaylist:
        print('----------------------------------------')
        print(playlist['name'] + ':')
    count = 0
    for item in playlist['tracks']['items']:
        count = count + 1
        # Album info
        album = item['track']['album']
        albumId = album['id']
        albumName = album['name']
        albumArtistsList = list(
            map(lambda artist: artist['name'], album['artists']))
        albumArtists = '，'.join(albumArtistsList)
        releaseDate = album['release_date']
        albumAlbumType = album['album_type']
        albumType = album['type']
        totalTracks = album['total_tracks']
        # Track info
        track = item['track']
        trackId = track['id']
        trackName = track['name']
        trackArtistsList = list(
            map(lambda artist: artist['name'], track['artists']))
        trackArtists = '，'.join(trackArtistsList)
        if printPlaylist:
            if simplePrint:
                print((str(count) + ':\t' + trackId + ',\t' + trackName +
                       ',  ' + releaseDate + ',  ' + albumName).expandtabs(5))
            else:
                print('----------')
                print(count)
                print('Track:   ' + trackName)
                print('Album:   ' + albumName + ' (' + releaseDate + ")")
                print('Artists: ' + trackArtists)
        file.write(trackId + ', ' + re.sub(r'\,', '，', trackName) + ', ' + trackArtists + ', '
                   + re.sub(r'\,', '，', albumName) + ', ' + albumArtists + ', ' + releaseDate + '\n')
    file.close()


def playlistStatistics(playlist):
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(playlist['name'] + ' Statistics:')
    playlistStats = {}
    for item in playlist['tracks']['items']:
        track = item['track']
        mainArtist = track['artists'][0]['name']
        if playlistStats.get(mainArtist) == None:
            playlistStats[mainArtist] = 1
        else:
            playlistStats[mainArtist] = playlistStats[mainArtist] + 1
    print(dict(sorted(playlistStats.items(),
          key=lambda item: item[1], reverse=True)))


if __name__ == '__main__':
    main()
