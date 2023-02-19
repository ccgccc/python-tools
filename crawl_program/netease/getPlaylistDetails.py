import re
from artists import *
from common import *
from getPlaylistSongs import *


# Read parameters from command line
if len(sys.argv) >= 2:
    playlistIDs, realPlaylistNames = getPlaylistIds(sys.argv[1:])
    if playlistIDs != None and len(playlistIDs) > 0:
        playlistIds = playlistIDs
else:
    artistKeys = [artistToCrawl]
    # Generated artists
    # artistKeys = list(generateArtists.keys())[::-1]
    playlistIDs, realPlaylistNames = getPlaylistIds(artistKeys)

    # # Collections
    # playlistNames = ['Collection ' + str(i + 1) for i in range(5)]
    # playlistIDs, realPlaylistNames = getPlaylistIds(playlistNames)
    print('--------------------')
    print('Playlist:', '\n'.join(realPlaylistNames), sep='\n', end='\n\n')
    sureCheck()

# Check playlist ids
if playlistIDs != None and len(playlistIDs) > 0:
    playlistIds = playlistIDs

for playlistId in playlistIds:
    playlist = getPlaylist(playlistId)
    playlistSongs = getPlaylistSongs(playlistId)
    playlistSongs['playlist'] = playlist

    printPlaylists([playlist['playlist']])
    songs = printSongs(playlistSongs['songs'],
                       csvFileName=None, isWriteToConsole=False)
    songs.reverse()

    print('----------')
    playlistName = playlist['playlist']['name']
    # if playlistName.startswith('Collection'):
    #     playlistName = playlistName.split(' - ')[0]
    csvFileName = 'playlists/playlist_details/playlist_details_' + playlistName + \
        '_by ' + playlist['playlist']['creator']['nickname']
    csvFile = open('files/' + csvFileName + '.csv', 'w')
    csvFile.write('-, ID, 歌曲, 演唱, 作词, 作曲, 编曲, 制作人, ' +
                  '时长, 发行日期, 专辑, 类型, 热度\n')
    # Get all artists' albums
    allArtistKeys = set()
    for song in songs:
        allArtistKeys = allArtistKeys | set(song['artistKeys'])
    allArtistAlbums = {}
    for artistKey in allArtistKeys:
        with open('files/albums/' + artistKey + '_albums.json') as f:
            artistAlbums = json.load(f)
            allArtistAlbums = allArtistAlbums | {album['id']: album
                                                 for album in artistAlbums}
    songInfo = playlistSongs['songInfo'] = {}
    songCount = 0
    for song in songs:
        songCount = songCount + 1
        songId = song['id']
        songName = song['name']
        singer = song['artists']
        genre = song['genre']
        duration = song['duration']
        publishTime = song['publishTime']
        popularity = song['popularity']
        albumId = song['albumId']
        albumName = song['albumName']
        album = allArtistAlbums.get(albumId)
        if album != None:
            albumPublishMs = album.get('publishTime')
        else:
            album = getAlbum(albumId)
            # print(json.dumps(album, ensure_ascii=False))
            albumPublishMs = album['album']['publishTime']
        song['album'] = album
        albumPublishTime = datetime.fromtimestamp(
            albumPublishMs / 1000).strftime('%Y-%m-%d') if albumPublishMs != None else '--'
        # Get song lyrics
        lyricJson = getSongLyric(songId)
        songInfo[songId] = {}
        songInfo[songId]['song'] = song
        songInfo[songId]['lyric'] = lyricJson
        # print(json.dumps(lyricJson, ensure_ascii=False))
        lyric = lyricJson['lrc']['lyric']
        result = re.search(r'(?<=作词 : ).*?\n', lyric)
        lyricist = re.sub(r'\,', '，', result.group().strip()
                          ) if result != None else '---'
        result = re.search(r'(?<=作曲 : ).*?\n', lyric)
        composer = re.sub(r'\,', '，', result.group().strip()
                          ) if result != None else '---'
        result = re.search(r'(?<=编曲 : ).*?\n', lyric)
        editor = re.sub(r'\,', '，', result.group().strip()
                        ) if result != None else '---'
        result = re.search(r'(?<=制作人 : ).*?\n', lyric)
        producer = re.sub(r'\,', '，', result.group().strip()
                          ) if result != None else '---'
        # print(songCount, songName, singer, lyricist,
        #       composer, editor, producer, sep=', ')
        print(songCount, songId, songName, singer, lyricist, composer, editor, producer,
              duration, albumPublishTime, albumName, sep=', ')
        print(songCount, songId, songName, singer, lyricist, composer, editor, producer,
              duration, albumPublishTime, albumName, genre, popularity, sep=', ', file=csvFile)
    csvFile.close()
    writeJsonToFile(playlistSongs, 'playlists/playlist_details/json/playlist_details_'
                    + playlistName + '_by ' + playlist['playlist']['creator']['nickname'])
