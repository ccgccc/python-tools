from common import *
from playlistRemoveSongs import playlistRomoveSongs


def main():
    # printPlaylistSongs()
    neteaseArtistCommentsDiffSongs()
    # neteaseMostCommentsSongs()
    # addPlaylistDiffSongs()
    # addPlaylistSongs()
    # likeSongs()
    # unLikeSongs()


# ********** Get playlist songs **********
def printPlaylistSongs():
    playlistName = 'Collection 1'
    playlistName = 'Listening'

    fileName = 'playlists/playlist_songs_' + playlistName + '_by ccgccc'
    playlist = loadJsonFromFile(fileName)
    print('Total:', len(playlist['songs']))
    print({song['name']: str(song['id']) for song in playlist['songs']}, '\n')
    print([song['name'] for song in playlist['songs']])
    print([str(song['id']) for song in playlist['songs']])


# ********** Get playlist diff songs(most comment songs - playlist songs)**********
def neteaseArtistCommentsDiffSongs():
    artist = 'phil_chang'
    songNumber = 45

    isCollection = False
    # isCollection = True
    collection = 'Collection 1'

    countOtherPlaylists = True
    # countOtherPlaylists = False

    toAddPlaylistId = 7690539370,  # Listening Artist

    # Most comment songs
    # songs = loadJsonFromFile('comments/json/' + artist + '_comments')
    mypath = 'files/comments/json/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f)) and f.startswith(artist)]
    with open(files[0]) as f:
        mostCommentSongs = json.load(f)

    # Most played songs playlist
    playlistSongIds = set()
    mypath = './files/playlists/playlist_details/json/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f))
             and f.startswith(('playlist_details_' + artists[artist]['name'] + ' Most Played Songs')
                              if not isCollection else ('playlist_details_' + collection))]
    with open(files[0]) as f:
        curPlaylistSongs = json.load(f)['songs']
        playlistSongIds = playlistSongIds | {
            song['id'] for song in curPlaylistSongs}
    # Other playlists
    if countOtherPlaylists:
        playlists = {
            "Favorite": 7673625615,
            "Like": 7673790351,
            "Nice": 7673790351,
            "Listening Artist": 7690539370,
            # "周杰伦": 7690432648,
            # "张学友": 7690443595
        }
        for playlistName, playlistId in playlists.items():
            # print('Requesting', playlistName, '...')
            # curPlaylistSongs = getPlaylistSongs(playlistId)['songs']
            with open('files/playlists/playlist_songs_' + playlistName + '_by ccgccc.json') as f:
                curPlaylistSongs = json.load(f)['songs']
            playlistSongIds = playlistSongIds | (
                {song['id'] for song in curPlaylistSongs})

    print('----------')
    diffSongs = []
    songCount = 0
    # print(playlistSongIds)
    for song in mostCommentSongs[:songNumber]:
        # print(songCount, song['id'], song['name'], sep=', ')
        songCount = songCount + 1
        if song['id'] in playlistSongIds:
            continue
        diffSongs.append(song)
        print(songCount, song['id'], song['commentCnt'],
              song['name'], song['albumName'], song['albumId'], song['artists'], sep=', ')
    print('----------')
    print('Diff songs:', len(diffSongs), '\n',
          [{str(song['id']): song['name']} for song in diffSongs], '\n')
    syncSongIds = [str(song['id']) for song in diffSongs]
    print('syncSongIds =', syncSongIds, '\n')

    # sureCheck()
    syncSongIds.reverse()
    addPlaylistSongs(toAddPlaylistId, syncSongIds)


# ********** Get playlist diff songs **********
def neteaseMostCommentsSongs():
    artist = 'zhouyunpeng'
    songNumber = 15
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

    # sureCheck()
    setBaseUrl(needCheck=True)
    syncSongIds = [str(song['id']) for song in songs[:songNumber]]
    addSongsToPlayList(playlistId, ','.join(syncSongIds))


# ********** Add playlist Diff songs **********
def addPlaylistDiffSongs():
    # Playlist id
    playlistId = 7690539370,  # Listening Artist
    isIncremental = True
    # playlist 2 minus 1
    playlistId1 = '8099516298'  # Listening
    playlistId2 = '7669746296'  #
    # playlistId1 = '7690539370'  # Listening Artist
    # playlistId2 = '8099516298'  # Listening
    # playlistId2 = '7769126077'  # Collection 1 - 朴树*许巍*李健*郑钧
    # playlistId1 = '7669372164'  # 周杰伦 Most Played Songs
    # playlistId2 = '7690432648'  # 周杰伦
    # playlistId = '7669698351'  # 张学友 Most Played Songs
    # playlistId2 = '7690443595'  # 张学友

    playlistId = 8099516298,  # Listening
    isIncremental = False
    playlistId1 = '8099516298'  # Listening
    playlistId2 = '7690539370'  # Listening Artist

    playlistSongs1 = getPlaylistSongs(playlistId1, addTs=True)['songs']
    playlistSongs2 = getPlaylistSongs(playlistId2, addTs=True)['songs']
    songIds = {song['id'] for song in playlistSongs1}
    playlistOnlySongs = []
    for song in playlistSongs2:
        if song['id'] not in songIds:
            playlistOnlySongs.append(song)
    printSongs(playlistOnlySongs)
    print('----------')
    playlistOnlySongIds = [{song['id']: song['name']}
                           for song in playlistOnlySongs]
    print('All:', len(playlistOnlySongIds))
    print(playlistOnlySongIds)
    syncSongIds = [str(list(dict.keys())[0]) for dict in playlistOnlySongIds]

    if not isIncremental:
        sureCheck()
        playlistRomoveSongs(playlistId, isSureCheck=True)
    # addSongsToPlayList(playlistId, ','.join(syncSongIds))
    addPlaylistSongs(playlistId, syncSongIds)


# ********** Add playlist songs **********
def addPlaylistSongs(playlistId=None, syncSongIds=None):
    # Playlist id
    if playlistId == None:
        # playlistId = 7673625615,  # Favorite
        playlistId = 7673790351,  # Like
        # playlistId = 7680312360,  # Nice
        # playlistId = 8075889883,  # High
        # playlistId = 7690539370,  # Listening Artist
    if syncSongIds == None:
        syncSongIds = ['442869386', '168097', '167747', '26494128', '110215',
                       '33248189', '110411', '29729145', '475073278', '33419478']

    # sureCheck()
    setBaseUrl(needCheck=True)
    # playlistRomoveSongs(playlistId, isSureCheck=True)
    addSongsToPlayList(playlistId, ','.join(syncSongIds))


# ********** Like songs **********
def likeSongs():
    # My like songs playlist id
    likePlaylistId = 553778357

    syncSongIds = ['33419478', '475073278', '26494128', '167747', '168097', '442869386']

    setBaseUrl(needCheck=True)
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
