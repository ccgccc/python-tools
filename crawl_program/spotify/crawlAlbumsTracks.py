import json
import xlwt
import time
from spotifyFunc import *
from artists import *

# ******************************
#  Crawl spotify artist tracks
# ******************************

# Define artist here
artist = 'eason_chan'
# Spotify developer api doesn't provide track playcount info, so use spotify's own api to get it.
# This workaround needs getting an accesstoken from spotify web page.
# Token is retrived by spotify web page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa (最偉大的作品).
# Find https://api-partner.spotify.com/pathfinder/v1/query request and copy accesstoken from its authorization header.
spotifyToken = "BQADPeQBlk5iAJBIMIzfA9srv1T8Q5M1E9BeLpqsTWsdnxOxsa1N15aOGPDcKFkUki2MFxd9VCXIZPj_7L3-QtAa5UgAISWhaXObuEtuyBkAsWg271kPm46b0GgvZlKoRhA2LdjmXWTQJZnzm_L6RRbdmwNbQclMRhgbjpBaBryG1Nvl9U97GasxZpbeOCOHnFgYho0vlntnGeyUWPsWqUb7NHdhj06n5mBmHwSNxYmAppXVj699FQzdEOIEJsAwxrZOweFhfpcuW5fNIslqEf2lbhbX8eGwvtX9OkVwq3md9TVQuXGHwYynrRBx0WQK6yuatILZjgKRz68UvGh_Q3teiL5x"


# Get artist albums
artistId = artists[artist]['artistId']
allAblums = getArtistAllAlbums(artistId)
# Get all albums tracks
allTracks = []
trackNames = set()
trackPlaycountToMs = {}
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
    print(str(albumCount) + ': ' + albumName)
    print('Album Id: ' + albumId)
    print('Album Artist: ' + albumArtists)
    print('Release Date: ' + releaseDate)
    print('Total Tracks: ' + str(album['total_tracks']))
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
        allArtists = ''
        containsArtist = False
        for i in range(len(artistsList)):
            if artistsList[i]['uri'].find(artistId) >= 0:
                containsArtist = True
            allArtists = allArtists + artistsList[i]['profile']['name'] + \
                (', ' if i < len(artistsList) - 1 else '')
        if not containsArtist:
            continue
        # ignore repeated tracks
        # 1. by track name
        if trackName in trackNames:
            continue
        else:
            trackNames.add(trackName)
        # 2. by playcount & duration
        # if trackPlaycount is equal & duration difference is less than 10 seconds, consider them the same track
        if trackPlaycount in trackPlaycountToMs.keys() and int(trackPlaycount) > 0 \
                and abs(trackPlaycountToMs[trackPlaycount] - durationMs) < 10000:
            continue
        else:
            trackPlaycountToMs[trackPlaycount] = durationMs
        print(str(trackCount) + ': ' + trackName + ", " + trackPlaycount)
        allTracks.append(
            {'trackUid': trackUid, 'trackUri': trackUri, 'trackName': trackName, 'artists': allArtists,
             'durationMs': durationMs, 'duration': duration, 'playcount': int(trackPlaycount), 'albumId': albumId,
             'albumName': albumName, 'albumArtists': albumArtists, 'releaseDate': releaseDate, 'playable': playable})
# Sort all tracks by playcount
allTracks = sorted(
    allTracks, key=lambda track: track['playcount'], reverse=True)
# print(allTracks)

# Write json to file
with open('./files/' + artist + '_allTracks.json', 'w') as f:
    json.dump(allTracks, f, ensure_ascii=False)


def writeToXlsx(allTracks, fileName):
    # create workbook and sheet
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = workbook.add_sheet('allTracks', cell_overwrite_ok=True)
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
    sheet.write(0, 5, 'Album Artist', style)
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


writeToXlsx(allTracks, './files/' + artists[artist]['name'] +
            '_All Tracks_Generated on ' + time.strftime("%Y-%m-%d") + '.xlsx')

# # Get album tracks by spotify developer api, but this doesn't have play count info
# token = getAccessToken(clientID, clientSecret)
# limit = 50
# # albumTracks = getAlbumTracks(token, allAblums[0]['id'], limit, 0)
# # print(albumTracks)
# # Write json to file
# # with open('albumTracks.json', 'w') as f:
# #     json.dump(albumTracks, f)
# allTracks = []
# for album in allAblums[0:10]:
#     albumTracks = getAlbumTracks(token, album['id'], limit, 0)
#     # print(albumTracks)
#     print('--------------------')
#     print('Album: ' + album['name'] + ' (' + album['release_date'] + ')')
#     i = 0
#     for track in albumTracks['items']:
#         i = i + 1
#         print(str(i) + ': ' + track['name'])
#         # print('Id: ' + t['id'])
#         # print('Date: ' + t['release_date'])
#         # print('Tracks: ' + str(t['total_tracks']))
#         # not necessary, album info already has track info
#         track = getSingleTrack(token, track['id'])
#         allTracks.append(track)

# # Write json to file
# with open('allTracks.json', 'w') as f:
#     json.dump(allTracks, f)
