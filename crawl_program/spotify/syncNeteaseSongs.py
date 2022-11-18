import os
import re
import sys
import json
import zhconv
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from netease.artists import artists as neteaseArtists
from netease.specialSongs import *
from artists import artists as spotifyArtists
from utils.auth import getAccessToken, getAuthorizationToken
from utils.secrets import clientID, clientSecret
from spotifyFunc import *
from playlistRemoveItems import playlistRemoveAllItems

# ****************************************
#      Sync netease playlist songs
# ****************************************
# From spotify playlists(spotifySourcePlaylistNames),
# match songs in netease playlist(neteaseMatchPlaylistName)
# and sync them to another spotify playlist(spotifyPlaylistId)

# Read parameters from command line
if len(sys.argv) < 2:
    print('Missing playlist name parameter.')
    sys.exit()
# Define sync mode. 0: sync all, 1: sync non-playable songs.
syncMode = 0
# Read playlist name & get playlist id
playlistName = sys.argv[1]
with open('../spotify/files/playlists/playlist_' + playlistName + '_by ccg ccc.json') as f:
    spotifyPlaylist = json.load(f)
    spotifyPlaylistId = spotifyPlaylist['id']
# Define spotify playlist isPrivate
isPrivate = True
# Define is incremental
isIncremental = True
# Define if describe missing tracks
descMissingTracks = False
# Spotify source playlists names
spotifySourcePlaylistNames = [playlistName]
# Netease match playlist name
neteaseMatchPlaylistName = 'playlist_songs_' + playlistName + '_by ccgccc'
if playlistName in {'Favorite', 'Like'}:
    isPrivate = False
    spotifySourcePlaylistNames = [playlistName, 'Listening Artist']
elif playlistName in {'Nice', 'Hmm', 'To Listen'}:
    spotifySourcePlaylistNames = [playlistName, 'Listening Artist']
elif playlistName in {'One Hit'}:
    descMissingTracks = True
    spotifySourcePlaylistNames = [playlistName]
elif playlistName in {'Netease Non-playable'}:
    syncMode = 1
    spotifySourcePlaylistNames = ['Favorite', 'Like']
else:
    print('Playlist name not defined.')
    sys.exit()
print('--------------------')
print('*** Sync Info ***')
print('Sync Mode:', syncMode,
      '(' + ('All' if syncMode == 0 else 'Non-playable') + ')')
print('Playlist:', playlistName if 'playlistName' in globals() else spotifyPlaylistId)
print('IsPrivate:', isPrivate)
print('IsIncremental:', isIncremental)
print('DescMissingTracks:', descMissingTracks)
print('SpotifySourcePlaylistNames:', spotifySourcePlaylistNames)
print('NeteaseMatchPlaylistName:', neteaseMatchPlaylistName)
print('--------------------')


