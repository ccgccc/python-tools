from common import *
from playlistRemoveSongs import playlistRomoveSongs


def main():
    # printPlaylistSongs()
    # countSongs()
    # getDiffSongs()
    neteaseArtistDiffSongs()
    # addNeteaseMostCommentSongs()
    # addPlaylistSongs()
    # likeSongs()
    # unLikeSongs()


# ********** Get playlist songs **********
def printPlaylistSongs():
    playlistName = 'Collection 1'

    fileName = 'playlists/playlist_songs_' + playlistName + '_by ccgccc'
    playlist = loadJsonFromFile(fileName)
    print({song['name']: str(song['id']) for song in playlist['songs']})
    print([song['name'] for song in playlist['songs']])
    print([str(song['id']) for song in playlist['songs']])


# === Count total tracks of all generated playlists
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
    playlistSongs = getPlaylistSongs(playlistId)
    tracksNum = len(playlistSongs['songs'])
    count = count + tracksNum
    print('好歌拾遗: ' + str(tracksNum) + '  (Acc:' + str(count) + ')')
    allSongs = allSongs | {song['id']
                           for song in playlistSongs['songs']}
    print('All: ', len(allSongs))
    return allSongs


# Get diff tracks
def getDiffSongs():
    allSongs = countSongs()
    print('--------------------')
    # Get playlist songs
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

    # Get artists diff tracks
    filterArtist = False
    artist = 'eason_chan'
    filterArtist = True
    diffSongIds = set()
    count = 0
    for song in playlistSongs:
        album = song['al']
        if filterArtist and song['ar'][0]['id'] != artists[artist]['artistId']:
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
    print(','.join(diffSongIds))


# ********** Get playlist diff songs **********
def neteaseArtistDiffSongs():
    artist = 'jj_lin'
    songNumber = 40
    toAddPlaylistId = 7690539370,  # Listening Artist

    playlists = {
        "Favorite": 7673625615,
        "Like": 7673790351,
        "Nice": 7673790351,
        # "Listening Artist": 7690539370,
        # "周杰伦": 7690432648,
        # "张学友": 7690443595
    }
    playlistSongIds = set()
    for playlistName, playlistId in playlists.items():
        # print('Requesting', playlistName, '...')
        # curPlaylistSongs = getPlaylistSongs(playlistId)['songs']
        with open('files/playlists/playlist_songs_' + playlistName + '_by ccgccc.json') as f:
            curPlaylistSongs = json.load(f)['songs']
        playlistSongIds = playlistSongIds | (
            {song['id'] for song in curPlaylistSongs})
    # Add most played songs playlist
    mypath = './files/playlists/playlist_details/json/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f))
             and f.startswith('playlist_details_' + artists[artist]['name'] + ' Most Played Songs')]
    with open(files[0]) as f:
        curPlaylistSongs = json.load(f)['songs']
        playlistSongIds = playlistSongIds | {
            song['id'] for song in curPlaylistSongs}

    print('----------')
    # songs = loadJsonFromFile('comments/json/' + artist + '_comments')
    mypath = 'files/comments/json/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f)) and f.startswith(artist)]
    with open(files[0]) as f:
        songs = json.load(f)
    diffSongs = []
    songCount = 0
    print(playlistSongIds)
    for song in songs[:songNumber]:
        songCount = songCount + 1
        if song['id'] in playlistSongIds:
            continue
        diffSongs.append(song)
        print(songCount, song['id'], song['commentCnt'],
              song['name'], song['albumName'], song['albumId'], song['artists'], sep=', ')
    print('----------')
    print('Diff songs:', [{str(song['id']): song['name']}
          for song in diffSongs], '\n')
    syncSongIds = [str(song['id']) for song in diffSongs]
    print('syncSongIds =', syncSongIds, '\n')

    # sureCheck()
    addPlaylistSongs(toAddPlaylistId, syncSongIds)


# ********** Add playlist songs **********
def addPlaylistSongs(playlistId=None, syncSongIds=None):
    # Playlist id
    if playlistId == None:
        # playlistId = 7673625615,  # Favorite
        # playlistId = 7673790351,  # Like
        # playlistId = 7680312360,  # Nice
        # playlistId = 8075889883,  # High
        playlistId = 7690539370,  # Listening Artist
    if syncSongIds == None:
        syncSongIds = ['34509411', '574908698', '31426608']

    # sureCheck()
    setBaseUrl(needCheck=True)
    # playlistRomoveSongs(playlistId, isSureCheck=True)
    addSongsToPlayList(playlistId, ','.join(syncSongIds))


# ********** Get playlist diff songs **********
def addNeteaseMostCommentSongs():
    artist = 'xiaohe'
    songNumber = 10
    playlistId = 8099516298,  # Listening

    print('----------')
    dir = './files/comments/json/'
    fileName = [f for f in os.listdir(dir)
                if os.path.isfile(os.path.join(dir, f))
                and re.search(artist, f)][0]
    with open(dir + fileName) as f:
        songs = json.load(f)
    songCount = 0
    for song in songs[:songNumber]:
        songCount = songCount + 1
        print(songCount, song['id'], song['commentCnt'],
              song['name'], song['albumName'], song['albumId'], song['artists'], sep=', ')

    syncSongIds = [str(song['id']) for song in songs[:songNumber]]

    addSongsToPlayList(playlistId, ','.join(syncSongIds))


# ********** Add playlist Diff songs **********
def addPlaylistDiffSongs():
    # Playlist id
    playlistId = 7690539370,  # Listening Artist

    # playlist 2 minus 1
    # playlistId = '7669698351'  # 张学友 Most Played Songs
    # playlistId2 = '7690443595'  # 张学友
    playlistId1 = '7669372164'  # 周杰伦 Most Played Songs
    playlistId2 = '7690432648'  # 周杰伦
    playlistSongs1 = getPlaylistSongs(playlistId1, addTs=True)['songs']
    playlistSongs2 = getPlaylistSongs(playlistId2, addTs=True)['songs']
    songIds = {song['id'] for song in playlistSongs1}
    playlistOnlySongs = []
    for song in playlistSongs2:
        if song['id'] not in songIds:
            playlistOnlySongs.append({song['id']: song['name']})
    print('All:', len(playlistOnlySongs))
    print(playlistOnlySongs)
    syncSongIds = [str(list(dict.keys())[0]) for dict in playlistOnlySongs]

    sureCheck()
    playlistRomoveSongs(playlistId, isSureCheck=True)
    addSongsToPlayList(playlistId, ','.join(syncSongIds))


# ********** Like songs **********
def likeSongs():
    syncSongIds = ['346089', '1855073423', '1855073420', '27678518', '401593758', '1954886570',
                   '27678500', '27678501', '1954889726', '1954888367', '1857483755', '1857483487']

    # My like songs playlist id
    likePlaylistId = 553778357
    addSongsToPlayList(likePlaylistId, ','.join(syncSongIds))


# ********** Like songs **********
def unLikeSongs():
    syncSongIds = ['347643', '347775', '347504',
                   '406243283', '347713', '347720', '347760']

    # My like songs playlist id
    likePlaylistId = 553778357
    # sureCheck()
    setBaseUrl(needCheck=True)
    deleteSongsToPlayList(likePlaylistId, ','.join(syncSongIds))


if __name__ == '__main__':
    main()
