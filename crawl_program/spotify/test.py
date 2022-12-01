import os
import re
import json
from artists import *


def main():
    getArtistsFisrtAlbum()
    # renameTrackSheets()
    # checkArtists()


def getArtistsFisrtAlbum():
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


def checkArtists():
    for artist, artistInfo in artists.items():
        if not re.match(r'^[a-z1-9_]+$', artist):
            if not artist.endswith('-2'):
                print(artistInfo['name'] + ': ' + artist + ' wrong.')
    print('All checked.')


def renameTrackSheets():
    mypath = './files/trackSheets/temp/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f))]
    for file in files:
        print(file)
        print(file.replace('_Generated on 2022-11-30', ''))
        os.rename(file, file.replace('_Generated on 2022-11-30', ''))


if __name__ == '__main__':
    main()
