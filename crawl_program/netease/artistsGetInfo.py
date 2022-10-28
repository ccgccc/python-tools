import re
import requests
from artists import *
from common import *

# ****************************************
#        Get netease artists info
# ****************************************

# Define write to csv or not
isWriteToCsv = True
# Define request or not
isRequest = True
# Get all artists info
artistIdNames = {v['artistId']: k for k, v in artists.items()}

# # Define is incremental
# isIncremental = False
# # Define all artists
# artistIds = artistIdNames.keys()

# Define is incremental
isIncremental = True
# Specify artists
artistIds = [artists[artistToCrawl]['artistId']]
# artistIds = [
#     '6460',  # 张学友
#     '6452',  # 周杰伦
# ]


if isRequest:
    artistDetailUrl = baseUrl + '/artist/detail'
    artistFanslUrl = baseUrl + '/artist/follow/count'
    allArtistsDetails = {}
    allArtistsFans = {}
    for artistId in artistIds:
        print('Requesting ' + artists[artistIdNames[artistId]]['name'] + '...')
        params = {
            'id': artistId,
        }
        resJson = requests.get(
            artistDetailUrl, headers=headers, params=params).json()
        # print(json.dumps(resJson, ensure_ascii=False))
        allArtistsDetails = allArtistsDetails | {
            artistIdNames[artistId]: resJson['data']}

        params = {
            'id': artistId,
        }
        resJson = requests.get(
            artistFanslUrl, headers=headers, params=params).json()
        # print(json.dumps(resJson, ensure_ascii=False))
        allArtistsFans = allArtistsFans | {
            artistIdNames[artistId]: resJson['data']}
    if isIncremental:
        allArtistsDetails = loadJsonFromFile(
            'artists/artists') | allArtistsDetails
        allArtistsFans = loadJsonFromFile(
            'artists/artistsFans') | allArtistsFans
    writeJsonToFile(allArtistsDetails, 'artists/artists')
    writeJsonToFile(allArtistsFans, 'artists/artistsFans')
else:
    allArtistsDetails = loadJsonFromFile('artists/artists')
    allArtistsFans = loadJsonFromFile('artists/artistsFans')


def wirteToCsvFile(allArtistsDetails, allArtistsFans, csvFileName, isPrint=True):
    file = open(csvFileName, 'w')
    print('Artist Id, Name, Albums, Songs, Mvs, Vedios, Fans, Rank, RankType, Identity, '
          '演唱, 作词, 作曲, 编曲, 制作, Beat, 演奏, 录音, 混音, BriefDesc', file=file)
    identities = {'演唱': 0, '作词': 0, '作曲': 0, '编曲': 0,
                  '制作': 0, 'Beat': 0, '演奏': 0, '录音': 0, '混音': 0}
    for artist, artistInfo in allArtistsDetails.items():
        artistId = artistInfo['artist']['id']
        artistName = artistInfo['artist']['name']
        albumSize = artistInfo['artist']['albumSize']
        musicSize = artistInfo['artist']['musicSize']
        mvSize = artistInfo['artist']['mvSize']
        briefDesc = artistInfo['artist']['briefDesc']
        fansCount = allArtistsFans[artist]['fansCnt']
        rank = artistInfo['artist']['rank']['rank'] \
            if artistInfo['artist'].get('rank') != None else ''
        rankType = artistInfo['artist']['rank']['type'] \
            if artistInfo['artist'].get('rank') != None else ''
        videoCount = artistInfo['videoCount']
        identify = artistInfo['identify']['imageDesc'] \
            if artistInfo.get('identify') != None else ''
        secondaryExpertIdentity = artistInfo['secondaryExpertIdentiy']
        secondaryIdentity = {identity['expertIdentiyName']: identity['expertIdentiyCount']
                             for identity in secondaryExpertIdentity}
        if isPrint:
            print('--------------------')
            print('Artist Id:', artistId)
            print('Artist Name:', artistName)
            print('Albums:', albumSize)
            print('Songs:', musicSize)
            print('Mvs:', mvSize)
            print('Vedios:', videoCount)
            print('Rank:', rank)
            print('RankType:', rankType)
            print('Identity:', identify)
            print('Identities:', {k: v for k,
                  v in secondaryIdentity.items() if v > 0})
            print('BriefDesc:', briefDesc)
        print(artistId, artistName, albumSize, musicSize, mvSize, videoCount,
              fansCount, rank, rankType, identify, sep=', ', end=', ', file=file)
        print(', '.join([str(secondaryIdentity[k])
                        if secondaryIdentity.get(k) != None and secondaryIdentity[k] > 0 else ''
                        for k, v in identities.items()]), end=', ', file=file)
        print('"' + re.sub(r'\n', '\\\\', briefDesc) + '"', file=file)
    file.close()


if isWriteToCsv:
    fileName = './files/artists/artists'
    wirteToCsvFile(allArtistsDetails, allArtistsFans,
                   fileName + '.csv', isPrint=True)

    # Sorted by fans count
    sorteArtistsDetails = dict(sorted(
        allArtistsDetails.items(), key=lambda item: allArtistsFans[item[0]]['fansCnt'], reverse=True))
    wirteToCsvFile(sorteArtistsDetails, allArtistsFans,
                   fileName + '_sorted_by_fans.csv', isPrint=False)

    # Sorted by ranktype and rank
    sorteArtistsDetails2 = dict(sorted(
        allArtistsDetails.items(),
        key=lambda item: (
            item[1]['artist']['rank']['type']
            if item[1]['artist'].get('rank') != None else 99999,
            item[1]['artist']['rank']['rank']
            if item[1]['artist'].get('rank') != None else 99999
        ))
    )
    wirteToCsvFile(sorteArtistsDetails2, allArtistsFans,
                   fileName + '_sorted_by_rank.csv', isPrint=False)
