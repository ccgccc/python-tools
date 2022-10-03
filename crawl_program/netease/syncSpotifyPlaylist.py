import zhconv
from artists import *
from common import *
from specialSongs import *
from playlistCreate import generatePlaylist


def main():
    headers['cookie'] = readFileContent('cookie.txt')
    syncSongs, missingSongs = getSyncSongs(artistToCrawl, True)
    playlist = generatePlaylist(artistToCrawl)
    addSongsToPlayList(playlist['playlist']['id'], ','.join(
        reversed(list(map(lambda song: str(list(song.values())[0]), syncSongs)))))


def getSyncSongs(artist, isRemoveAlias=True):
    # Get spotify playlist
    with open('../spotify/files/playlists/generated_playlists_info/playlist_' +
              artists[artist]['name'] + ' Most Played Songs_by ccg ccc.json') as f:
        playlist = json.load(f)
    spotifyOriginTrackNames = list(
        map(lambda track: track['track']['name'], playlist['tracks']['items']))
    spotifyTrackNames = list(map(lambda track: re.sub(
        r' \(.*', '', re.sub(r' - .*', '', track)), spotifyOriginTrackNames)) if isRemoveAlias == True else spotifyOriginTrackNames
    spotifyTrackNames = list(map(lambda track: zhconv.convert(
        (track if track not in specialSongNames else specialSongNames[track]), 'zh-cn'), spotifyTrackNames))
    print('------------------------------')
    print('Spotify Tracks:', len(spotifyOriginTrackNames))
    print(spotifyOriginTrackNames, '\n')

    # Get netease all songs
    fileName = 'songs/' + artist + '_allsongs'
    neteaseAllSongs = loadJsonFromFile(fileName)
    # Get sync songs name & id
    syncSongs = [{song['name']: song['id']}
                 for song in neteaseAllSongs if song['name'] in spotifyTrackNames]
    syncSongs = sorted(
        syncSongs, key=lambda song: spotifyTrackNames.index(list(song.keys())[0]))
    print('------------------------------')
    print('Netease sync songs:', len(syncSongs))
    print(syncSongs, '\n')

    # Get missing songs
    missingSongs = set(spotifyTrackNames) - \
        set(map(lambda song: list(song.keys())[0], syncSongs))
    missingSongs = sorted(
        list(missingSongs), key=lambda song: spotifyTrackNames.index(song))
    print('------------------------------')
    print('Netease missing songs:', len(missingSongs))
    print(missingSongs if len(missingSongs) > 0 else None, '\n')
    print('------------------------------')

    # Confirmation prompt
    confirmOnceMode = True
    isContinue = False
    while not isContinue:
        if len(missingSongs) > 0:
            continueMsg = input(
                'There is some missing songs. Do you want to continue? (y/n): ')
        else:
            continueMsg = input(
                'All songs can be synced. Press Y to continue. (y/n): ')
        if continueMsg == 'y' or continueMsg == 'Y':
            isContinue = True
        elif confirmOnceMode or continueMsg == 'n' or continueMsg == 'N':
            sys.exit()
    return syncSongs, missingSongs


if __name__ == '__main__':
    main()
