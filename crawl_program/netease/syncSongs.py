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

    # Get spotify artists IDs (must in netease artists)
    spotifyArtistIds = {v['artistId']: k for k, v in spotifyArtists.items()
                        if k in artists.keys() or k.split('-')[0] in artists.keys()}
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
                trackUri = track['track']['uri']
                trackName = track['track']['name']
                if trackName + '_' + artist not in seenTrackNames:
                    spotifyArtistTrackNames[artist].append(
                        {trackUri: trackName})
                    seenTrackNames.add(trackName + '_' + artist)
                else:
                    spotifyArtistTrackNames[artist].append(
                        {trackUri: trackName + '_2_' + track['track']['artists'][0]['name']})
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
def getSpotifyToNeteaseSongs(spotifyArtistTrackIdNames, spotifyArtists, addSpotifyMissing=False, isNeedMissingPrompt=True):
    syncSongs = []
    neteaseMissingSongs = []
    neteaseMissingSongsStr = []
    neteaseMissingSongSpotifyNames = []
    spotifyMissingTracks = []
    spotifyMissingTracksStr = []
    # Get sync songs
    for artist, trackIdNames in spotifyArtistTrackIdNames.items():
        if len(trackIdNames) == 0:
            continue
        artist = artist.split('-')[0]
        artistName = spotifyArtists[artist]['name']
        print('\n************************************************************')
        print('************************************************************')
        print('Processing', artistName, '......')
        curSyncSongs, curMissingSongs, curMissingSongSpotifyNames = getSyncSongs(
            artist, trackIdNames, addSpotifyMissing=addSpotifyMissing, isRemoveAlias=True, isNeedPrompt=False, isOkPrompt=False)
        syncSongs.extend(curSyncSongs)
        neteaseMissingSongs.extend(curMissingSongs)
        neteaseMissingSongSpotifyNames.extend(curMissingSongSpotifyNames)
        if len(curMissingSongs) > 0:
            neteaseMissingSongsStr.append(
                '、'.join(curMissingSongs) + '(' + artistName + ')')
        if addSpotifyMissing:
            curSpotifyMissingSongs = spotifyMissingSongs.get(artist)
            if curSpotifyMissingSongs != None and len(curSpotifyMissingSongs) > 0:
                curSpotifyMissingTracks = [
                    list(dict.keys())[0] for dict in curSpotifyMissingSongs]
                spotifyMissingTracks.extend(curSpotifyMissingTracks)
                spotifyMissingTracksStr.append(
                    '、'.join(curSpotifyMissingTracks) + '(' + artistName + ')')
        print('Acc count:', len(syncSongs))
    print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('All sync songs: ', len(syncSongs), '\n', json.dumps(
        syncSongs, ensure_ascii=False), '\n', sep='')
    print('All netease missing songs: ', len(neteaseMissingSongs), '\n', 'spotify name: ',
          json.dumps(neteaseMissingSongSpotifyNames, ensure_ascii=False), '\n',
          'converted: ', json.dumps(neteaseMissingSongs, ensure_ascii=False), '\n', sep='')
    if addSpotifyMissing:
        print('All spotify missing songs: ', len(spotifyMissingTracks),
              '\n', json.dumps(spotifyMissingTracks, ensure_ascii=False), '\n', sep='')
    if isNeedMissingPrompt and len(neteaseMissingSongs) > 0:
        msg = input('Are you sure? Press Y to continue: ')
        if msg != 'y' and msg != 'Y':
            sys.exit()
    return syncSongs, neteaseMissingSongs, neteaseMissingSongsStr, spotifyMissingTracksStr


# Process spotify track names & match netease songs for one artist
def getSyncSongs(artist, spotifyTrackIdNames, isRemoveAlias=True, addSpotifyMissing=False,
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
    if addSpotifyMissing:
        # Add spotify missing songs
        if spotifyMissingSongs.get(artist) != None:
            syncSongs.extend(spotifyMissingSongs[artist])
    print('------------------------------')
    print('Netease sync songs:', len(syncSongs))
    print(syncSongs, '\n')

    # Get missing songs
    neteaseMissingSongs = set(spotifyTrackNames) - \
        {list(songDict.keys())[0] for songDict in syncSongs}
    neteaseMissingSongs = sorted(
        list(neteaseMissingSongs), key=lambda songName: spotifyTrackNames.index(songName))
    missingSongSpotifyNames = [spotifyTrackOriginalNames[spotifyTrackNames.index(songName)]
                               for songName in neteaseMissingSongs]
    print('------------------------------')
    missingCount = len(spotifyTrackOriginalNames) - len(syncSongs)
    if addSpotifyMissing and spotifyMissingSongs.get(artist) != None:
        missingCount = missingCount + len(spotifyMissingSongs[artist])
    print('Netease missing songs:', missingCount)
    if missingCount > len(neteaseMissingSongs):
        # Already modified duplicated names before, so  probably no duplicates here
        seen = set()
        dupes = [x for x in spotifyTrackOriginalNames
                 if x in seen or seen.add(x)]
        print('Duplicate:', dupes)
    if len(neteaseMissingSongs) > 0:
        print('spotify name:', missingSongSpotifyNames)
        print('converted:', neteaseMissingSongs)
    print('------------------------------')

    # Process netease sensitive words
    neteaseMissingSongs = [song if sensitiveWords.get(song) == None else sensitiveWords[song]
                           for song in neteaseMissingSongs]
    # Confirmation prompt
    if not isNeedPrompt or not isOkPrompt and missingCount == 0:
        return syncSongs, neteaseMissingSongs, missingSongSpotifyNames
    while True:
        if len(neteaseMissingSongs) > 0:
            continueMsg = input(
                'There are some missing songs. Do you want to continue? (y/n): ')
        else:
            continueMsg = input(
                'All songs can be synced. Press Y to continue. (y/n): ')
        if continueMsg == 'y' or continueMsg == 'Y':
            break
        elif confirmOnceMode or continueMsg == 'n' or continueMsg == 'N':
            sys.exit()
    return syncSongs, neteaseMissingSongs, missingSongSpotifyNames
