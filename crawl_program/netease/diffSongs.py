from common import *
from countSongs import countSongs
from test import addPlaylistSongs

# ******************************
#   Get artists diff tracks
# ******************************


# Get artists diff tracks
# (playlists artist songs - all generated playlists songs)
filterArtist = False
# artist = 'stefanie_sun'
if len(sys.argv) >= 2:
    artist = sys.argv[1]
    filterArtist = True

mustMainArtist = False

toAddPlaylistId = 8167810670  # 好歌拾遗
# toAddPlaylistId = 7690539370  # Listening Artist


# Get diff tracks
def diffSongs():
    # Get all songs of all generated playlists
    allSongs = countSongs()

    # Get playlist songs
    print('--------------------')
    playlists = {
        "Favorite": 7673625615,
        "Like": 7673790351,
        "Nice": 7673790351
    }
    playlistSongs = []
    totalSongs = 0
    for playlistName, playlistId in playlists.items():
        # print('Requesting', playlistName, '...')
        # curPlaylistSongs = getPlaylistSongs(playlistId)['songs']
        with open('files/playlists/playlist_songs_' + playlistName + '_by ccgccc.json') as f:
            curPlaylistSongs = json.load(f)['songs']
        playlistSongs.extend(curPlaylistSongs)
        totalSongs = totalSongs + len(curPlaylistSongs)
        print(playlistName + ':', len(curPlaylistSongs))
    print('Playlists total:', totalSongs)

    diffSongIds = set()
    count = 0
    for song in playlistSongs:
        album = song['al']
        if filterArtist:
            if mustMainArtist:
                if song['ar'][0]['id'] != artists[artist]['artistId']:
                    continue
            else:
                containsArtist = False
                for ar in song['ar']:
                    if ar['id'] == artists[artist]['artistId']:
                        containsArtist = True
                        break
                if not containsArtist:
                    continue
        if song['id'] in allSongs or song['id'] in diffSongIds:
            continue
        count = count + 1
        diffSongIds.add(str(song['id']))
        songArtist = '/'.join(list(
            map(lambda artist: artist['name'], song['ar'])))
        print((str(count) + ':\t' + str(song['id']) + ',\t' + song['name'] +
               ',  ' + songArtist + ',  ' + album['name']).expandtabs(4))
        # print(count, track['id'], track['name'], trackArtists, sep=', ')
    print('Diff song ids:')
    print(','.join(diffSongIds), '\n\n')

    print('--------------------')
    if toAddPlaylistId == 8167810670:
        print('Adding songs to playlist 好歌拾遗...')
    if toAddPlaylistId == 7690539370:
        print('Adding songs to playlist Listening Artist...')

    if len(diffSongIds) > 0:
        addPlaylistSongs(toAddPlaylistId, diffSongIds)


if __name__ == '__main__':
    diffSongs()