def main():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Get netease playlist
    neteasePlaylistFileName = '../netease/files/playlists/' + \
        neteaseMatchPlaylistName + '.json'
    if not os.path.isfile(neteasePlaylistFileName):
        print('Playlist not created yet.')
        sys.exit()
    with open(neteasePlaylistFileName) as f:
        neteasePlaylist = json.load(f)
    if syncMode == 0:
        neteaseAllSyncSongNames = [song['name']
                                   for song in neteasePlaylist['songs']]
        print('Netease all songs:', len(neteaseAllSyncSongNames))
        print(neteaseAllSyncSongNames, '\n')
    elif syncMode == 1:
        # Get netease all non-playable songs
        neteasePlaylistSongs = neteasePlaylist['songs']
        neteasePlaylistPrivileges = neteasePlaylist['privileges']
        neteaseAllSyncSongs = []
        neteaseNoCopyrightSongs = []
        neteaseNeedPurchaseSongs = []
        for i in range(len(neteasePlaylistSongs)):
            if neteasePlaylistPrivileges[i]['st'] < 0:
                neteaseNoCopyrightSongs.append(neteasePlaylistSongs[i])
                neteaseAllSyncSongs.append(neteasePlaylistSongs[i])
                continue
            # if neteasePlaylistSongs[i]['fee'] == 4:
            # TODO reliable?? hahaha
            if neteasePlaylistSongs[i]['fee'] == 4 and (
                    neteasePlaylistPrivileges[i]['flag'] % 4 == 0
                    or neteasePlaylistPrivileges[i]['flag'] == 8197):
                # print(neteasePlaylistSongs[i]['name'], neteasePlaylistPrivileges[i]['flag'])
                neteaseNeedPurchaseSongs.append(neteasePlaylistSongs[i])
                neteaseAllSyncSongs.append(neteasePlaylistSongs[i])
        print('------------------------------')
        print('Netease no copyright songs:', len(neteaseNoCopyrightSongs))
        print({song['id']: song['name']
              for song in neteaseNoCopyrightSongs}, '\n')
        print('Netease need purchase songs:', len(neteaseNeedPurchaseSongs))
        print({song['id']: song['name']
               for song in neteaseNeedPurchaseSongs}, '\n')
        neteaseAllSyncSongNames = {song['name']
                                   for song in neteaseAllSyncSongs}
    else:
        print('Sync mode not supported. Exiting...')
        sys.exit()

    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Get spotify playlists & artist track names
    spotifyArtistTrackNames = {}
    # Iterate playlists
    for spotifyPlaylistName in spotifySourcePlaylistNames:
        with open('../spotify/files/playlists/playlist_' + spotifyPlaylistName + '_by ccg ccc.json') as f:
            spotifyPlaylist = json.load(f)
        # Classify playlist tracks by artist
        curSpotifyArtistTrackNames = getSpotifyArtistTrackNames(
            spotifyPlaylistName, spotifyPlaylist['tracks'])
        # Iterate artists
        for artist, spotifyTracks in curSpotifyArtistTrackNames.items():
            # Process spotify track names for each playlist & artist
            spotifyProcessedTracks = [{list(dict.keys())[0]: re.sub(r' \(.*', '', re.sub(r' - .*', '', list(dict.values())[0]))}
                                      for dict in spotifyTracks]
            spotifyProcessedTracks = [{list(dict.keys())[0]: zhconv.convert(list(dict.values())[0], 'zh-cn', update=specialSongNames.get(artist))}
                                      for dict in spotifyProcessedTracks]
            if spotifyArtistTrackNames.get(artist) != None:
                spotifyArtistTrackNames[artist].extend(spotifyProcessedTracks)
            else:
                spotifyArtistTrackNames[artist] = spotifyProcessedTracks
    spotifyTrackNames = []
    for artist, trackNames in spotifyArtistTrackNames.items():
        if spotifyArtistTrackNames.get(artist) != None:
            spotifyTrackNames.extend(
                spotifyArtistTrackNames.get(artist))
    print('------------------------------')
    print('Spotify processed track names:', len(spotifyTrackNames))
    print([list(track.values())[0] for track in spotifyTrackNames], '\n')

    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('------------------------------')
    # Get matching songs from netease
    spotifyTracksFromNetease = [dict for dict in spotifyTrackNames if list(
        dict.values())[0] in neteaseAllSyncSongNames]
    print('Spotify sync tracks from netease:',
          len(spotifyTracksFromNetease))
    print([list(track.values())[0]
          for track in spotifyTracksFromNetease])
    if descMissingTracks:
        spotifyMissingTracks = [songName for songName in reversed(neteaseAllSyncSongNames)
                                if songName not in {list(dict.values())[0] for dict in spotifyTracksFromNetease}]
        print('\nSpotify missing tracks:', len(spotifyMissingTracks))
        print(spotifyMissingTracks)
        missingSongs = []
        for song in reversed(neteasePlaylist['songs']):
            for missingSongName in spotifyMissingTracks:
                if missingSongName == song['name']:
                    songArtists = '_'.join(artist['name']
                                           for artist in song['ar'])
                    missingSongs.append(
                        missingSongName + '(' + songArtists + ')')
        missingSongsStr = '、'.join(missingSongs)
        print(missingSongsStr)

    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    trackUriList = [list(dict.keys())[0] for dict in spotifyTracksFromNetease]
    # Get spotify authorization token by scope and accessToken
    if isPrivate:
        scope = [
            "playlist-read-private",
            "playlist-modify-private",
            "playlist-modify-public"
        ]
        spotify, authorizeToken = getAuthorizationToken(
            clientID, clientSecret, scope)
        accessToken = None
    else:
        accessToken = getAccessToken(clientID, clientSecret)
        spotify = None
        authorizeToken = None
    if isIncremental:
        # Get incremental sync trackuri
        playlist = getPlaylistAndAllTracks(
            accessToken, spotifyPlaylistId, isPrivate=isPrivate, spotify=spotify)
        playlistTrackUris = [track['track']['uri']
                             for track in playlist['tracks']['items']]
        trackUriList = [
            trackUri for trackUri in trackUriList if trackUri not in playlistTrackUris]
    else:
        # Remove playlist songs
        playlistRemoveAllItems(
            accessToken, spotify, authorizeToken, spotifyPlaylistId, isPrivate=isPrivate)
        print()
    # Check before sync
    print('------------------------------')
    print('Incremental:', isIncremental)
    print('DescMissingTracks:', descMissingTracks)
    print('To sync tracks:', len(trackUriList))
    print('track uris:', trackUriList)
    print('track names:', [list(dict.values())[0] for dict in spotifyTracksFromNetease
                           if list(dict.keys())[0] in trackUriList])
    if descMissingTracks:
        playlistDescription = 'Sync between spotify and netease. Spotify missing: ' + \
            missingSongsStr + '.'
        res = updatePlayList(spotify, authorizeToken, spotifyPlaylistId,
                             playlistName, playlistDescription, True)
        print('Response:', res)
    if len(trackUriList) == 0:
        print('\nNothing to sync. Exit...')
        sys.exit()
    msg = input(
        '\nAre you sure to sync these tracks? Press Y to continue. (y/n): ')
    if msg != 'y' and msg != 'n':
        sys.exit()
    print()
    # Add tracks to spotify playlist
    if not isPrivate:
        scope = "playlist-modify-public"
        spotify, authorizeToken = getAuthorizationToken(
            clientID, clientSecret, scope)
    addTracksToPlayList(spotify, authorizeToken,
                        spotifyPlaylistId, trackUriList)


