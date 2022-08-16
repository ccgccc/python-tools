import requests
import base64
import json
from secrets import *

# ******************************
#    抓取 Spotify 播放列表数据
# ******************************

# 此处定义播放列表id
playlistID = "6Ev0ju4qLsqSLznN7fjErt"


def getAccessToken(clientID, clientSecret):
    # curl -X "POST" -H "Authorization: Basic ZjM4ZjAw...WYØMzE=" -d grant type=client credentials https ://accounts.spotify.com/api/token
    authUrl = "https://accounts.spotify.com/api/token"
    authHeader = {}
    authData = {}

    # Base64 Encode Client ID and Client Secret
    message = f"{clientID}:{clientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    # print(base64_message)

    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"
    res = requests.post(authUrl, headers=authHeader, data=authData)
    # print(res)
    responseObject = res.json()
    # print(json.dumps(responseObject, indent=2))
    accessToken = responseObject['access_token']
    return accessToken


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
