import os
import re
import sys
import json
from artists import *


def main():
    getArtistsFisrtAlbum()
    # countTracks()
    # renameTrackSheets()
    # checkArtists()
    # removeTrackFiles()


def getArtistsFisrtAlbum():
    # ********** Get artists first album **********
    mypath = './files/albums/'
    files = [f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f)) and f.endswith('_albums.json')]
    artistAlbums = []
    for file in files:
        artist = file.replace('_albums.json', '')
        if artists.get(artist) == None:
            continue
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


def countTracks():
    artistNames = list(reversed([artistInfo['name']
                                 for artist, artistInfo in generateArtists.items()]))
    mypath = './files/playlists/generated_playlists_info/'
    files = [mypath + f for f in os.listdir(mypath)
             if os.path.isfile(os.path.join(mypath, f)) and f.endswith('.json')]
    files.sort(key=lambda file: artistNames.index(
        re.sub(".*playlist_(.*) Most.*", r'\1', file)))
    mypath2 = './files/playlists/'
    files2 = [mypath2 + f for f in os.listdir(mypath2)
              if os.path.isfile(os.path.join(mypath2, f)) and f.endswith('.json')
              and (f.find('Collection') > 0 or f.find('Hit') > 0)]
    files2.sort()
    files.extend(files2)
    count = 0
    allTracks = set()
    for file in files:
        with open(file) as f:
            playlist = json.load(f)
        tracksNum = len(playlist['tracks']['items'])
        count = count + tracksNum
        print(re.sub(".*playlist_(.*)_by ccg ccc\.json", r'\1', file) +
              ':  ' + str(tracksNum) + '  (Acc:' + str(count) + ')')
        allTracks = allTracks | {track['track']['id']
                                 for track in playlist['tracks']['items']}
    print('All: ', len(allTracks))


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


def removeTrackFiles():
    artist = 'dicky_cheung2'
    mypath = './files/'
    files = [os.path.join(dirpath, f)
             for (dirpath, dirnames, filenames) in os.walk(mypath)
             for f in filenames if f.startswith(artist) or f.startswith(artists[artist]['name'])]
    print('Removing:')
    print(files)
    if len(files) > 0:
        sureCheck()
        for file in files:
            os.remove(file)


def sureCheck():
    msg = input('Are you sure? Press Y to continue: ')
    if msg != 'y' and msg != 'Y':
        sys.exit()


if __name__ == '__main__':
    main()
