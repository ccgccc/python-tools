import os
import re
import sys
import json
import time
import zhconv
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from netease.specialSongs import *
from netease.syncSongs import getSpotifyArtistTrackIdNames, getArtistSpecialSongNames
from artists import artists as spotifyArtists
from utils.auth import getAccessToken, getAuthorizationToken
from utils.secrets import clientID, clientSecret
from spotifyFunc import *
from crawlPlaylists import crawlSinglePlaylist
from playlistRemoveItems import playlistRemoveAllItems

# ****************************************
#      Sync netease playlist songs
# ****************************************
# From spotify playlists(spotifySourcePlaylistNames),
# match songs in netease playlist(neteaseMatchPlaylistName)
# and sync them to another spotify playlist(spotifyPlaylistId)
# Note: spotify歌单有重名歌曲的时候只会同步其中一个

# Read parameters from command line
if len(sys.argv) < 2:
    print('Missing playlist name parameter.')
    sys.exit()
# Define sync mode. 0: sync all, 1: sync non-playable songs.
syncMode = 0
# Read playlist name & get playlist id
playlistName = sys.argv[1]
playlistFileName = '../spotify/files/playlists/playlist_' + \
    playlistName + '_by ccg ccc.json'
if os.path.isfile(playlistFileName):
    with open(playlistFileName) as f:
        spotifyPlaylist = json.load(f)
        spotifyPlaylistId = spotifyPlaylist['id']
# Define spotify playlist isPrivate
isPrivate = True
# Define is incremental
isIncremental = True
# Define if update description
isUpdateDesc = False
# Spotify source playlists names
spotifySourcePlaylistNames = [playlistName]
# Netease match playlist name
neteaseMatchPlaylistName = 'playlist_songs_' + playlistName + '_by ccgccc'
if playlistName in {'Favorite', 'Like'}:
    isPrivate = False
    isIncremental = True
    spotifySourcePlaylistNames = [playlistName, 'Listening Artist', '好歌拾遗']
    isUpdateDesc = True
    # spotifySourcePlaylistNames = [playlistName, 'Collection 1']
    # # Update description
    # isUpdateDesc = True
    # spotifySourcePlaylistNames = [playlistName]
elif playlistName in {'Nice', 'Hmm', 'To Listen'}:
    isPrivate = True
    isIncremental = True
    spotifySourcePlaylistNames = [playlistName, 'Listening Artist', '好歌拾遗']
    isUpdateDesc = True
    # spotifySourcePlaylistNames = [playlistName, 'Collection 1']
    # # Update description
    # isUpdateDesc = True
    # spotifySourcePlaylistNames = [playlistName]
elif playlistName in {'好歌拾遗', 'One Hit', 'More Hits - 民谣', 'More Hits - 流行'}:
    isUpdateDesc = True
    spotifySourcePlaylistNames = [playlistName]
elif playlistName in {'High'}:
    isIncremental = True
    isUpdateDesc = False
    spotifySourcePlaylistNames = ['Listening Artist']
    # spotifySourcePlaylistNames = ['Favorite', 'Like', 'Nice', '张学友']
elif playlistName.startswith('Collection'):
    isUpdateDesc = True
    spotifySourcePlaylistNames = [playlistName]
elif playlistName in {'Netease Non-playable'}:
    syncMode = 1
    neteaseMatchPlaylistName = 'playlist_songs_ccgccc喜欢的音乐_by ccgccc'
    spotifySourcePlaylistNames = ['Favorite', 'Like']
elif playlistName in {'Listening', 'Listening Artist'}:
    syncMode = 1
    isIncremental = False
    neteaseMatchPlaylistName = 'playlist_songs_Listening Artist_by ccgccc'
    # spotifySourcePlaylistNames = ['Listening Artist']
    syncMode = 0
    spotifySourcePlaylistNames = ['张学友']
print('--------------------')
print('*** Sync Info ***')
print('Sync Mode:', syncMode,
      '(' + ('All' if syncMode == 0 else 'Non-playable') + ')')
print('Playlist:', playlistName)
print('IsPrivate:', isPrivate)
print('IsIncremental:', isIncremental)
print('IsUpdateDesc:', isUpdateDesc)
print('SpotifySourcePlaylistNames:', spotifySourcePlaylistNames)
print('NeteaseMatchPlaylistName:', neteaseMatchPlaylistName)
print('--------------------')


