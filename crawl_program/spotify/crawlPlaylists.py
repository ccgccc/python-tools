import re
import json
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from spotifyFunc import *

# ******************************
#    Crawl spotify playlists
# ******************************

# Define isPrivate & public playlist ids here
isPrivate = False
playlistIds = [
    # "7J6PrVFDlPWiQe0m6NF2ie",  # Favorite
    # "2QBH6yCLDJhTiXKqDfCtOA",  # Like
    # '4SqLcwtjZJXdkH8twICyOa',  # Nice
    "6Ev0ju4qLsqSLznN7fjErt",  # 张学友
    "7w3Y21vKZuLLq1huUuEWZZ",  # 周杰伦
    # "4DLB8que4WlMKhdg96wrvh",  # 五月天 Most Played Songs
]

# Define isPrivate & private playlist ids here
# isPrivate = True
# playlistIds = [
#     # '1cd55XqNdveVHn8DUJRJM1',  # To Listen
#     # '2UuyNeehZW9HQXhTkmFKBj',  # Netease Liked
#     '2R48aLSO7QmOaHAGaV0zIM'  # Listening Artist
# ]

# Define if simple print
simplePrint = True


def main():
    token = getAccessToken(clientID, clientSecret)
    playlistDir = './files/playlists/'
    crawlPlaylists(token, playlistIds, playlistDir, isPrivate=isPrivate)


def crawlPlaylists(token, playlistIds, playlistDir, isPrivate=False):
    for playlistID in playlistIds:
        crawlSinglePlaylist(token, playlistID, playlistDir,
                            isPrivate=isPrivate)


def crawlSinglePlaylist(token, playlistID, playlistDir, isPrivate=False):
    # API request
    if isPrivate:
        scope = "playlist-read-private"
        spotify, authorizeToken = getAuthorizationToken(
            clientID, clientSecret, scope)
        playlist = getPlaylistAndAllTracks(
            token, playlistID, isPrivate, spotify)
    else:
        playlist = getPlaylistAndAllTracks(token, playlistID, isPrivate)
    fileName = playlistDir + 'playlist_' + \
        playlist['name'] + '_by ' + playlist['owner']['display_name']
    # Write json to file
    with open(fileName + '.json', 'w') as f:
        json.dump(playlist, f, ensure_ascii=False)
    # Write playlist tracks to csv file
    csvFileName = fileName + '.csv'
    writeToCsvFile(playlist['tracks']['items'],
                   csvFileName, simplePrint=simplePrint)


def writeToCsvFile(trackItems, csvFileName, simplePrint=False):
    with open(csvFileName, 'w') as f:
        f.write('Track Id, Track, Artists, Album, Album Artist, Release Date\n')
    file = open(csvFileName, 'a')
    count = 0
    for item in trackItems:
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


if __name__ == '__main__':
    main()
