from utils.secrets import clientID, clientSecret
from utils.auth import getAuthorizationToken
from artists import *
from spotifyFunc import *
from artistsGetInfo import *


scope = "user-follow-read"
spotify, authorizeToken = getAuthorizationToken(
    clientID, clientSecret, scope)
artistsEn = getFollowingArtists(spotify, authorizeToken, 50)
artistsZh = getFollowingArtists(
    spotify, authorizeToken, 50, language='zh-CN')

fileName = 'files/artists/following_artists'
with open(fileName + '.json', 'w') as f:
    json.dump(artistsZh, f, ensure_ascii=False)
with open(fileName + '_en.json', 'w') as f:
    json.dump(artistsEn, f, ensure_ascii=False)
# print(json.dumps(artistsZh, ensure_ascii=False))

# with open('files/artists/following_artists.json') as f:
#     artistsZh = json.load(f)
# with open('files/artists/following_artists_en.json') as f:
#     artistsEn = json.load(f)

# 1. No sort
printOrWriteArtists(artistsEn['artists']['items'],
                    artistsZh['artists']['items'], fileName + '.csv', isPrint=True)
print('--------------------')
print('Total:', len(artistsZh['artists']['items']))

# 2. Sort by followers
sortedArtists = sorted(
    artistsEn['artists']['items'], key=lambda artist: artist['followers']['total'], reverse=True)
sortedArtistsZh = sorted(
    artistsZh['artists']['items'], key=lambda artistZh: artistZh['followers']['total'], reverse=True)
printOrWriteArtists(sortedArtists, sortedArtistsZh,
                    fileName + '_sorted_by_followers.csv', isPrint=False)

# 3. Sort by followers & filter existing artists
existArtistIdSet = {v['artistId'] for k, v in artists.items()}
filteredArtists = [artist for artist in sortedArtists
                   if artist['id'] not in existArtistIdSet]
filteredArtistsZh = [artist for artist in sortedArtistsZh
                     if artist['id'] not in existArtistIdSet]
printOrWriteArtists(filteredArtists, filteredArtistsZh,
                    fileName + '_filtered.csv', isPrint=False)
print('Filtered:', len(filteredArtistsZh))

processArtistsJson(filteredArtists, filteredArtistsZh, fileName + '_filtered')
