import os
from common import *

# ****************************************
#    Get netease playlist songs by id
# ****************************************

# Define palylist id
playlistIds = [
    553778357,  # 我喜欢的音乐
    # 7673625615,  # Favorite
    # 7673790351,  # Like
    # 7680312360,  # Nice
    # 7722735074,  # Hmm
    # 7741781941,  # One Hit
    # 7759490556,  # More Hits - 民谣
    # 7759804520,  # More Hits - 流行
    # 7690539370,  # Listening Artist
    # 7674298063,  # To Listen
    # 8075889883,  # High
]
# # Liked songs playlist id
# playlistIds = [553778357]


def getPlaylistIds(playlistNames):
    playlistIDs = []
    realPlaylistNames = []
    for playlistName in playlistNames:
        playlistPath = './files/playlists/playlist_songs_' + \
            playlistName + '_by ccgccc.json'
        customPlaylistPath = './files/playlists/custom_playlists/playlist_' + \
            playlistName + '.json'
        generatedPlaylistPath = './files/playlists/generated_playlists/' + \
            playlistName + '_playlist.json'
        if os.path.isfile(playlistPath):
            with open(playlistPath) as f:
                playlist = json.load(f)['playlist']
        elif os.path.isfile(customPlaylistPath):
            with open(customPlaylistPath) as f:
                playlist = json.load(f)
        elif os.path.isfile(generatedPlaylistPath):
            with open(generatedPlaylistPath) as f:
                playlist = json.load(f)
        else:
            print(playlistName, 'playlist not found...')
            continue
        playlistIDs.append(playlist['playlist']['id'])
        realPlaylistNames.append(playlist['playlist']['name'])
    return playlistIDs, realPlaylistNames


def main():
    # Read parameters from command line
    if len(sys.argv) >= 2:
        playlistIDs, realPlaylistNames = getPlaylistIds(sys.argv[1:])
        if playlistIDs != None and len(playlistIDs) > 0:
            playlistIds = playlistIDs

    for playlistId in playlistIds:
        playlist = getPlaylist(playlistId)
        playlistSongs = getPlaylistSongs(playlistId, addTs=True)
        playlistSongs['playlist'] = playlist

        playlistName = playlist['playlist']['name']
        if playlistName.startswith('Collection'):
            playlistName = playlistName.split(' - ')[0]
        fileName = 'playlists/playlist_songs_' + playlistName + \
            '_by ' + playlist['playlist']['creator']['nickname']
        # + '_bak_' + time.strftime("%Y-%m-%d")
        writeJsonToFile(playlistSongs, fileName)

        printPlaylists([playlist['playlist']])
        printSongs(playlistSongs['songs'], csvFileName=fileName)


if __name__ == '__main__':
    main()
