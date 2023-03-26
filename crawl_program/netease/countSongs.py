from common import *

# **************************************************
#    Count all songs of all generated playlists
# **************************************************


def countSongs():
    artistNames = list(
        reversed([artistInfo['name'] for artist, artistInfo in generateArtists.items()]))
    # Generated playlists
    mypath = './files/playlists/playlist_details/json/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f)) and f.endswith('Most Played Songs_by ccgccc.json')]
    files.sort(key=lambda file: artistNames.index(
        re.sub(r'.*json/playlist_details_(.*) Most.*', r'\1', file)))
    # Collections
    mypath2 = './files/playlists/'
    files2 = [mypath2 + f for f in os.listdir(mypath2)
              if os.path.isfile(os.path.join(mypath2, f)) and f.endswith('.json')
              and (f.find('Collection') > 0  # or f.find('Hit') > 0
                   or f.find('张学友_by ccgccc') > 0 or f.find('周杰伦_by ccgccc') > 0)]
    files2.sort()
    files.extend(files2)
    # Get all songs
    allSongs = set()
    count = 0
    for file in files:
        with open(file) as f:
            playlistSongs = json.load(f)
        songsNum = len(playlistSongs['songs'])
        count = count + songsNum
        if file in files2:
            print(re.sub(".*playlist_songs_(.*)_by ccgccc\.json", r'\1', file), end='')
        else:
            print(re.sub(".*playlist_details_(.*)_by ccgccc\.json", r'\1', file), end='')
        print(':  ' + str(songsNum) + '  (Acc:' + str(count) + ')')
        allSongs = allSongs | {song['id']
                               for song in playlistSongs['songs']}
    # plus 好歌拾遗
    playlistId = 8167810670
    # setBaseUrl()
    playlistSongs = getPlaylistSongs(playlistId, addTs=True)
    tracksNum = len(playlistSongs['songs'])
    count = count + tracksNum
    print('好歌拾遗: ' + str(tracksNum) + '  (Acc:' + str(count) + ')')
    allSongs = allSongs | {song['id']
                           for song in playlistSongs['songs']}
    print('All: ', len(allSongs))
    return allSongs


if __name__ == '__main__':
    countSongs()
