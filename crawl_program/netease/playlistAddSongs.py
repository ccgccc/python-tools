import os
import sys
import time
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from artists import *
from common import *
from specialSongs import *
from netease.syncSongs import getSyncSongs

# ************************************************************
#  Add synced songs to netease playlists by spotify playlists
# ************************************************************


def main():
    # Set baseUrl
    setBaseUrl()
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
    syncSongs, neteaseMissingSongs, missingSongSpotifyNames = getSyncSongs(
        artistToCrawl, spotifyTrackNames, isRemoveAlias=True)

    playlistAddSongs(artistToCrawl, playlistId, syncSongs,
                     neteaseMissingSongs, spotifyPlaylist)


def playlistAddSongs(artistToCrawl, playlistId, syncSongs, neteaseMissingSongs, spotifyPlaylist,
                     isUpdateDesc=True, isPromptDescMissing=True, confirmOnceMode=False):
    syncSongIds = ','.join(
        reversed([str(list(song.values())[0]) for song in syncSongs]))
    addSongsToPlayList(playlistId, syncSongIds)

    if not isUpdateDesc:
        return
    # Update playlist description
    isDescMissingSongs = True
    spotifyMissingTracks = []
    if spotifyMissingSongs.get(artistToCrawl) != None:
        spotifyMissingTracks = [list(dict.keys())[0]
                                for dict in spotifyMissingSongs[artistToCrawl]]
    if len(neteaseMissingSongs) == 0 and len(spotifyMissingTracks) == 0:
        isDescMissingSongs = False
    if isDescMissingSongs and isPromptDescMissing:
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
    missingSongsPart = ''
    if isDescMissingSongs:
        if len(neteaseMissingSongs) > 0:
            missingSongsPart = missingSongsPart + \
                '，Netease missing: ' + '、'.join(neteaseMissingSongs)
        missingSongsPart = missingSongsPart + '。'
        if len(spotifyMissingTracks) > 0:
            missingSongsPart = missingSongsPart + 'Added spotify missing songs: ' + \
                '、'.join(spotifyMissingTracks) + '. '
    isUsingSpotifyTime = True
    captionPart = re.sub(r'.*(Generated.*)', r'\1', spotifyPlaylist['description']) if isUsingSpotifyTime else (
        'Generated on ' + time.strftime("%Y-%m-%d") + ' by ccg.')
    playlistDescription = artists[artistToCrawl]['name'] + '播放最多歌曲，根据Spotify播放量数据自动生成' + re.sub(
        r'.*(\(.*?\)).*', r'\1', spotifyPlaylist['description']) + (missingSongsPart if missingSongsPart else '。') + captionPart
    # print(playlistDescription)
    updatePlaylistDesc(playlistId, playlistDescription)


if __name__ == '__main__':
    main()