def getSpotifyArtistTrackNames(spotifyPlaylistName, spotifyPlaylistTracks):
    # Print spoitfy playlist track names
    print('------------------------------')
    allPlaylistTrackNames = [track['track']['name']
                             for track in spotifyPlaylistTracks['items']]
    totalPlaylistTracks = len(allPlaylistTrackNames)
    print('Spotify playlist track names (' + spotifyPlaylistName + '): ',
          '(Total ', totalPlaylistTracks, ')', sep='')
    print(allPlaylistTrackNames, '\n')

    # Get spotify artists IDs
    spotifyArtistIds = {v['artistId']: k for k, v in spotifyArtists.items()}
    spotifyArtistIdsSet = spotifyArtistIds.keys()
    # Get spotify artist track names, like this: {'artist': ['trackname', 'trackname2']}
    spotifyArtistTrackNames = {k: [] for k, v in spotifyArtists.items()}
    artistsNotFound = set()
    for track in spotifyPlaylistTracks['items']:
        isArtistFound = False
        for trackArtist in track['track']['artists']:
            trackArtistId = trackArtist['id']
            if trackArtist['id'] in spotifyArtistIdsSet:
                artist = spotifyArtistIds.get(trackArtistId)
                if spotifyArtistTrackNames.get(artist) != None:
                    spotifyArtistTrackNames[artist].append(
                        {track['track']['uri']: track['track']['name']})
                    isArtistFound = True
                    break
        if not isArtistFound:
            artistsNotFound.add(
                '_'.join([artists['name'] for artists in track['track']['artists']]))
    # Remove empty artists
    for k in list(spotifyArtistTrackNames.keys()):
        if len(spotifyArtistTrackNames[k]) == 0:
            del spotifyArtistTrackNames[k]
    totalTrackNames = sum([len(v) for k, v in spotifyArtistTrackNames.items()])
    # print('------------------------------')
    # print('Spotify playlist track names(classified): ',
    #       '(Total ', totalTrackNames, ')', sep='')
    # print(spotifyArtistTrackNames, '\n')

    if (len(artistsNotFound) > 0):
        print('------------------------------')
        print('These artists are not crawled yet, please crawl them first:',
              artistsNotFound, '\n')
        sys.exit()
    if (totalTrackNames != totalPlaylistTracks):
        print('------------------------------')
        print('Track numbers don\'t match, please check', artistsNotFound)
        sys.exit()
    return spotifyArtistTrackNames


if __name__ == '__main__':
    main()
