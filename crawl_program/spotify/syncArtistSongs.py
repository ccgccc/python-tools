import os
import re
import sys
import json
import time
import zhconv
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from netease.specialSongs import *
from netease.syncSongs import getSpotifyArtistTrackIdNames, getArtistSpecialSongNames
from artists import artists as spotifyArtists
from utils.auth import getAccessToken, getAuthorizationToken
from utils.secrets import clientID, clientSecret
from spotifyFunc import *
from crawlPlaylists import crawlSinglePlaylist
from playlistRemoveItems import playlistRemoveAllItems

# Define artist
artist = 'g_e_m'
# Define netease playlist
playlistName = 'Listening Artist'
playlistName = '好歌拾遗'
spotifyPlaylistName = '好歌拾遗'
# Define spotify playlist isPrivate
isPrivate = True
# Define is incremental
isIncremental = True
# Netease playlist file name
neteasePlaylistFileName = '../netease/files/playlists/playlist_songs_' + \
    playlistName + '_by ccgccc.json'
# Spotify playlist file name
spotifyPlaylistFileName = '../spotify/files/playlists/playlist_' + \
    spotifyPlaylistName + '_by ccg ccc.json'
if playlistName in ['Listening Artist']:
    isPrivate = True
    isIncremental = False
elif playlistName in ['好歌拾遗']:
    isPrivate = False
    isIncremental = True


# Get netease playlist
if not os.path.isfile(neteasePlaylistFileName):
    print('Netease playlist not created yet.')
    sys.exit()
with open(neteasePlaylistFileName) as f:
    neteasePlaylist = json.load(f)
neteaseAllSyncSongNames = [song['name']
                           for song in neteasePlaylist['songs']]
print('Netease all songs:', len(neteaseAllSyncSongNames))
print(neteaseAllSyncSongNames, '\n')

# Get artist all tracks
allTracks = []
with open('./files/tracks/' + artist + '_alltracks.json') as f:
    allTracks = json.load(f)
spotifyMatchTracks = {}
neteaseSongNameSet = set(neteaseAllSyncSongNames)
for track in allTracks:
    trackName = track['trackName']
    processedTrackName = re.sub(r' \(.*', '', re.sub(r' - .*', '', trackName))
    processedTrackName = zhconv.convert(
        processedTrackName, 'zh-cn', update=getArtistSpecialSongNames(artist, None))
    if processedTrackName in neteaseSongNameSet and spotifyMatchTracks.get(processedTrackName) == None:
        spotifyMatchTracks[processedTrackName] = track['trackUri']

# Get sync songs
syncSongs = []
missingSongs = []
for songName in neteaseAllSyncSongNames:
    if spotifyMatchTracks.get(songName) != None:
        syncSongs.append({songName: spotifyMatchTracks[songName]})
    else:
        missingSongs.append(songName)
print('Sync songs:', syncSongs, '\n')
print('Missing songs:', missingSongs, '\n')
sureCheck()

# Modify spotify playlist by netease sync songs
trackUriList = [list(dict.values())[0] for dict in syncSongs]
# Get spotify playlist id
if os.path.isfile(spotifyPlaylistFileName):
    with open(spotifyPlaylistFileName) as f:
        spotifyPlaylist = json.load(f)
        spotifyPlaylistId = spotifyPlaylist['id']
# Get spotify authorization token by scope and accessToken
scope = [
    "playlist-read-private",
    "playlist-modify-private",
    "playlist-modify-public"
]
spotify, authorizeToken = getAuthorizationToken(
    clientID, clientSecret, scope)
accessToken = getAccessToken(clientID, clientSecret)
if not isIncremental:
    # Remove playlist tracks
    playlistRemoveAllItems(
        accessToken, spotify, authorizeToken, spotifyPlaylistId, isPrivate=isPrivate)
    print()
# Add tracks to spotify playlist
addTracksToPlayList(spotify, authorizeToken,
                    spotifyPlaylistId, trackUriList)

print('Crawling playlist new info...')
crawlSinglePlaylist(accessToken, spotifyPlaylistId,
                    './files/playlists/', isPrivate=isPrivate, spotify=spotify, printPlaylist=False)
print('Done!')
