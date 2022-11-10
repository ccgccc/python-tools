import time
from artists import *
from common import *
from syncSongs import getSyncSongs

# ************************************************************
#  Add synced songs to netease playlists by spotify playlists
# ************************************************************


def main():
    headers['cookie'] = readFileContent('cookie.txt')

    # Get netease playlist
    playlist = loadJsonFromFile(
        'playlists/generated_playlists/' + artistToCrawl + '_playlist')
    playlistId = playlist['playlist']['id']

    # Get spotify playlist
    with open('../spotify/files/playlists/generated_playlists_info/playlist_' +
              artists[artistToCrawl]['name'] + ' Most Played Songs_by ccg ccc.json') as f:
        spotifyPlaylist = json.load(f)
    print(spotifyPlaylist['description'])
    spotifyTrackNames = {artistToCrawl: [track['track']['name']
                                         for track in spotifyPlaylist['tracks']['items']]}
    syncSongs, missingSongs = getSyncSongs(
        artistToCrawl, spotifyTrackNames, isRemoveAlias=True)

    playlistAddSongs(artistToCrawl, playlistId, syncSongs,
                     missingSongs, spotifyPlaylist)


def playlistAddSongs(artistToCrawl, playlistId, syncSongs, missingSongs, spotifyPlaylist,
                     isUpdateDesc=True, isPromptDescMissing=True, confirmOnceMode=False):
    syncSongIds = ','.join(
        reversed([str(list(song.values())[0]) for song in syncSongs]))
    addSongsToPlayList(playlistId, syncSongIds)

    if not isUpdateDesc:
        return
    # Update playlist description
    isDescMissingSongs = True
    if len(missingSongs) == 0:
        isDescMissingSongs = False
    if isPromptDescMissing:
        print('\n------------------------------')
        while True:
            continueMsg = input(
                'Do you want to add missing songs to playlist description? (y/n): ')
            if continueMsg == 'y' or continueMsg == 'Y':
                isDescMissingSongs = True
                break
            elif confirmOnceMode or continueMsg == 'n' or continueMsg == 'N':
                isDescMissingSongs = False
                break
    # isDescMissingSongs = True
    missingSongsPart = ('，Missing: ' + '、'.join(missingSongs)
                        ) if isDescMissingSongs else ''
    isUsingSpotifyTime = True
    captionPart = re.sub(r'.*(Generated.*)', r'\1', spotifyPlaylist['description']) if isUsingSpotifyTime else (
        'Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.')
    playlistDescription = artists[artistToCrawl]['name'] + '播放最多歌曲，根据Spotify播放量数据自动生成' + re.sub(
        r'.*(\(.*?\)).*', r'\1', spotifyPlaylist['description']) + missingSongsPart + '。' + captionPart
    # print(playlistDescription)
    updatePlaylistDesc(playlistId, playlistDescription)


if __name__ == '__main__':
    main()
