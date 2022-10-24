import requests
from artists import *
from common import *

# ****************************************
#    Get netease artist songs directly
# ****************************************


url = baseUrl + '/artist/songs'
# url = baseUrl + '/artist/top/song'
limit = 200  # max 200
params = {
    'id': artists[artistToCrawl]['artistId'],
    'limit': limit,
    'offset': 0
}
resJson = requests.get(url, headers=headers, params=params).json()
allSongs = resJson
while resJson['more'] == True:
    params['offset'] = params['offset'] + limit
    print(params)
    resJson = requests.get(url, headers=headers, params=params).json()
    allSongs['songs'].extend(resJson['songs'])

writeJsonToFile(allSongs, artistToCrawl + '_songs')

printSongs(allSongs['songs'])
