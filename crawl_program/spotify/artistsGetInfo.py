from spotifyFunc import *

# ****************************************
#     Get spotify artist info from id
# ****************************************

# Define artists id here
artistList = [
    # '1Hu58yHg2CXNfDhlPd7Tdd',  # 张学友
    # '2elBjNSdBE2Y3f0j1mjrql',  # 周杰伦
    # '2QcZxAgcs2I1q7CtCkl6MI',  # 陈奕迅
    # '0du5cEVh5yTK9QJze8zA0C',  # Bruno Mars
    # '7aRC4L63dBn3CiLDuWaLSI',  # 邓紫棋
    '7Dx7RhX0mFuXhCOUgB01uM',  # 林俊杰
]


# request artists info
token = getAccessToken(clientID, clientSecret)
artists = getArtistInfo(token, artistList)
# print(json.dumps(artists, ensure_ascii=False))
artistsZh = getArtistInfo(token, artistList, language='zh-CN')
# print(json.dumps(artistsZh, ensure_ascii=False))

# print artists info
for i in range(len(artists['artists'])):
    print('--------------------')
    artist = artists['artists'][i]
    print('Artist Id: ' + artist['id'])
    print('Artist Name: ' + artist['name'])
    print('Artist Name(Zh): ' + artistsZh['artists'][i]['name'])
    print('Popularity: ' + str(artist['popularity']))
    print('Followers: ' + format(artist['followers']['total'], ','))
    print('Genres: ' + ', '.join(artist['genres']))
