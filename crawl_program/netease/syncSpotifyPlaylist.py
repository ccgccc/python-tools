import zhconv
from artists import *
from common import *


# Get spotify playlist
playlist = []
with open('../spotify/files/playlists/generated_playlists_info/playlist_' +
          artists[artistToCrawl]['name'] + ' Most Played Songs_by ccg ccc.json') as f:
    playlist = json.load(f)

spotifyTrackNames = set(map(lambda track: zhconv.convert(
    track['track']['name'], 'zh-cn'), playlist['tracks']['items']))
print('------------------------------')
print('Spotify Tracks: ' + str(len(spotifyTrackNames)))
print(spotifyTrackNames, '\n')


# Get netease all songs
fileName = 'songs/' + artistToCrawl + '_allsongs'
neteaseAllSongs = loadJsonFromFile(fileName)
allSongsDict = {}
for song in neteaseAllSongs:
    if allSongsDict.get(song['name']) == None:
        allSongsDict[song['name']] = song['id']
# print(allSongsDict)
# print(len(allSongsDict))


# Get sync songs name & id
# syncSongs = dict(filter(lambda item: item[0] in spotifyTrackNames, allSongsDict.items()))
syncSongs = {k: v for k, v in allSongsDict.items() if k in spotifyTrackNames}
print('------------------------------')
print('Netease sync songs: ' + str(len(syncSongs)))
print(syncSongs, '\n')


# Get missing songs
missingSongs = spotifyTrackNames - syncSongs.keys()
print('------------------------------')
print('Netease missing songs: ' + str(len(missingSongs)))
print(missingSongs if len(missingSongs) > 0 else None, '\n')
print('------------------------------')


confirmOnceMode = True
isContinue = False
while not isContinue:
    if len(missingSongs) > 0:
        continueMsg = input(
            'There is some missing songs. Do you want to continue? (y/n): ')
    else:
        continueMsg = input(
            'All songs can be synced. Press Y to continue. (y/n): ')
    if continueMsg == 'y' or continueMsg == 'Y':
        isContinue = True
    elif confirmOnceMode or continueMsg == 'n' or continueMsg == 'N':
        sys.exit()

print('more')
