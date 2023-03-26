import os
import re
import sys
import json
import zhconv
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from netease.artists import artists as neteaseArtists
from netease.specialSongs import *
from netease.syncSongs import getArtistSpecialSongNames
from artists import *
from utils.auth import getAccessToken, getAuthorizationToken
from utils.secrets import clientID, clientSecret
from spotifyFunc import *
from crawlPlaylists import crawlSinglePlaylist
from playlistRemoveItems import playlistRemoveAllItems

# Define artist
artist = artistToCrawl
# Read parameters from command line
if len(sys.argv) >= 2:
    neteasePlaylistName = sys.argv[1]
    if len(sys.argv) >= 3:
        artist = sys.argv[2]
else:
    print('Parameter error! Exit...')
    sys.exit()

# Define netease & spotify playlist
# neteasePlaylistName = 'Listening Artist'
# spotifyPlaylistName = 'Listening'
# neteasePlaylistName = '好歌拾遗'
# spotifyPlaylistName = '好歌拾遗'
# Define spotify playlist isPrivate
isPrivate = True
# Define is incremental
isIncremental = True
if neteasePlaylistName in ['Listening Artist']:
    spotifyPlaylistName = 'Listening'
    isPrivate = True
    isIncremental = False
elif neteasePlaylistName in ['好歌拾遗']:
    spotifyPlaylistName = '好歌拾遗'
    isPrivate = False
    isIncremental = True
# Netease playlist file name
neteasePlaylistFileName = '../netease/files/playlists/playlist_songs_' + \
    neteasePlaylistName + '_by ccgccc.json'
# Spotify playlist file name
spotifyPlaylistFileName = '../spotify/files/playlists/playlist_' + \
    spotifyPlaylistName + '_by ccg ccc.json'


# Get spotify playlist info
if os.path.isfile(spotifyPlaylistFileName):
    with open(spotifyPlaylistFileName) as f:
        spotifyPlaylist = json.load(f)
        spotifyPlaylistId = spotifyPlaylist['id']
        spotifyPlaylistTrackIds = {trackItem['track']['uri']
                                   for trackItem in spotifyPlaylist['tracks']['items']}
print('Spotify all tracks:', len(spotifyPlaylist['tracks']['items']))
print({trackItem['track']['name']
      for trackItem in spotifyPlaylist['tracks']['items']}, '\n')

# Get netease playlist
print('--------------------')
if not os.path.isfile(neteasePlaylistFileName):
    print('Netease playlist not created yet.')
    sys.exit()
with open(neteasePlaylistFileName) as f:
    neteasePlaylist = json.load(f)
neteaseAllSyncSongNames = [song['name'] for song in neteasePlaylist['songs']
                           if neteaseArtists[artist]['artistId'] in {ar['id'] for ar in song['ar']}]
print('Netease all sync songs:', len(neteaseAllSyncSongNames))
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
print('--------------------')
syncSongs = []
missingSongs = []
for songName in neteaseAllSyncSongNames:
    spotifyMatchTrackId = spotifyMatchTracks.get(songName)
    if isIncremental and spotifyMatchTrackId in spotifyPlaylistTrackIds:
        continue
    if spotifyMatchTrackId != None:
        syncSongs.append({songName: spotifyMatchTrackId})
    else:
        missingSongs.append(songName)
print('Sync songs(' + str(len(syncSongs)) + '):', syncSongs, '\n')
print('Missing songs(' + str(len(missingSongs)) + '):', missingSongs, '\n')
sureCheck()

# Modify spotify playlist by netease sync songs
trackUriList = [list(dict.values())[0] for dict in syncSongs]
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
