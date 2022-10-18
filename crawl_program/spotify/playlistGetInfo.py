import json
from os import listdir
from os.path import isfile, join
from utils.secrets import clientID, clientSecret
from utils.auth import getAccessToken
from artists import artists, artistToCrawl
from spotifyFunc import *
from crawlPlaylists import crawlPlaylists

# ******************************
#   Crawl generated playlists
# ******************************

# All generated playlists
dir = './files/playlists/generated_playlists/'
# fileNames = [f for f in listdir(dir) if isfile(join(dir, f))]
# Specify crawling playlists
fileNames = [artistToCrawl + '_playlist.json']

playlistIds = []
for fileName in fileNames:
    # Get playlist
    playlist = []
    with open(dir + fileName) as f:
        playlist = json.load(f)
    playlistId = playlist['id']
    playlistIds.append(playlistId)

token = getAccessToken(clientID, clientSecret)
crawlPlaylists(token, playlistIds,
               './files/playlists/generated_playlists_info/')
