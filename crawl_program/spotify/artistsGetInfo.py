import zhconv
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken, getAuthorizationToken
from artists import *
from spotifyFunc import *

# ****************************************
#     Get spotify artist info by ids
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
    isMerged = False
    if len(sys.argv) > 1:
        filePath = './files/artists'
        if sys.argv[1] == 'generate':
            artistList = list(reversed([v['artistId']
                                        for k, v in otherArtists.items()]))
            filePath = filePath + '/generate'
        elif sys.argv[1] == 'other':
            artistList = list(reversed([v['artistId']
                                        for k, v in otherArtists.items()]))
            filePath = filePath + '/other'
        elif sys.argv[1] == 'all':
            artistList = list(reversed([v['artistId']
                                        for k, v in artists.items()]))
            filePath = filePath + '/all'
        elif sys.argv[1] == 'merge':
            artistList = list(reversed([v['artistId']
                                        for k, v in artists.items()]))
            isMerged = True
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
    if isMerged:
        fileName = filePath + '/artists_merged'
        scope = "user-follow-read"
        spotify, authorizeToken = getAuthorizationToken(
            clientID, clientSecret, scope)
        followingArtistsEn = getFollowingArtists(spotify, authorizeToken, 50)
        followingArtistsZh = getFollowingArtists(
            spotify, authorizeToken, 50, language='zh-CN')
        # with open('files/artists/following_artists.json') as f:
        #     followingArtistsEn = json.load(f)
        # with open('files/artists/following_artists_en.json') as f:
        #     followingArtistsZh = json.load(f)
        # Concatenate following artists
        existArtistIds = {artist['id'] for artist in artistsEn}
        artistsEn.extend(
            [artist for artist in followingArtistsEn['artists']['items'] if artist['id'] not in existArtistIds])
        artistsZh.extend(
            [artist for artist in followingArtistsZh['artists']['items'] if artist['id'] not in existArtistIds])
    if fileName != None:
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

    # Process artists to json
    if isMerged:
        processArtistsJson(sortedArtists, sortedArtistsZh, fileName)

    # Stat
    print('--------------------')
    print('Generate:', len(generateArtists))
    seen = set()
    uniqeOtherArtists = [artist for artist in otherArtists.keys()
                         if artist.split('-')[0] not in seen and not seen.add(artist.split('-')[0])]
    print('Other:', len(uniqeOtherArtists),
          '(' + str(len(otherArtists)) + ')')
    print('Total:', len(generateArtists) + len(uniqeOtherArtists),
          '(' + str(len(artists)) + ')')
    if isMerged:
        print('----------')
        print('Follows:', len(followingArtistsEn['artists']['items']))
        print('Merge:', len(generateArtists) + len(uniqeOtherArtists) +
              len([artist for artist in followingArtistsEn['artists']
                  ['items'] if artist['id'] not in existArtistIds]),
              '(' + str(len(artistsEn)) + ')')
        print('Unfollow:', [v['name'] for k, v in otherArtists.items() if v['artistId'] in {
              a['id'] for a in followingArtistsEn['artists']['items']}])


def processArtistsJson(artistsEn, artistsZh, fileName):
    artistsJson = dict()
    for i in range(len(artistsEn)):
        curArtistJson = {
            artistsEn[i]['name'].lower().replace(' ', '_'): {
                'name': zhconv.convert(artistsZh[i]['name'], 'zh-cn'),
                'artistId': artistsEn[i]['id']
            }}
        artistsJson = artistsJson | curArtistJson
    # Write json to file
    with open(fileName + '_processed.json', 'w') as f:
        json.dump(artistsJson, f, ensure_ascii=False)


def printOrWriteArtists(artists, artistsZh, csvFileName, isPrint=True):
    if csvFileName != None:
        file = open(csvFileName, 'w')
        print('Artist Id, Name, Name(Zh), Name(En), Followers, Popularity, Genres',
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
