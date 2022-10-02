from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken
from spotifyFunc import *

# ****************************************
#     Get spotify artist info from id
# ****************************************

# Define artists id here
artistList = [
    '1Hu58yHg2CXNfDhlPd7Tdd',  # 张学友
    '2elBjNSdBE2Y3f0j1mjrql',  # 周杰伦
    '2QcZxAgcs2I1q7CtCkl6MI',  # 陈奕迅
    '0du5cEVh5yTK9QJze8zA0C',  # Bruno Mars
    '7aRC4L63dBn3CiLDuWaLSI',  # 邓紫棋
    '7Dx7RhX0mFuXhCOUgB01uM',  # 林俊杰
    '2hgxWUG24w1cFLBlPSEVcV',  # 许嵩
    '2F5W6Rsxwzg0plQ0w8dSyt',  # 王力宏
    '4F5TrtYYxsVM1PhbtISE5m',  # Beyond
    '10LslMPb7P5j9L2QXGZBmM'  # 汪峰
]


# Request artists info
token = getAccessToken(clientID, clientSecret)
artists = getArtistInfo(token, artistList)
# print(json.dumps(artists, ensure_ascii=False))
artistsZh = getArtistInfo(token, artistList, language='zh-CN')
# print(json.dumps(artistsZh, ensure_ascii=False))

fileName = './files/artists/artists'
# Write json to file
with open(fileName + '.json', 'w') as f:
    json.dump(artistsZh, f, ensure_ascii=False)

# Print artists info
csvFileName = fileName + '.csv'
file = open(csvFileName, 'w')
print('Artist Id, Name, Name(Zh), Popularity, Followers, Genres', file=file)
for i in range(len(artistsZh['artists'])):
    print('--------------------')
    artist = artistsZh['artists'][i]
    artistId = artist['id']
    artistName = artists['artists'][i]['name']
    artistZhName = artistsZh['artists'][i]['name']
    popularity = str(artist['popularity'])
    followers = artist['followers']['total']
    genres = ', '.join(artist['genres'])
    print('Artist Id: ' + artistId)
    print('Artist Name: ' + artistName)
    print('Artist Name(Zh): ' + artistZhName)
    print('Popularity: ' + popularity)
    print('Followers: ' + format(followers, ','))
    print('Genres: ' + genres)
    print(artistId, artistName, artistZhName, popularity,
          followers, genres, sep=', ', file=file)
file.close()
