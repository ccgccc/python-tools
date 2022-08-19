import json
from spotifyFunc import *
from artists import *

# ******************************
#  Crawl spotify artist albums
# ******************************

# Define artist here
artist = 'bruno_mars'
artistId = artists[artist]['artistId']


#  Get artist albums
allAblums = getArtistAllAlbums(artistId)

# Write json to file
with open('./files/' + artist + '_albums.json', 'w') as f:
    json.dump(allAblums, f, ensure_ascii=False)

# Simple Output
# i = 0
# for t in allAblums:
#     print('--------------------')
#     i = i + 1
#     print(str(i) + ': ' + t['name'])
#     print('Date: ' + t['release_date'])
#     print('Tracks: ' + str(t['total_tracks']))

# Detail Output
count = 0
albumFile = open('./files/' + artist + '_albums.txt', 'w')
for t in allAblums:
    seperation = '--------------------'
    count = count + 1
    albumName = str(count) + ': ' + t['name']
    albumId = 'Id: ' + t['id']
    albumGroup = 'Group: ' + t['album_group']
    albumType = 'Type:  ' + t['album_type']
    releaseDate = 'Date:  ' + t['release_date']
    tracksNum = 'Tracks: ' + str(t['total_tracks'])
    artists = 'Artists: '
    artistsList = t['artists']
    for i in range(len(artistsList)):
        artists = artists + artistsList[i]['name'] + \
            (', ' if i < len(artistsList) - 1 else '')
    print(seperation, albumName, albumId, albumGroup, albumType,
          releaseDate, tracksNum, artists, sep='\n')
    print(seperation, albumName, albumId, albumGroup, albumType,
          releaseDate, tracksNum, artists, sep='\n', file=albumFile)
albumFile.close()

print('--------------------')
print('Album Statistic:')
albumGroupStat = dict()
albumTypeStat = dict()
albumGroupTypeStat = dict()
for t in allAblums:
    albumGroup = 'AlbumGroup: ' + t['album_group']
    if albumGroup not in albumGroupStat:
        albumGroupStat[albumGroup] = 1
    else:
        albumGroupStat[albumGroup] = albumGroupStat[albumGroup] + 1
    albumType = 'AlbumType: ' + t['album_type']
    if albumType not in albumTypeStat:
        albumTypeStat[albumType] = 1
    else:
        albumTypeStat[albumType] = albumTypeStat[albumType] + 1
    albumGroupType = albumGroup + ', ' + albumType
    if albumGroupType not in albumGroupTypeStat:
        albumGroupTypeStat[albumGroupType] = 1
    else:
        albumGroupTypeStat[albumGroupType] = albumGroupTypeStat[albumGroupType] + 1
print(albumGroupStat.items())
print(albumTypeStat.items())
print(albumGroupTypeStat.items())
