import json
from spotifyFunc import *

# ******************************
#    Crawl spotify playlist
# ******************************

# Define playlist id here
playlistID = "6Ev0ju4qLsqSLznN7fjErt"
# playlistID = "7w3Y21vKZuLLq1huUuEWZZ"


# API requests
playlist = getPlaylistAndAllTracks(playlistID)
# print(tracklist)
# Write json to file
with open('./files/playlist_' + playlist['name'] + '_by ' + playlist['owner']['display_name'] + '.json', 'w') as f:
    json.dump(playlist, f, ensure_ascii=False)

count = 0
for t in playlist['tracks']['items']:
    print('--------------------')
    count = count + 1
    print(str(count))
    print('Track:   ' + t['track']['name'])
    print('Album:   ' + t['track']['album']['name'] +
          ' (' + t['track']['album']['release_date'] + ")")
    print('Artists: ', end='')
    artists = t['track']['artists']
    for i in range(len(artists)):
        print(artists[i]['name'], end='')
        print(', ', end='') if i < len(artists) - 1 else print()

# print(token)
# curl 'https://api.spotify.com/v1/playlists/6Ev0ju4qLsqSLznN7fjErt' -H "Authorization:Bearer BQBQS20cvbToq8OlQBFC44A4GqG75_L4hmfO9zAboidrbz_dvDy7_8s2a-EIthtK8y-o6df9b0Sg_-bqDWgTI7NmWpNcjb8TakzJkXxe1lvw6PUsb-s"
