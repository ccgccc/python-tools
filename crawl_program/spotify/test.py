import os
import json
from artists import *

# ********** Get artists first album **********
mypath = './files/albums/'
files = [f for f in os.listdir(mypath)
         if os.path.isfile(os.path.join(mypath, f)) and f.endswith('_albums.json')]
artistAlbums = []
for file in files:
    artist = file.replace('_albums.json', '')
    with open(mypath + file) as f:
        albums = json.load(f)
    artistAlbums.append({'artist': artist, 'name': artists[artist]['name'],
                        'firstAlbum': albums[0]['name'], 'releaseDate': albums[0]['release_date']})
    # print(artist, artists[artist]['name'], albums[0]
    #     ['name'], albums[0]['release_date'], sep=', ')

artistAlbums = sorted(artistAlbums, key=lambda album: album['releaseDate'])
for artistAlbum in artistAlbums:
    print(artistAlbum['releaseDate'], artistAlbum['name'],
          artistAlbum['artist'], artistAlbum['firstAlbum'], sep=', ')
