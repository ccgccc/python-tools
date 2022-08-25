import json
import xlwt
import time
from spotifyFunc import *
from artists import artists, artistToCrawl
from utils.secrets import clientID, clientSecret

# ******************************
#  Crawl spotify artist tracks
# ******************************

# Define artist here
artist = artistToCrawl
# Spotify developer api doesn't provide track playcount info, so use spotify's own api to get it.
# This workaround needs getting an accesstoken from spotify web page.
# Token is retrived by spotify web page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa (最偉大的作品).
# Find https://api-partner.spotify.com/pathfinder/v1/query request (search 'query') and copy token from its authorization headers.
spotifyToken = \
    'BQDcVilZxBxIZGot9f8aCn1lKcWzXhVhEXkUbFdm_n6m6uWNzZuYww8Cv0rZHzcsiEtiWrg_0iartAZdcKEfMjewk1yMj2kwnJrf0SvT3MvzTlrdYhAzIe9QKdY7KQpu4qKPqyzmtdBe5lyIjL-h3RkoTXTOEhYq8fJQmUYXEAjc8vyQsJWgq9nGtSSGamNcrOEmty9gUvMJflOPAXnP4A4HkxBc86TzfLU8knwaYL1XNdSbG47MTBSs4SHIMFmQgNO8kb1xdkovMOb7de4Z2b154K1cXTqMLprm-x5uuBCKrD5EMudVN5Jx9B3LybdpUG97-_MJQQyZcXSy2ANN2_Z7NG_k'
# Filter track by track name or not
filterTrackByName = False


