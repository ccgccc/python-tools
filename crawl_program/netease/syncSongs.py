import re
import sys
import json
import zhconv
from .specialSongs import *
from .artists import *

# **************************************************
#  Get spotify synced songs by artist & track names
# **************************************************


# Classify playlist tracks by artist
def getSpotifyArtistTrackIdNames(spotifyPlaylistName, spotifyPlaylistTracks, spotifyArtists):
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
    # Initialize spotify artist track names, like this: {'artist': ['trackname', 'trackname2']}
    spotifyArtistTrackNames = {}
    artistsNotFound = set()
    seenTrackNames = set()
    for track in spotifyPlaylistTracks['items']:  # Iterate playlist tracks
        isArtistFound = False
        for trackArtist in track['track']['artists']:  # Iterate track artists
            trackArtistId = trackArtist['id']
            if trackArtist['id'] in spotifyArtistIdsSet:
                # Classify tracks to artists & rename duplicate track names
                artist = spotifyArtistIds.get(trackArtistId)
                if spotifyArtistTrackNames.get(artist) == None:
                    spotifyArtistTrackNames[artist] = []
                trackName = track['track']['name']
                if trackName not in seenTrackNames:
                    spotifyArtistTrackNames[artist].append(
                        {track['track']['uri']: trackName})
                    seenTrackNames.add(trackName)
                else:
                    spotifyArtistTrackNames[artist].append(
                        {track['track']['uri']: trackName + '_2_' + track['track']['artists'][0]['name']})
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


# Get netease sync songs from spotify for every artist & merge all sync songs
def getSpotifyToNeteaseSongs(spotifyArtistTrackIdNames, spotifyArtists, isNeedMissingPrompt=True):
    syncSongs = []
    missingSongs = []
    missingSongsStr = []
    # Get sync songs
    for artist, trackIdNames in spotifyArtistTrackIdNames.items():
        if len(trackIdNames) == 0:
            continue
        artist = artist.split('-')[0]
        artistName = spotifyArtists[artist]['name']
        print('\n************************************************************')
        print('************************************************************')
        print('Processing', artistName, '......')
        curSyncSongs, curMissingSongs = getSyncSongs(
            artist, trackIdNames, isRemoveAlias=True, isNeedPrompt=False, isOkPrompt=False)
        syncSongs.extend(curSyncSongs)
        missingSongs.extend(curMissingSongs)
        if len(curMissingSongs) > 0:
            missingSongsStr.append(
                '、'.join(curMissingSongs) + '(' + artistName + ')')
        print('Acc count:', len(syncSongs))
    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('All sync songs: ', len(syncSongs), '\n', json.dumps(
        syncSongs, ensure_ascii=False), '\n', sep='')
    print('All missing songs: ', len(missingSongs),
          '\n', json.dumps(missingSongs, ensure_ascii=False), '\n', sep='')
    if isNeedMissingPrompt and len(missingSongs) > 0:
        msg = input('Are you sure? Press Y to continue: ')
        if msg != 'y' and msg != 'Y':
            sys.exit()
    return syncSongs, missingSongs, missingSongsStr


# Process spotify track names & match netease songs for one artist
def getSyncSongs(artist, spotifyTrackIdNames, isRemoveAlias=True,
                 isNeedPrompt=True, isOkPrompt=True, confirmOnceMode=True):
    # Get spotify playlist song names
    spotifyTrackOriginalNames = [
        list(dict.values())[0] for dict in spotifyTrackIdNames]
    if isRemoveAlias == True:
        spotifyTrackOriginalNames = [re.sub(r' \(.*', '', re.sub(r' - .*', '', track))
                                     for track in spotifyTrackOriginalNames]
    spotifyTrackNames = [zhconv.convert(track, 'zh-cn', update=specialSongNames.get(artist))
                         for track in spotifyTrackOriginalNames]
    print('------------------------------')
    print('Spotify Tracks:', len(spotifyTrackOriginalNames))
    print(spotifyTrackOriginalNames, '\n')

    # Get netease artist all songs
    fileName = 'songs/' + artist + '_allsongs'
    # Load json from file
    with open('./files/' + fileName + '.json') as f:
        neteaseArtistSongs = json.load(f)
    neteaseArtistSongIds = {song['name']: song['id']
                            for song in neteaseArtistSongs}
    if specialSongIds.get(artist) != None:
        neteaseArtistSongIds = neteaseArtistSongIds \
            | specialSongIds.get(artist)  # since python 3.9
    if replaceSongIds.get(artist) != None:
        for k, v in replaceSongIds.get(artist).items():
            neteaseArtistSongIds[k] = v

    # Get sync songs name & id
    seen = set()
    syncSongs = [{name: neteaseArtistSongIds.get(name)} for name in spotifyTrackNames
                 if neteaseArtistSongIds.get(name) != None and name not in seen and not seen.add(name)]
    print('------------------------------')
    print('Netease sync songs:', len(syncSongs))
    print(syncSongs, '\n')

    # Get missing songs
    missingSongs = set(spotifyTrackNames) - \
        {list(songDict.keys())[0] for songDict in syncSongs}
    missingSongs = sorted(
        list(missingSongs), key=lambda songName: spotifyTrackNames.index(songName))
    missingSongSpotifyNames = [spotifyTrackOriginalNames[spotifyTrackNames.index(songName)]
                               for songName in missingSongs]
    print('------------------------------')
    missingCount = len(spotifyTrackOriginalNames) - len(syncSongs)
    print('Netease missing songs:', missingCount)
    if missingCount > len(missingSongs):
        # Already modified duplicated names before, so  probably no duplicates here
        seen = set()
        dupes = [x for x in spotifyTrackOriginalNames
                 if x in seen or seen.add(x)]
        print('Duplicate:', dupes)
    if len(missingSongs) > 0:
        print('Missing:', missingSongSpotifyNames)
        print('Missing:', missingSongs)
    print('------------------------------')

    # Process netease sensitive words
    missingSongs = [song if sensitiveWords.get(song) == None else sensitiveWords[song]
                    for song in missingSongs]
    # Confirmation prompt
    if not isNeedPrompt or not isOkPrompt and missingCount == 0:
        return syncSongs, missingSongSpotifyNames
    while True:
        if len(missingSongs) > 0:
            continueMsg = input(
                'There are some missing songs. Do you want to continue? (y/n): ')
        else:
            continueMsg = input(
                'All songs can be synced. Press Y to continue. (y/n): ')
        if continueMsg == 'y' or continueMsg == 'Y':
            break
        elif confirmOnceMode or continueMsg == 'n' or continueMsg == 'N':
            sys.exit()
    return syncSongs, missingSongs
