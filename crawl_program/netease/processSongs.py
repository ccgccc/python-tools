from artists import *
from common import *

# ****************************************
#  Process netease artist crawled tracks
# ****************************************

# Define if filter song by name
filterSongByName = True


def main():
    fileName = 'songs/' + artistToCrawl + '_allsongs_raw'
    allSongs = loadJsonFromFile(fileName)

    processSongs(artistToCrawl, allSongs, filterSongByName=filterSongByName)


def processSongs(artist, allSongs, filterSongByName=True):
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

    fileName = 'songs/' + artist + '_allsongs'
    writeJsonToFile(filterdSongs, fileName)
    printSongs(filterdSongs, fileName)
    return filterdSongs
