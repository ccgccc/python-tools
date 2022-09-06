import json
from utils.secrets import clientID, clientSecret
from spotifyFunc import *
from crawlPlaylist import writeToCsvFile

# ******************************
#   Crawl spotify liked songs
# ******************************


scope = [
    "user-library-read"
]
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
# API requests
# tracks = getUserSavedTracks(spotify, token, 50, 50)
tracks = getUserAllLikedSongs(spotify, token)
print(tracks)

fileName = './files/playlists/my_liked_songs'
# Write json to file
with open(fileName + '.json', 'w') as f:
    json.dump(tracks, f, ensure_ascii=False)

# Load json from file
# tracks = []
# with open(fileName + '.json') as f:
#     tracks = json.load(f)

csvFileName = fileName + '.csv'
writeToCsvFile(tracks['items'], csvFileName)
