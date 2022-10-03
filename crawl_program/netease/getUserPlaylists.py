import time
import requests
from common import *

# Use right cookie to retrive private playlists
headers['cookie'] = readFileContent('cookie.txt')

url = baseUrl + '/user/playlist'
limit = 1000
params = {
    'uid': myUserId,
    'limit': limit,
    'offset': 0
}
playlists = requests.get(url, headers=headers, params=params).json()
# print(json.dumps(playlists, ensure_ascii=False))

fileName = 'playlists/all_my_playlists_bak_'+ time.strftime("%Y-%m-%d")
writeJsonToFile(playlists, fileName)
printPlaylists(playlists['playlist'], fileName)
