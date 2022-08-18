import json
import xlwt
from spotifyFunc import *
from artists import *

# ******************************
#  Crawl spotify artist tracks
# ******************************

# Define artist here
artist = 'jacky_cheung'
artistId = artists[artist]['artistId']
# Spotify developer api doesn't provide track playcount info, so we use spotify's own api to get it.
# This workaround needs us to get an accesstoken from spotify web page.
# Token is retrived by spotify web page, e.g. https://open.spotify.com/album/1rBr9FeLlp5ueSKtE89FZa (最偉大的作品).
# Find https://api-partner.spotify.com/pathfinder/v1/query request and copy accesstoken from its authorization header.
spotifyToken = "BQAP8B-mAK55ycUsug87jIMuu4XSe7qqoxoDB7fmEKVf6YMvNKXIxT_IP4CCVgjAozbmi-7JxW1KtkmcPQZ2vRX_N6j3PeVe3Q0rwtKbSx5--WBUhP12pZX7ewY322nhYhQTV0D_tyE2CZVqZqFnBaT9q2GFJNy3oRoX3Li3h5o6rgH2H3D04Ffc40DZ5bVDT5U9Nam4n5STg2Cv4PTaC-SIV2S7UijZmuFPt4yww-_IqrwERq5PB_fUae8z5om42ZjqT7lrtJZIfDIaG_XYKITa3t0RF00i28hPEHsTbu2miTz70ZFvNB9roAr5kzcIl5fj3wUsnp0sj1ab9oip54-IYxZM"


# Get artist albums
allAblums = getArtistAllAlbums(artistId)
# Get all albums tracks
allTracks = []
trackNames = set()
albumCount = 0
# for album in allAblums[0:10]:
for album in allAblums:
    print('--------------------')
    albumCount = albumCount + 1
    albumId = album['id']
    albumName = album['name']
    releaseDate = album['release_date']
    print(str(albumCount) + ': ' + albumName)
    print('AlbumId: ' + albumId)
    print('Date: ' + releaseDate)
    print('Tracks: ' + str(album['total_tracks']))
    albumTracks = getAlbumTracksByThirdPartyAPI(
        spotifyToken, albumId)
    # print(albumTracks)
    trackCount = 0
    for track in albumTracks['data']['album']['tracks']['items']:
        trackCount = trackCount + 1
        # ignore repeated tracks
        trackName = track['track']['name']
        if trackName in trackNames:
            continue
        else:
            trackNames.add(trackName)
        trackPlaycount = track['track']['playcount']
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
        durationMs = track['track']['duration']['totalMilliseconds']
        duration = str(durationMs // 60000) + "m " + \
            str(durationMs // 1000 % 60) + "s"
        print(str(trackCount) + ': ' + trackName + ", " + trackPlaycount)
        allTracks.append(
            {'trackName': trackName, 'artists': allArtists, 'duration': duration,
             'playcount': int(trackPlaycount), 'albumName': albumName, 'releaseDate': releaseDate})
# Sort all tracks by playcount
allTracks = sorted(
    allTracks, key=lambda track: track['playcount'], reverse=True)
# print(allTracks)

# Write json to file
with open('allTracks.json', 'w') as f:
    json.dump(allTracks, f)


def writeToXlsx(allTracks, fileName):
    # create workbook and sheet
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = workbook.add_sheet('allTracks', cell_overwrite_ok=True)
    # set column width
    sheet.col(0).width = 256*20  # 列宽n个字符长度，256为衡量单位
    sheet.col(1).width = 256*10
    sheet.col(2).width = 256*20
    sheet.col(3).width = 256*10
    sheet.col(4).width = 256*20
    sheet.col(5).width = 256*20
    # set font
    font = xlwt.Font()
    font.name = '等线'  # 字体类型
    font.height = 20*12  # 字体大小，11为字号，20为衡量单位
    style = xlwt.XFStyle()
    style.font = font
    # write header
    writeHeader(sheet, style)
    # write track data
    for i in range(len(allTracks)):
        sheet.row(i+1).height_mismatch = True
        sheet.row(i+1).height = int(256*1.4)
        sheet.write(i+1, 0, allTracks[i]['trackName'], style)
        sheet.write(i+1, 1, allTracks[i]['playcount'], style)
        sheet.write(i+1, 2, allTracks[i]['artists'], style)
        sheet.write(i+1, 3, allTracks[i]['duration'], style)
        sheet.write(i+1, 4, allTracks[i]['albumName'], style)
        sheet.write(i+1, 5, allTracks[i]['releaseDate'], style)
    # save to file
    workbook.save(fileName)


def writeHeader(sheet, style):
    sheet.row(0).height_mismatch = True
    sheet.row(0).height = int(256*1.3)
    sheet.write(0, 0, 'Track', style)
    sheet.write(0, 1, 'PlayCount', style)
    sheet.write(0, 2, 'Artists', style)
    sheet.write(0, 3, 'Duration', style)
    sheet.write(0, 4, 'Album', style)
    sheet.write(0, 5, 'Release Date', style)


writeToXlsx(allTracks, artists[artist]['name'] + '_All Tracks.xlsx')

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
