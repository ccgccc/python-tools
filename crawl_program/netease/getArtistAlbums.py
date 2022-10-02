import requests
from artists import *
from common import *

url = baseUrl + '/artist/album'
limit = 100
params = {
    'id': artists[artistToCrawl]['artistId'],
    'limit': limit,
    'offset': 0
}
resJson = requests.get(url, headers=headers, params=params).json()
allAlbums = resJson['hotAlbums']
# while allAlbums['more'] == True: # seems not working
while len(resJson['hotAlbums']) == limit:
    params['offset'] = params['offset'] + limit
    print(params)
    resJson = requests.get(url, headers=headers, params=params).json()
    allAlbums.extend(resJson['hotAlbums'])

allAlbums = sorted(allAlbums, key=lambda album: album['publishTime'])

writeJsonToFile(allAlbums, 'albums/' + artistToCrawl + '_albums')

printAlbums(allAlbums)
