from artists import *
from common import *

# ****************************************
#    Get netease artist songs' comments
# ****************************************

# Define artist
# Define if load comments json file directly
loadCommentsFile = False
# Read parameters from command line
if len(sys.argv) >= 2:
    artistList = sys.argv[1:]
else:
    # Generated artists
    artistList = [artistToCrawl]
    # artistList = list(generateArtists.keys())
    # print('--------------------')
    # print('Artists:', '\n'.join(artistList), sep='\n', end='\n\n')
    # sureCheck()


for artist in artistList:
    print('--------------------')
    if loadCommentsFile:
        print('Loading file...')
        mypath = 'files/comments/json/'
        files = [mypath + f for f in os.listdir(mypath)
                 if os.path.isfile(os.path.join(mypath, f)) and f.startswith(artist)]
        with open(files[0]) as f:
            songs = json.load(f)
        # songs = loadJsonFromFile('comments/json/' + artist + '_comments')
        # songs.sort(key=lambda song: (
        #            song['commentCnt'], song['albumId'], -song['id']), reverse=True)
        # # Write to json file
        # writeJsonToFile(songs, 'comments/json/' + artist + '_comments')
    else:
        allSongs = getArtistSongs(artist)
        # allSongs = loadJsonFromFile(artist + '_songs')
        print(artists[artist]['name'], 'all songs:', len(allSongs['songs']))
        songs = printSongs(allSongs['songs'], reverse=False,
                           csvFileName=None, isWriteToConsole=False)
        print('----------')
        songCount = 0
        # songs = songs[:5]
        for song in songs:
            songCount = songCount + 1
            songId = song['id']
            songName = song['name']
            singer = song['artists']
            comments = getSongComments(songId, limit=1)
            commentCount = comments['total']
            song['commentCnt'] = commentCount
            song['comments'] = comments
            print(songCount, songId, song['name'],
                  singer, commentCount, sep=', ')
        # Sort by comments count
        # songs.sort(key=lambda song: song['commentCnt'], reverse=True)
        songs.sort(key=lambda song: (
            song['commentCnt'], song['albumId'], -song['id']), reverse=True)
        # Write to json file
        writeJsonToFile(songs, 'comments/json/' + artist +
                        '_comments_' + time.strftime("%Y%m%d"))

    print('Writing to csv...')
    # Write to csv file
    csvFile = open('files/comments/' + artist + '_comments.csv', 'w')
    csvFile.write('-, ID, 评论数量, 歌曲, 专辑, 专辑ID, 歌手\n')
    songCount = 0
    for song in songs:
        songCount = songCount + 1
        print(songCount, song['id'], song['commentCnt'],
              song['name'], song['albumName'], song['albumId'], song['artists'], sep=', ', file=csvFile)
    csvFile.close()
    print('Done!')
print('All Done!')