# Get artist albums
artistId = artists[artist]['artistId']
token = getAccessToken(clientID, clientSecret)
allAblums = getArtistAllAlbums(token, artistId)
# Get all albums tracks
allTracks = []
albumCount = 0
# for album in allAblums[0:5]:
for album in allAblums:
    print('--------------------')
    albumCount = albumCount + 1
    albumId = album['id']
    albumName = album['name']
    albumArtistsList = album['artists']
    albumArtists = ''
    for i in range(len(albumArtistsList)):
        albumArtists = albumArtists + albumArtistsList[i]['name'] + \
            (', ' if i < len(albumArtistsList) - 1 else '')
    releaseDate = album['release_date']
    albumAlbumGroup = album['album_group']
    albumAlbumType = album['album_type']
    albumType = album['type']
    totalTracks = album['total_tracks']
    print(str(albumCount) + ': ' + albumName)
    print('Album Id: ' + albumId)
    print('Album Artist: ' + albumArtists)
    print('Release Date: ' + releaseDate)
    print('Total Tracks: ' + str(totalTracks))
    albumTracks = getAlbumTracksByThirdPartyAPI(
        spotifyToken, albumId)
    # print(albumTracks)
    trackCount = 0
    for track in albumTracks['data']['album']['tracks']['items']:
        trackCount = trackCount + 1
        trackUid = track['uid']
        trackUri = track['track']['uri']
        trackName = track['track']['name']
        trackPlaycount = track['track']['playcount']
        durationMs = track['track']['duration']['totalMilliseconds']
        duration = str(durationMs // 60000) + "m " + \
            "{:02d}".format(durationMs // 1000 % 60) + "s"
        playable = 'Y' if track['track']['playability']['playable'] == True else 'N'
        # concatenate artists & filter other artists
        artistsList = track['track']['artists']['items']
        containsArtist = False
        allArtists = ''
        for i in range(len(artistsList)):
            if artistsList[i]['uri'].find(artistId) >= 0:
                containsArtist = True
            allArtists = allArtists + artistsList[i]['profile']['name'] + \
                (', ' if i < len(artistsList) - 1 else '')
        if not containsArtist:
            continue
        print(str(trackCount) + ': ' + trackName + ", " + trackPlaycount)
        allTracks.append(
            {'trackUid': trackUid, 'trackUri': trackUri, 'trackName': trackName, 'artists': allArtists,
             'durationMs': durationMs, 'duration': duration, 'playcount': int(trackPlaycount), 'playable': playable,
             'albumId': albumId, 'albumName': albumName, 'albumArtists': albumArtists, 'releaseDate': releaseDate,
             'albumAlbumGroup': albumAlbumGroup, 'albumAlbumType': albumAlbumType, 'albumType': albumType, 'totalTracks': totalTracks})

# Write json to file
with open('./files/' + artist + '_alltracks_raw.json', 'w') as f:
    json.dump(allTracks, f, ensure_ascii=False)

# Filter albums tracks
filterdTracks = []
trackNames = set()
trackPlaycountToMs = {}
for track in allTracks:
    trackPlaycount = track['playcount']
    durationMs = track['durationMs']
    # ignore repeated tracks by playcount & duration
    # if trackPlaycount is equal & duration difference is less than 10 seconds, consider them the same track
    if trackPlaycount in trackPlaycountToMs.keys() and int(trackPlaycount) > 0 \
            and abs(trackPlaycountToMs[trackPlaycount] - durationMs) < 10000:
        continue
    else:
        trackPlaycountToMs[trackPlaycount] = durationMs
    if filterTrackByName:
        # ignore repeated tracks by track name
        # not recomendded, sometimes repeated track names are alright, e.g. K歌之王 (国+粤)
        if trackName in trackNames:
            continue
        else:
            trackNames.add(trackName)
    filterdTracks.append(track)

# Sort all tracks by playcount
sortedTracks = sorted(
    filterdTracks, key=lambda track: track['playcount'], reverse=True)
# print(allTracks)

# Write json to file
# with open('./files/' + artist + '_alltracks.json', 'w') as f:
#     json.dump(allTracks, f, ensure_ascii=False)


def writeToXlsx(allTracks, fileName):
    # create workbook and sheet
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = workbook.add_sheet('All Tracks', cell_overwrite_ok=True)
    # set column width
    sheet.col(0).width = 256*40  # 列宽n个字符长度，256为衡量单位
    sheet.col(1).width = 256*40
    sheet.col(2).width = 256*12
    sheet.col(3).width = 256*10
    sheet.col(4).width = 256*40
    sheet.col(5).width = 256*20
    sheet.col(6).width = 256*20
    sheet.col(7).width = 256*10
    # set font
    font = xlwt.Font()
    font.name = '等线'  # 字体类型
    font.height = 20*12  # 字体大小，11为字号，20为衡量单位
    style = xlwt.XFStyle()
    style.font = font
    # write header
    sheet.row(0).height_mismatch = True
    sheet.row(0).height = int(256*1.3)
    sheet.write(0, 0, 'Track', style)
    sheet.write(0, 1, 'Artists', style)
    sheet.write(0, 2, 'Play Count', style)
    sheet.write(0, 3, 'Duration', style)
    sheet.write(0, 4, 'Album', style)
    sheet.write(0, 5, 'Album Artists', style)
    sheet.write(0, 6, 'Release Date', style)
    sheet.write(0, 7, 'Playable', style)
    # write track data
    for i in range(len(allTracks)):
        sheet.row(i+1).height_mismatch = True
        sheet.row(i+1).height = int(256*1.4)
        sheet.write(i+1, 0, allTracks[i]['trackName'], style)
        sheet.write(i+1, 1, allTracks[i]['artists'], style)
        sheet.write(i+1, 2, allTracks[i]['playcount'], style)
        sheet.write(i+1, 3, allTracks[i]['duration'], style)
        sheet.write(i+1, 4, allTracks[i]['albumName'], style)
        sheet.write(i+1, 5, allTracks[i]['albumArtists'], style)
        sheet.write(i+1, 6, allTracks[i]['releaseDate'], style)
        sheet.write(i+1, 7, allTracks[i]['playable'], style)
    # save to file
    workbook.save(fileName)


writeToXlsx(sortedTracks, './files/' + artists[artist]['name'] +
            '_All Tracks_Generated on ' + time.strftime("%Y-%m-%d") + '.xlsx')