def main():
    # ********** Get netease sync songs **********
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Get netease playlist
    neteasePlaylistFileName = '../netease/files/playlists/' + \
        neteaseMatchPlaylistName + '.json'
    if not os.path.isfile(neteasePlaylistFileName):
        print('Netease playlist not created yet.')
        sys.exit()
    with open(neteasePlaylistFileName) as f:
        neteasePlaylist = json.load(f)
    if syncMode == 0:  # Sync All: Get netease all songs
        neteaseAllSyncSongNames = [song['name']
                                   for song in neteasePlaylist['songs']]
        print('Netease all songs:', len(neteaseAllSyncSongNames))
        print(neteaseAllSyncSongNames, '\n')
    elif syncMode == 1:  # Sync non-playable: Get netease all non-playable songs
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
        neteaseAllSyncSongNames = [song['name']
                                   for song in neteaseAllSyncSongs]
    else:
        print('Sync mode not supported. Exiting...')
        sys.exit()

    # ********** Get and process spotify artist track names for each playlist **********
    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    spotifyArtistTrackIdNames = {}
    # Iterate playlists
    for spotifyPlaylistName in spotifySourcePlaylistNames:
        with open('../spotify/files/playlists/playlist_' + spotifyPlaylistName + '_by ccg ccc.json') as f:
            spotifyPlaylist = json.load(f)
        # Classify playlist tracks by artist
        curSpotifyArtistTrackIdNames = getSpotifyArtistTrackIdNames(
            spotifyPlaylistName, spotifyPlaylist['tracks'], spotifyArtists)
        # Iterate artists
        for artist, spotifyTrackIdNames in curSpotifyArtistTrackIdNames.items():
            # Process spotify track names for each playlist & artist
            spotifyProcessedTracks = [{list(dict.keys())[0]: re.sub(r' \(.*', '', re.sub(r' - .*', '', list(dict.values())[0]))}
                                      for dict in spotifyTrackIdNames]
            spotifyProcessedTracks = [{list(dict.keys())[0]: zhconv.convert(list(dict.values())[0], 'zh-cn', update=getArtistSpecialSongNames(artist, playlistName))}
                                      for dict in spotifyProcessedTracks]
            if spotifyArtistTrackIdNames.get(artist) != None:
                spotifyArtistTrackIdNames[artist].extend(
                    spotifyProcessedTracks)
            else:
                spotifyArtistTrackIdNames[artist] = spotifyProcessedTracks
    spotifyAllTrackIdNames = []
    for artist, trackIdNames in spotifyArtistTrackIdNames.items():
        if spotifyArtistTrackIdNames.get(artist) != None:
            spotifyAllTrackIdNames.extend(
                spotifyArtistTrackIdNames.get(artist))
    print('------------------------------')
    print('Spotify processed track names:', len(spotifyAllTrackIdNames))
    print([list(track.values())[0] for track in spotifyAllTrackIdNames], '\n')

    # ********** Get spotify's matching & missing songs from netease **********
    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('------------------------------')
    # seen = set()
    # dupes = [name for name in neteaseAllSyncSongNames if name in seen or seen.add(name)]
    # print(dupes)
    # spotifyTracksFromNetease = {list(dict.keys())[0]: list(dict.values())[0] for dict in spotifyAllTrackIdNames if list(
    #     dict.values())[0] in neteaseAllSyncSongNames}
    spotifyTracksFromNetease = [dict for dict in spotifyAllTrackIdNames if list(
        dict.values())[0] in neteaseAllSyncSongNames]
    print('Spotify sync tracks from netease:',
          len(spotifyTracksFromNetease))
    print([list(track.values())[0]
          for track in spotifyTracksFromNetease])
    if isUpdateDesc:
        spotifyMissingTracks = [songName for songName in reversed(neteaseAllSyncSongNames)
                                if songName not in {list(dict.values())[0] for dict in spotifyTracksFromNetease}]
        print('\nSpotify missing tracks:', len(spotifyMissingTracks))
        print(spotifyMissingTracks)
        missingSongs = []
        for song in reversed(neteasePlaylist['songs']):
            for missingSongName in spotifyMissingTracks:
                if missingSongName == song['name']:
                    songArtists = '/'.join(artist['name']
                                           for artist in song['ar'][:3])
                    missingSongs.append(
                        missingSongName + '(' + songArtists + ('等' if len(song['ar']) > 3 else '') + ')')
        missingSongsStr = '、'.join(missingSongs) if len(
            missingSongs) > 0 else ''
        print('Missing:', missingSongsStr)

    # ********** Modify spotify playlist by netease sync songs **********
    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    trackUriList = [list(dict.keys())[0] for dict in spotifyTracksFromNetease]
    # Get spotify authorization token by scope and accessToken
    if isPrivate or isUpdateDesc:
        scope = [
            "playlist-read-private",
            "playlist-modify-private",
            "playlist-modify-public"
        ]
        spotify, authorizeToken = getAuthorizationToken(
            clientID, clientSecret, scope)
    else:
        spotify = None
        authorizeToken = None
    accessToken = getAccessToken(clientID, clientSecret)
    if isIncremental:
        # Get incremental sync trackuri
        playlist = getPlaylistAndAllTracks(
            accessToken, spotifyPlaylistId, isPrivate=isPrivate, spotify=spotify)
        oldPlaylistDescription = playlist['description']
        playlistTrackUris = [track['track']['uri']
                             for track in playlist['tracks']['items']]
        # Filter track uri & remove duplication
        seen = set()
        trackUriList = [trackUri for trackUri in trackUriList
                        if trackUri not in playlistTrackUris
                        and trackUri not in seen and not seen.add(trackUri)]
    else:
        # Remove playlist tracks
        playlistRemoveAllItems(
            accessToken, spotify, authorizeToken, spotifyPlaylistId, isPrivate=isPrivate)
        print()
    # Check before sync
    print('------------------------------')
    print('Incremental:', isIncremental)
    print('UpdateDesc:', isUpdateDesc)
    print('To sync tracks:', len(trackUriList))
    print('track uris:', trackUriList)
    print('track names:', [list(dict.values())[0] for dict in spotifyTracksFromNetease
                           if list(dict.keys())[0] in trackUriList])
    if isUpdateDesc:
        missingPart = ('Spotify missing(' + str(len(missingSongs)) +
                       '): ' + missingSongsStr + '. ') if missingSongsStr else ''
        playlistDescription = 'Sync between spotify and netease. ' + \
            missingPart + 'Updated on ' + time.strftime("%Y-%m-%d") + '.'
        # if not oldPlaylistDescription:
        #     playlistDescription = 'Sync between spotify and netease. Spotify missing: ' + \
        #         missingSongsStr + '. Updated on ' + time.strftime("%Y-%m-%d") + '.'
        # else:
        #     playlistDescription = re.sub(r'(Sync.*?\. ).*(Updated on.*)',
        #                                 r'\1' + 'Spotify missing: ' + missingSongsStr + '. ' + r'\2', oldPlaylistDescription)
        print('\n------------------------------')
        print('Playlist description:', playlistDescription)
        msg = input(
            '\n*** Are you sure to update playlist description? Press Y to continue. (y/n): ')
        if msg == 'y' or msg == 'Y':
            updatePlayList(spotify, authorizeToken, spotifyPlaylistId,
                           None, playlistDescription, True)
        else:
            print('Didn\'t update description, continue...\n')
    if len(trackUriList) == 0:
        print('Nothing to sync. Exit...')
        sys.exit()
    print('------------------------------')
    msg = input(
        '*** Are you sure to sync these tracks? Press Y to continue. (y/n): ')
    if msg != 'y':
        sys.exit()
    # Add tracks to spotify playlist
    if not (isPrivate or isUpdateDesc):
        scope = "playlist-modify-public"
        spotify, authorizeToken = getAuthorizationToken(
            clientID, clientSecret, scope)
    addTracksToPlayList(spotify, authorizeToken,
                        spotifyPlaylistId, trackUriList)
    print('Crawling playlist new info...')
    crawlSinglePlaylist(accessToken, spotifyPlaylistId,
                        './files/playlists/', isPrivate=isPrivate, spotify=spotify, printPlaylist=False)
    print('Done!')


if __name__ == '__main__':
    main()
