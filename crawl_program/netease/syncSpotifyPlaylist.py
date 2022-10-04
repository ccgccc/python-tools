from artists import *
from common import *
from os import listdir
from os.path import isfile, join
from syncSongs import getSyncSongs
from playlistCreate import generatePlaylist
from playlistRemoveSongs import playlistRomoveSongs
from playlistAddSongs import playlistAddSongs


# Define create playlist or update playlist
isCreate = True
# Defin cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


# Prepare check
if isCreate:
    dir = './files/playlists/generated_playlists/'
    fileNames = [f for f in listdir(dir) if isfile(join(dir, f))]
    if artistToCrawl + '_playlist.json' in fileNames:
        print('Alreay created playlist. Exit...')
        sys.exit()

# Get spotify playlist
with open('../spotify/files/playlists/generated_playlists_info/playlist_' +
          artists[artistToCrawl]['name'] + ' Most Played Songs_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
# Get sync songs
syncSongs, missingSongs = getSyncSongs(
    artistToCrawl, spotifyPlaylist, isRemoveAlias=True)

# Create or clear playlist
if isCreate:
    # Create playlist
    playlist = generatePlaylist(artistToCrawl, isUpdateDesc=False)
    playlistId = playlist['playlist']['id']
else:
    # Get netease playlist
    fileName = 'playlists/generated_playlists/' + artistToCrawl + '_playlist'
    if not isfile('./files/' + fileName + '.json'):
        print('Playlist not created yet. Please set isCreate to True.')
        sys.exit()
    playlist = loadJsonFromFile(fileName)
    playlistId = playlist['playlist']['id']
    # Remove playlist songs
    playlistRomoveSongs(playlistId)

# Add songs & update playlist description
playlistAddSongs(playlistId, syncSongs, missingSongs, spotifyPlaylist)
# Get new playlist Info
playlist = getPlaylist(playlistId)
writeJsonToFile(playlist, 'playlists/generated_playlists/' +
                artistToCrawl + '_playlist')
