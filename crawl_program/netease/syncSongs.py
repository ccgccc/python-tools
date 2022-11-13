
import zhconv
from artists import *
from common import *
from specialSongs import *

# **************************************************
#  Get spotify synced songs by artist & track names
# **************************************************


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

    # Get sync songs name & id
    seen = set()
    syncSongs = [{name: neteaseArtistSongIds.get(name)} for name in spotifyTrackNames
                 if neteaseArtistSongIds.get(name) != None and name not in seen and not seen.add(name)]
    print('------------------------------')
    print('Netease sync songs:', len(syncSongs))
    print(syncSongs, '\n')

    # Get missing songs
    missingSongs = set(spotifyTrackNames) - \
        {list(songDict.keys())[0] for songDict in syncSongs}
    missingSongs = sorted(
        list(missingSongs), key=lambda songName: spotifyTrackNames.index(songName))
    missingSongSpotifyNames = [spotifyTrackOriginalNames[spotifyTrackNames.index(songName)]
                               for songName in missingSongs]
    print('------------------------------')
    missingCount = len(spotifyTrackOriginalNames) - len(syncSongs)
    print('Netease missing songs:', missingCount)
    if missingCount > len(missingSongs):
        # Already modified duplicated names before, so  probably no duplicates here
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
    if not isNeedPrompt or not isOkPrompt and missingCount == 0:
        return syncSongs, missingSongSpotifyNames
    while True:
        if len(missingSongs) > 0:
            continueMsg = input(
                'There are some missing songs. Do you want to continue? (y/n): ')
        else:
            continueMsg = input(
                'All songs can be synced. Press Y to continue. (y/n): ')
        if continueMsg == 'y' or continueMsg == 'Y':
            break
        elif confirmOnceMode or continueMsg == 'n' or continueMsg == 'N':
            sys.exit()
    return syncSongs, missingSongs
