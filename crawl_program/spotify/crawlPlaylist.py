import requests
import json
from utils.auth import *
from secrets import *

# ******************************
#    Crawl spotify playlist
# ******************************

# Define playlist id here
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

print(token)
# curl 'https://api.spotify.com/v1/playlists/6Ev0ju4qLsqSLznN7fjErt' -H "Authorization:Bearer BQBQS20cvbToq8OlQBFC44A4GqG75_L4hmfO9zAboidrbz_dvDy7_8s2a-EIthtK8y-o6df9b0Sg_-bqDWgTI7NmWpNcjb8TakzJkXxe1lvw6PUsb-s"