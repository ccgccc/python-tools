import zhconv
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken
from artists import *
from spotifyFunc import *

# ****************************************
#     Get spotify artistZh info by ids
# ****************************************

# Define all artist ids
artistsList = [artists[artistToCrawl]['artistId']]

# # Define artist ids here
# artistList = [
#     # '1Hu58yHg2CXNfDhlPd7Tdd',  # 张学友
#     # '2elBjNSdBE2Y3f0j1mjrql',  # 周杰伦
#     # '2QcZxAgcs2I1q7CtCkl6MI',  # 陈奕迅
# ]


def main():
    filePath = None
    if len(sys.argv) >= 2:
        filePath = './files/artists'
        if sys.argv[1] == 'other':
            artistList = list(reversed([v['artistId']
                                        for k, v in otherArtists.items()]))
            filePath = filePath + '/other'
        elif sys.argv[1] == 'other':
            artistList = list(reversed([v['artistId']
                                        for k, v in otherArtists.items()]))
            filePath = filePath + '/other'
        elif sys.argv[1] == 'all':
            artistList = list(reversed([v['artistId']
                                        for k, v in artists.items()]))
            filePath = filePath + '/all'
        else:
            artistList = [artists[sys.argv[1]]['artistId']]
            filePath = None
    else:
        artistList = artistsList

    # Request artists info
    token = getAccessToken(clientID, clientSecret)
    artistsEn = getArtistInfo(token, artistList)['artists']
    # print(json.dumps(artists, ensure_ascii=False))
    artistsZh = getArtistInfo(token, artistList, language='zh-CN')['artists']
    # print(json.dumps(artistsZh, ensure_ascii=False))

    fileName = None
    if filePath != None:
        fileName = filePath + '/artists'
        # Write json to file
        with open(fileName + '.json', 'w') as f:
            json.dump(artistsZh, f, ensure_ascii=False)
        with open(fileName + '_en.json', 'w') as f:
            json.dump(artistsEn, f, ensure_ascii=False)

    # Print
    printOrWriteArtists(artistsEn, artistsZh, None, isPrint=True)
    if fileName == None:
        sys.exit()

    # 1. No sort
    printOrWriteArtists(artistsEn, artistsZh, fileName + '.csv')

    # 2. Sort by followers
    sortedArtists = sorted(
        artistsEn, key=lambda artist: artist['followers']['total'], reverse=True)
    sortedArtistsZh = sorted(
        artistsZh, key=lambda artistZh: artistZh['followers']['total'], reverse=True)
    printOrWriteArtists(sortedArtists, sortedArtistsZh,
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


def printOrWriteArtists(artists, artistsZh, csvFileName, isPrint=True):
    if csvFileName != None:
        file = open(csvFileName, 'w')
        print('Artist Id, Name, Name(Zh), Name(En), Popularity, Followers, Genres',
              file=file)
    for i in range(len(artistsZh)):
        artistZh = artistsZh[i]
        artistId = artistZh['id']
        artistName = artists[i]['name']
        artistZhName = artistZh['name']
        artistSimZhName = zhconv.convert(artistZhName, 'zh-cn')
        popularity = str(artistZh['popularity'])
        followers = artistZh['followers']['total']
        genres = ', '.join(artistZh['genres'])
        if isPrint:
            print('--------------------')
            print('Artist Id: ' + artistId)
            print('Artist Name: ' + artistZhName)
            print('Artist Name(Zh): ' + artistSimZhName)
            print('Artist Name(En): ' + artistName)
            print('Followers: ' + format(followers, ','))
            print('Popularity: ' + popularity)
            print('Genres: ' + genres)
        if csvFileName != None:
            print(artistId, artistZhName, artistSimZhName, artistName, followers,
                  popularity, genres, sep=', ', file=file)
    if csvFileName != None:
        file.close()


if __name__ == '__main__':
    main()
