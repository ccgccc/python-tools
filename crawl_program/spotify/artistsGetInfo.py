from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken
from artists import *
from spotifyFunc import *

# ****************************************
#     Get spotify artistZh info by ids
# ****************************************

# Define all artist ids
artistList = list(reversed([v['artistId']
                  for k, v in generateArtists.items()]))
filePath = './files/artists'
if len(sys.argv) >= 2:
    if sys.argv[1] == 'other':
        artistList = list(reversed([v['artistId']
                          for k, v in otherArtists.items()]))
        filePath = filePath + '/other'
    elif sys.argv[1] == 'all':
        artistList = list(reversed([v['artistId']
                          for k, v in artists.items()]))
        filePath = filePath + '/all'
# # Define artist ids here
# artistList = [
#     # '1Hu58yHg2CXNfDhlPd7Tdd',  # 张学友
#     # '2elBjNSdBE2Y3f0j1mjrql',  # 周杰伦
#     # '2QcZxAgcs2I1q7CtCkl6MI',  # 陈奕迅
# ]


# Request artists info
token = getAccessToken(clientID, clientSecret)
artistsEn = getArtistInfo(token, artistList)['artists']
# print(json.dumps(artists, ensure_ascii=False))
artistsZh = getArtistInfo(token, artistList, language='zh-CN')['artists']
# print(json.dumps(artistsZh, ensure_ascii=False))

fileName = filePath + '/artists'
# Write json to file
with open(fileName + '.json', 'w') as f:
    json.dump(artistsZh, f, ensure_ascii=False)


def wirteToCsvFile(artists, artistsZh, csvFileName, isPrint=True):
    file = open(csvFileName, 'w')
    print('Artist Id, Name, Name(Zh), Popularity, Followers, Genres', file=file)
    for i in range(len(artistsZh)):
        artistZh = artistsZh[i]
        artistId = artistZh['id']
        artistName = artists[i]['name']
        artistZhName = artistZh['name']
        popularity = str(artistZh['popularity'])
        followers = artistZh['followers']['total']
        genres = ', '.join(artistZh['genres'])
        if isPrint:
            print('--------------------')
            print('Artist Id: ' + artistId)
            print('Artist Name: ' + artistName)
            print('Artist Name(Zh): ' + artistZhName)
            print('Popularity: ' + popularity)
            print('Followers: ' + format(followers, ','))
            print('Genres: ' + genres)
        print(artistId, artistName, artistZhName, popularity,
              followers, genres, sep=', ', file=file)
    file.close()


# 1. No sort
wirteToCsvFile(artistsEn, artistsZh, fileName + '.csv', isPrint=True)

# 2. Sort by followers
sortedArtists = sorted(
    artistsEn, key=lambda artist: artist['followers']['total'], reverse=True)
sortedArtistsZh = sorted(
    artistsZh, key=lambda artistZh: artistZh['followers']['total'], reverse=True)
wirteToCsvFile(sortedArtists, sortedArtistsZh,
               fileName + '_sorted_by_followers.csv', isPrint=False)

# Stat
print('--------------------')
print('Generate:', len(generateArtists))
seen = set()
uniqeOtherArtists = [artist for artist in otherArtists.keys()
                     if artist.split('-')[0] not in seen and not seen.add(artist.split('-')[0])]
print('Other:', len(uniqeOtherArtists),
      '(' + str(len(otherArtists)) + ')')
print('Total:', str(len(generateArtists) + len(uniqeOtherArtists)),
      '(' + str(len(artists)) + ')')
sys.exit()
