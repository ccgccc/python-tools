import time
import requests
from common import *

# ****************************************
#      sub or unsub netease artist
# ****************************************

# Define artist ids
artistIds = ['32809', '35050']
# 0: unsubcribe, 1: subcribe
operation = 0
# Use right cookie to retrive private playlists
headers['cookie'] = readFileContent('cookie.txt')


url = baseUrl + '/artist/sub'
for artistId in artistIds:
    params = {
        'id': artistId,
        't': operation
    }
    resJson = requests.get(url, headers=headers, params=params).json()
    print(json.dumps(resJson, ensure_ascii=False))
