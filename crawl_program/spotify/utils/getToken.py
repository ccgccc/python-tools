from auth import *
from secrets import clientID, clientSecret

token = getAccessToken(clientID, clientSecret)
print(token)
# curl 'https://api.spotify.com/v1/playlists/6Ev0ju4qLsqSLznN7fjErt' -H "Authorization:Bearer BQBQS20cvbToq8OlQBFC44A4GqG75_L4hmfO9zAboidrbz_dvDy7_8s2a-EIthtK8y-o6df9b0Sg_-bqDWgTI7NmWpNcjb8TakzJkXxe1lvw6PUsb-s"
