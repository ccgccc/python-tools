import json
import re
from utils.secrets import clientID, clientSecret
from spotifyFunc import *

# ******************************
#    Crawl spotify playlist
# ******************************

# Define playlist id here
# playlistID = "7J6PrVFDlPWiQe0m6NF2ie"  # Favorite
playlistID = "2QBH6yCLDJhTiXKqDfCtOA"  # Like
# playlistID = "1zIsw5K3WfUq3lcadhqA8n"  # 邓紫棋 Most Played Songs
# playlistID = "6Ev0ju4qLsqSLznN7fjErt"  # 张学友
# playlistID = "7w3Y21vKZuLLq1huUuEWZZ"  # 周杰伦


def main():
    # API requests
    token = getAccessToken(clientID, clientSecret)
    playlist = getPlaylistAndAllTracks(token, playlistID)

    fileName = './files/playlists/playlist_' + \
        playlist['name'] + '_by ' + playlist['owner']['display_name']
    # Write json to file
    with open(fileName + '.json', 'w') as f:
        json.dump(playlist, f, ensure_ascii=False)
    # Write playlist tracks to csv file
    csvFileName = fileName + '.csv'
    writeToCsvFile(playlist['tracks']['items'], csvFileName)


def writeToCsvFile(trackItems, csvFileName):
    with open(csvFileName, 'w') as f:
        f.write('Track Id, Track, Artists, Album, Album Artist, Release Date\n')
    file = open(csvFileName, 'a')
    count = 0
    for item in trackItems:
        print('--------------------')
        count = count + 1
        print(str(count))
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
        print('Track:   ' + trackName)
        print('Album:   ' + albumName + ' (' + releaseDate + ")")
        print('Artists: ' + trackArtists)
        file.write(trackId + ', ' + re.sub(r'\,', '，', trackName) + ', ' + trackArtists + ', '
                   + re.sub(r'\,', '，', albumName) + ', ' + albumArtists + ', ' + releaseDate + '\n')
    file.close()


if __name__ == '__main__':
    main()
