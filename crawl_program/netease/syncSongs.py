
import zhconv
from artists import *
from common import *
from specialSongs import *


def getSyncSongs(artist, spotifyPlaylist, isRemoveAlias=True, isNeedPrompt=True, confirmOnceMode=True):
    spotifyTrackOriginalNames = list(
        map(lambda track: track['track']['name'], spotifyPlaylist['tracks']['items']))
    spotifyTrackOriginalNames = list(map(lambda track: re.sub(
        r' \(.*', '', re.sub(r' - .*', '', track)), spotifyTrackOriginalNames)) \
        if isRemoveAlias == True else spotifyTrackOriginalNames
    spotifyTrackNames = list(map(lambda track: zhconv.convert(
        track, 'zh-cn', update=specialSongNames.get(artist)), spotifyTrackOriginalNames))
    print('------------------------------')
    print('Spotify Tracks:', len(spotifyTrackOriginalNames))
    print(spotifyTrackOriginalNames, '\n')

    # Get netease all songs
    fileName = 'songs/' + artist + '_allsongs'
    neteaseArtistSongs = loadJsonFromFile(fileName)
    neteaseArtistSongIds = [{song['name']: song['id']}
                            for song in neteaseArtistSongs]
    if specialSongIds.get(artist) != None:
        neteaseArtistSongIds.extend(specialSongIds.get(artist))
    # print(neteaseArtistSongIds)
    # Get sync songs name & id
    syncSongs = [dict for dict in neteaseArtistSongIds
                 if list(dict.keys())[0] in spotifyTrackNames]
    syncSongs = sorted(
        syncSongs, key=lambda song: spotifyTrackNames.index(list(song.keys())[0]))
    if repeatedSongs.get(artist) != None:
        syncSongs.extend(repeatedSongs.get(artist))
    print('------------------------------')
    print('Netease sync songs:', len(syncSongs))
    print(syncSongs, '\n')

    # Get missing songs
    missingSongs = set(spotifyTrackNames) - \
        set(map(lambda songName: list(songName.keys())[0], syncSongs))
    missingSongs = sorted(
        list(missingSongs), key=lambda songName: spotifyTrackNames.index(songName))
    missingSongSpotifyNames = list(map(
        lambda songName: spotifyTrackOriginalNames[spotifyTrackNames.index(songName)], missingSongs))
    print('------------------------------')
    missingCount = len(spotifyTrackOriginalNames) - len(syncSongs)
    print('Netease missing songs:', missingCount)
    if missingCount > len(missingSongs):
        seen = set()
        dupes = [
            x for x in spotifyTrackOriginalNames if x in seen or seen.add(x)]
        print('Duplicate:', dupes)
    if len(missingSongs) > 0:
        print('Missing:', missingSongSpotifyNames)
        print('Missing:', missingSongs, '\n')
    print('------------------------------')

    # Confirmation prompt
    if not isNeedPrompt:
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
