import os
from os import listdir
from os.path import isfile, join
from artists import *
from common import *

makeSure = False

if makeSure == False:
    print('Are you sure?')
    sys.exit()

headers['cookie'] = readFileContent('cookie.txt')

dir = './files/playlists/generated_playlists/'
fileNames = [f for f in listdir(dir) if isfile(join(dir, f))]
if artistToCrawl + '_playlist.json' not in fileNames:
    print('Playlist doesn\'t exitst. Exit...')
    sys.exit()

playlist = loadJsonFromFile(
    'playlists/generated_playlists/' + artistToCrawl + '_playlist')
playlistId = playlist['playlist']['id']

deletePlaylist(playlistId)

os.remove(dir + artistToCrawl + '_playlist.json')
