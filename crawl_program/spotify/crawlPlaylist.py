import requests
import json
from utils.auth import *
from secrets import *

# ******************************
#    抓取 Spotify 播放列表数据
# ******************************

# 此处定义播放列表id
playlistID = "6Ev0ju4qLsqSLznN7fjErt"


def getPlaylistTracks(token, playlistID):
    playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}"
    getHeader = {
        "Authorization": "Bearer " + token
    }
    res = requests.get(playlistEndPoint, headers=getHeader)
    playlistObject = res.json()
    return playlistObject


# API requests
token = getAccessToken(clientID, clientSecret)
tracklist = getPlaylistTracks(token, playlistID)
# print(tracklist)
# Write json to file
# with open('tracklist.json', 'w') as f:
#     json.dump(tracklist, f)

for t in tracklist['tracks']['items']:
    print('--------------------')
    print('Track:   ' + t['track']['name'])
    print('Album:   ' + t['track']['album']['name'] +
          ' (' + t['track']['album']['release_date'] + ")")
    print('Artists: ', end='')
    artists = t['track']['artists']
    for i in range(len(artists)):
        print(artists[i]['name'], end='')
        print(', ', end='') if i < len(artists) - 1 else print()
