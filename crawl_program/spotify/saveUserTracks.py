from utils.secrets import clientID, clientSecret
from utils.auth import getAuthorizationToken
from spotifyFunc import *

# ******************************
#   Save spotify liked tracks
# ******************************

# Define track ids, comma separated
trackIds = '3Wg5l1RDGRUDHs1sHKyPYn,6TpLVNUQFASvBOuPRFtCfC,5Hm71iOLGamb6uxaIuVKcJ,6xVw19NAlPn9oA638jzE3l,0yaSPL458ha2hn7WCEvjid,4hP61siAf05IPRZxcPAwAV,6j7hgKen4M3G1A9LZSEbbV,0q20lyhL4EvguaNF56dfbI,0awvYbOMrpO7q8kG4ApetV,4JheGaqICjOz0Ux2F1swfu,5Aj0agGNOflU5NYjOB2Dck,0JfCjl7Fw75wlhdJL92OMD,28GRiXeaaeDylP30k5z4jJ'


scope = [
    "user-library-modify"
]
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
# API requests
res = saveUserTracks(spotify, token, trackIds)
print(res)
