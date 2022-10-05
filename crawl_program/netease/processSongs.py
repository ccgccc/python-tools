from artists import *
from common import *

filterSongByName = True


def main():
    fileName = 'songs/' + artistToCrawl + '_allsongs_raw'
    allSongs = loadJsonFromFile(fileName)

    processSongs(allSongs, filterSongByName=filterSongByName)


def processSongs(allSongs, filterSongByName=True):
    # Filter albums tracks
    filterdSongs = []
    songNames = set()
    for song in allSongs:
        if filterSongByName:
            # ignore repeated songs by song name
            # not recomendded, sometimes repeated song names are alright, e.g. K歌之王 (国+粤)
            songName = song['name']
            if songName in songNames:
                continue
            else:
                songNames.add(songName)
        filterdSongs.append(song)

    fileName = 'songs/' + artistToCrawl + '_allsongs'
    writeJsonToFile(filterdSongs, fileName)
    printSongs(filterdSongs, fileName)
    return filterdSongs
