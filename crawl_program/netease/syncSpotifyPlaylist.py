from os.path import isfile
from artists import *
from common import *
from syncSongs import getSyncSongs
from playlistCreate import generatePlaylist
from playlistRemoveSongs import playlistRomoveSongs
from playlistAddSongs import playlistAddSongs

# ************************************************************
#     Sync spotify most played songs playlists to netease
# ************************************************************

# Define artist here
artistToSyncList = [artistToCrawl]
# Define create playlist or update playlist
isCreate = True
# Read parameters from command line
if len(sys.argv) >= 2 and sys.argv[1] == 'update':
    isCreate = False
    if len(sys.argv) >= 3 and sys.argv[1] == 'all':
        artistToSyncList = list(generateArtists.keys())

# Define if update description
isUpdateDesc = True
# Define if need prompt
isNeedPrompt = True
# Define prompt if no missing songs
isOkPrompt = False
# Define if propmt updating missing description
isPromptDescMissing = False

# Define cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


def main():
    for artist in artistToSyncList:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Updating ' + artists[artist]['name'] + '...')
        syncSpotifyPlaylist(artist)


def syncSpotifyPlaylist(artist):
    # Prepare check
    if isCreate:
        if isfile('./files/playlists/generated_playlists/' + artist + '_playlist.json'):
            print('Alreay created playlist. Exit...')
            sys.exit()

    # Get spotify playlist
    with open('../spotify/files/playlists/generated_playlists_info/playlist_' +
              artists[artist]['name'] + ' Most Played Songs_by ccg ccc.json') as f:
        spotifyPlaylist = json.load(f)
    # Get sync songs
    seen = set()
    artistTrackList = []
    for track in spotifyPlaylist['tracks']['items']:
        trackName = track['track']['name']
        if trackName not in seen:
            artistTrackList.append(trackName)
            seen.add(trackName)
        else:
            artistTrackList.append(trackName + '_2_' +
                                   track['track']['artists'][0]['name'])
    spotifyTrackNames = {artist: artistTrackList}

    syncSongs, missingSongs = getSyncSongs(
        artist, spotifyTrackNames, isRemoveAlias=True, isNeedPrompt=isNeedPrompt, isOkPrompt=isOkPrompt)

    # Create or clear playlist
    if isCreate:
        # Create netease playlist
        playlist = generatePlaylist(artist, isUpdateDesc=False)
        playlistId = playlist['playlist']['id']
    else:
        # Get netease playlist
        fileName = 'playlists/generated_playlists/' + artist + '_playlist'
        if not isfile('./files/' + fileName + '.json'):
            print('Playlist not created yet. Please set isCreate to True.')
            sys.exit()
        playlist = loadJsonFromFile(fileName)
        playlistId = playlist['playlist']['id']
        # Remove playlist songs
        playlistRomoveSongs(playlistId)

    # Add songs & update playlist description
    playlistAddSongs(artist, playlistId, syncSongs, missingSongs,
                     spotifyPlaylist, isUpdateDesc=isUpdateDesc, isPromptDescMissing=isPromptDescMissing)
    # Get new playlist Info
    playlist = getPlaylist(playlistId)
    writeJsonToFile(playlist, 'playlists/generated_playlists/' +
                    artist + '_playlist')


if __name__ == '__main__':
    main()
