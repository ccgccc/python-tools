
import zhconv
from artists import *
from common import *
from specialSongs import *


def getSyncSongs(artist, isRemoveAlias=True, isNeedPrompt=True, confirmOnceMode=True):
    # Get spotify playlist
    with open('../spotify/files/playlists/generated_playlists_info/playlist_' +
              artists[artist]['name'] + ' Most Played Songs_by ccg ccc.json') as f:
        playlist = json.load(f)
    spotifyTrackOriginalNames = list(
        map(lambda track: track['track']['name'], playlist['tracks']['items']))
    spotifyTrackNames = list(map(lambda track: re.sub(
        r' \(.*', '', re.sub(r' - .*', '', track)), spotifyTrackOriginalNames)) \
        if isRemoveAlias == True else spotifyTrackOriginalNames
    spotifyTrackNames = list(map(lambda track: zhconv.convert(
        track, 'zh-cn', update=specialSongNames), spotifyTrackNames))
    print('------------------------------')
    print('Spotify Tracks:', len(spotifyTrackOriginalNames))
    print(spotifyTrackOriginalNames, '\n')

    # Get netease all songs
    fileName = 'songs/' + artist + '_allsongs'
    neteaseAllSongs = loadJsonFromFile(fileName)
    neteaseAllSongIds = [{song['name']: song['id']}
                         for song in neteaseAllSongs]
    neteaseAllSongIds.append(specialSongIds)
    # Get sync songs name & id
    syncSongs = [dict for dict in neteaseAllSongIds
                 if list(dict.keys())[0] in spotifyTrackNames]
    syncSongs = sorted(
        syncSongs, key=lambda song: spotifyTrackNames.index(list(song.keys())[0]))
    syncSongs.append(repeatedSongs[artist])
    print('------------------------------')
    print('Netease sync songs:', len(syncSongs))
    print(syncSongs, '\n')

    # Get missing songs
    missingSongs = set(spotifyTrackNames) - \
        set(map(lambda song: list(song.keys())[0], syncSongs))
    missingSongs = sorted(
        list(missingSongs), key=lambda song: spotifyTrackNames.index(song))
    print('------------------------------')
    print('Netease missing songs:',
          len(spotifyTrackOriginalNames) - len(syncSongs))
    print('Missing:', missingSongs if len(missingSongs) > 0 else None, '\n')
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
