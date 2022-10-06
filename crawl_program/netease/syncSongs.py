
import zhconv
from artists import *
from common import *
from specialSongs import *


def getSyncSongs(artist, spotifyTrackNames, isRemoveAlias=True,
                 isNeedPrompt=True, isOkPrompt=True, confirmOnceMode=True):
    # Get spotify playlist song names
    spotifyTrackOriginalNames = spotifyTrackNames[artist]
    if isRemoveAlias == True:
        spotifyTrackOriginalNames = [re.sub(r' \(.*', '', re.sub(r' - .*', '', track))
                                     for track in spotifyTrackOriginalNames]
    spotifyTrackNames = [zhconv.convert(track, 'zh-cn', update=specialSongNames.get(artist))
                         for track in spotifyTrackOriginalNames]
    print('------------------------------')
    print('Spotify Tracks:', len(spotifyTrackOriginalNames))
    print(spotifyTrackOriginalNames, '\n')

    # Get netease artist all songs
    fileName = 'songs/' + artist + '_allsongs'
    neteaseArtistSongs = loadJsonFromFile(fileName)
    neteaseArtistSongIds = {song['name']: song['id']
                            for song in neteaseArtistSongs}
    if specialSongIds.get(artist) != None:
        neteaseArtistSongIds = neteaseArtistSongIds \
            | specialSongIds.get(artist)  # since python 3.9
    if replaceSongIds.get(artist) != None:
        for k, v in replaceSongIds.get(artist).items():
            neteaseArtistSongIds[k] = v
    # Get sync songs name & id  # dictionary is ordered since python 3.7
    syncSongs = {name: neteaseArtistSongIds[name] for name in spotifyTrackNames
                 if neteaseArtistSongIds.get(name) != None}
    missingCount = len(spotifyTrackOriginalNames) - len(syncSongs)
    if missingCount > 0 and repeatedSongs.get(artist) != None:
        syncSongs = syncSongs | repeatedSongs.get(artist)
    print('------------------------------')
    print('Netease sync songs:', len(syncSongs))
    print(syncSongs, '\n')

    # Get missing songs
    missingSongs = set(spotifyTrackNames) - syncSongs.keys()
    missingSongs = sorted(
        list(missingSongs), key=lambda songName: spotifyTrackNames.index(songName))
    missingSongSpotifyNames = [spotifyTrackOriginalNames[spotifyTrackNames.index(songName)]
                               for songName in missingSongs]
    print('------------------------------')
    print('Netease missing songs:', missingCount)
    if missingCount > len(missingSongs):
        seen = set()
        dupes = [x for x in spotifyTrackOriginalNames
                 if x in seen or seen.add(x)]
        print('Duplicate:', dupes)
    if len(missingSongs) > 0:
        print('Missing:', missingSongSpotifyNames)
        print('Missing:', missingSongs)
    print('------------------------------')

    # Process netease sensitive words
    missingSongs = [song if sensitiveWords.get(song) == None else sensitiveWords[song]
                    for song in missingSongs]
    # Confirmation prompt
    if not isNeedPrompt or not isOkPrompt and len(missingSongs) == 0:
        return syncSongs, missingSongs
    while True:
        if len(missingSongs) > 0:
            continueMsg = input(
                'There is some missing songs. Do you want to continue? (y/n): ')
        else:
            continueMsg = input(
                'All songs can be synced. Press Y to continue. (y/n): ')
        if continueMsg == 'y' or continueMsg == 'Y':
            break
        elif confirmOnceMode or continueMsg == 'n' or continueMsg == 'N':
            sys.exit()
    return syncSongs, missingSongs
