import json
from utils.secrets import clientID, clientSecret
from utils.auth import getAuthorizationToken
from spotifyFunc import *
from crawlPlaylists import writeToCsvFile, playlistStatistics

# ******************************
#   Crawl spotify liked songs
# ******************************

# Define if simple print
simplePrint = True


scope = [
    "user-library-read"
]
spotify, token = getAuthorizationToken(clientID, clientSecret, scope)
# API requests
# tracks = getUserSavedTracks(spotify, token, 50, 50)
tracks = getUserAllLikedSongs(spotify, token)
# print(tracks)
likedPlaylist = {}
likedPlaylist['name'] = '我点赞的歌曲'
likedPlaylist['tracks'] = tracks

fileName = './files/playlists/my_liked_songs'
# Write json to file
with open(fileName + '.json', 'w') as f:
    json.dump(tracks, f, ensure_ascii=False)
# Load json from file
# tracks = []
# with open(fileName + '.json') as f:
#     tracks = json.load(f)

csvFileName = fileName + '.csv'
writeToCsvFile(likedPlaylist, csvFileName, simplePrint=simplePrint)
playlistStatistics(likedPlaylist)
