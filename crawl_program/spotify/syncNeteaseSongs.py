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
from playlistRemoveItems import playlistRemoveAllItems
from spotifyFunc import *
from utils.auth import getAccessToken, getAuthorizationToken
from utils.secrets import clientID, clientSecret
from netease.specialSongs import *
from netease.artists import artists as neteaseArtists
from artists import artists as spotifyArtists

# ****************************************
#     Sync netease non-playable songs
# ****************************************


# From spotify playlists(spotifySourcePlaylistNames),
# match non-playable songs in netease playlist(neteaseMatchPlaylistName)
# and sync them to another spotify playlist(spotifyPlaylistId)
# Spotify playlist id
spotifyPlaylistId = '2UuyNeehZW9HQXhTkmFKBj'  # Netease Liked
# Define is incremental
isIncremental = True
# Define spotify playlist isPrivate
isPrivate = True
# Spotify source playlists names
spotifySourcePlaylistNames = ['Favorite', 'Like']
# Netease match playlist name
neteaseMatchPlaylistName = 'playlist_songs_ccgccc喜欢的音乐_by ccgccc_bak_2022-10-09'


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
        # TODO reliable??
        if neteasePlaylistSongs[i]['fee'] == 4 and neteasePlaylistPrivileges[i]['flag'] % 4 == 0:
            # print(neteasePlaylistSongs[i]['name'], neteasePlaylistPrivileges[i]['flag'])
            neteaseNeedPurchaseSongs.append(neteasePlaylistSongs[i])
            neteaseAllSyncSongs.append(neteasePlaylistSongs[i])
    print('------------------------------')
    print('Netease no copyright songs:', len(neteaseNoCopyrightSongs))
    print({song['id']: song['name'] for song in neteaseNoCopyrightSongs}, '\n')
    print('Netease need purchase songs:', len(neteaseNeedPurchaseSongs))
    print({song['id']: song['name']
          for song in neteaseNeedPurchaseSongs}, '\n')
    neteaseAllSyncSongNames = {song['name'] for song in neteaseAllSyncSongs}

    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Get spotify playlists & artist track names
    spotifyArtistTrackNames = {}
    for spotifyPlaylistName in spotifySourcePlaylistNames:
        with open('../spotify/files/playlists/playlist_' + spotifyPlaylistName + '_by ccg ccc.json') as f:
            spotifyPlaylist = json.load(f)
        curSpotifyArtistTrackNames = getSpotifyArtistTrackNames(
            spotifyPlaylistName, spotifyPlaylist['tracks'])
        for artist, trackNames in curSpotifyArtistTrackNames.items():
            if spotifyArtistTrackNames.get(artist) != None:
                spotifyArtistTrackNames[artist].extend(trackNames)
            else:
                spotifyArtistTrackNames[artist] = trackNames
    spotifyTrackOriginalNames = []
    for artist, trackNames in spotifyArtistTrackNames.items():
        if spotifyArtistTrackNames.get(artist) != None:
            spotifyTrackOriginalNames.extend(
                spotifyArtistTrackNames.get(artist))
    # print('Spotify original track names: ',
    #       '(Total ', len(spotifyTrackOriginalNames), ')', sep='')
    # print(spotifyTrackOriginalNames, '\n')

    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Process original track names
    spotifyTrackOriginalNames = [{list(dict.keys())[0]: re.sub(r' \(.*', '', re.sub(r' - .*', '', list(dict.values())[0]))}
                                 for dict in spotifyTrackOriginalNames]
    allSpecialSongNames = {}
    for artist, songNameDict in specialSongNames.items():
        allSpecialSongNames = allSpecialSongNames | songNameDict
    spotifyTrackNames = [{list(dict.keys())[0]: zhconv.convert(list(dict.values())[0], 'zh-cn', update=allSpecialSongNames)}
                         for dict in spotifyTrackOriginalNames]
    print('------------------------------')
    print('Spotify processed track names:', len(spotifyTrackNames))
    print([list(track.values())[0] for track in spotifyTrackNames], '\n')
    # Get matching songs from netease
    spotifyTracksFromNetease = [dict for dict in spotifyTrackNames if list(
        dict.values())[0] in neteaseAllSyncSongNames]
    print('------------------------------')
    print('Spotify sync tracks from netease can\'t play:',
          len(spotifyTracksFromNetease))
    print([list(track.values())[0]
          for track in spotifyTracksFromNetease], '\n')

    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Get spotify authorization token by scope and accessToken
    scope = ["playlist-read-private", "playlist-modify-private"]
    spotify, authorizeToken = getAuthorizationToken(
        clientID, clientSecret, scope)
    accessToken = getAccessToken(clientID, clientSecret)
    trackUriList = [list(dict.keys())[0] for dict in spotifyTracksFromNetease]
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
    print('To sync trackUris:', len(trackUriList))
    print(trackUriList, '\n')
    if len(trackUriList) == 0:
        print('Nothing to sync. Exit...')
        sys.exit()
    msg = input(
        'Are you sure to sync these tracks? Press Y to continue. (y/n): ')
    if msg != 'y' and msg != 'n':
        sys.exit()
    print(len(trackUriList))
    # Add tracks to spotify playlist
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
    spotifyArtistTrackNames = {k: [] for k, v in neteaseArtists.items()}
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
