import json
import time
import xlwt
from artists import artists, artistToCrawl
from spotifyFunc import *

# ******************************
#  Crawl spotify artist tracks
# ******************************

# Define artist to crawl here
artistToCrawlList = [artistToCrawl]
# Crawl all artists
# artistToCrawlList = artists.keys()


def main():
    for artist in artistToCrawlList:
        print('--------------------')
        print('Processing ' + artists[artist]['name'] + '...')

        # Get all tracks
        allAlbumsTracks = []
        with open('./files/tracks/' + artist + '_alltracks_raw.json') as f:
            allAlbumsTracks = json.load(f)
        # print(allTracks)

        if artist in {'beyond', 'kare_mok'}:
            mustMainArtist = True
        else:
            mustMainArtist = False

        processTracks(artists, artist, allAlbumsTracks,
                      filterTrackByName=False, mustMainArtist=mustMainArtist, printInfo=False)
        print('Done!')


def processTracks(artists, artist, allAlbumsTracks, filterTrackByName=False, mustMainArtist=False, printInfo=True):
    artistId = artists[artist]['artistId']
    # Get all albums tracks
    albumCount = 0
    preAlbumId = ''
    filterdTracks = []
    trackNames = set()
    trackPlaycountToMs = {}
    for albumTracks in allAlbumsTracks:
        album = albumTracks['album']
        albumId = album['id']
        albumName = album['name']
        if preAlbumId != albumId:
            albumCount = albumCount + 1
            preAlbumId = albumId
        albumArtists = ', '.join([artist['name']
                                 for artist in album['artists']])
        releaseDate = album['release_date']
        albumAlbumGroup = album['album_group']
        albumAlbumType = album['album_type']
        albumType = album['type']
        totalTracks = album['total_tracks']
        if printInfo:
            print('--------------------')
            print(str(albumCount) + ': ' + albumName)
            print('Album Id: ' + albumId)
            print('Album Artist: ' + albumArtists)
            print('Release Date: ' + releaseDate)
            print('Total Tracks: ' + str(totalTracks))
            print('Tracks:')
        trackCount = 0
        for track in albumTracks['tracks']['items']:
            trackCount = trackCount + 1
            trackUid = track['uid']
            trackUri = track['track']['uri']
            trackName = track['track']['name']
            trackPlaycount = track['track']['playcount']
            durationMs = track['track']['duration']['totalMilliseconds']
            duration = str(durationMs // 60000) + "m " + \
                "{:02d}".format(durationMs // 1000 % 60) + "s"
            playable = 'Y' if track['track']['playability']['playable'] == True else 'N'

            # Check if mustMainArtist
            artistsList = track['track']['artists']['items']
            if mustMainArtist and artistsList[0]['uri'].find(artistId) < 0:
                continue
            # Check if filterTrackByName
            if filterTrackByName:
                # Ignore repeated tracks by track name
                # Not recomendded, sometimes repeated track names are alright, e.g. K歌之王 (国+粤)
                if trackName in trackNames:
                    continue
                else:
                    trackNames.add(trackName)

            # Concatenate artists & filter other artists
            containsArtist = False
            allArtists = ''
            for i in range(len(artistsList)):
                if artistsList[i]['uri'].find(artistId) >= 0:
                    containsArtist = True
                allArtists = allArtists + artistsList[i]['profile']['name'] + \
                    (', ' if i < len(artistsList) - 1 else '')
            if not containsArtist:
                continue
            # Ignore repeated tracks by playcount & duration
            # If trackPlaycount is equal & duration difference is less than 20 seconds, consider them the same track
            if trackPlaycount in trackPlaycountToMs.keys() and int(trackPlaycount) > 0 \
                    and abs(trackPlaycountToMs[trackPlaycount] - durationMs) < 20000:
                continue
            else:
                trackPlaycountToMs[trackPlaycount] = durationMs
            if printInfo:
                print(str(trackCount) + ': ' + trackName + ", " + trackPlaycount)
            filterdTracks.append(
                {'trackUid': trackUid, 'trackUri': trackUri, 'trackName': trackName, 'artists': allArtists,
                    'durationMs': durationMs, 'duration': duration, 'playcount': int(trackPlaycount), 'playable': playable,
                    'albumId': albumId, 'albumName': albumName, 'albumArtists': albumArtists, 'releaseDate': releaseDate,
                    'albumAlbumGroup': albumAlbumGroup, 'albumAlbumType': albumAlbumType, 'albumType': albumType, 'totalTracks': totalTracks})

    # Sort all tracks by playcount
    sortedTracks = sorted(
        filterdTracks, key=lambda track: track['playcount'], reverse=True)

    # Write json to file
    with open('./files/tracks/' + artist + '_alltracks.json', 'w') as f:
        json.dump(sortedTracks, f, ensure_ascii=False)
    writeToXlsx(sortedTracks, './files/trackSheets/' + artists[artist]['name'] +
                '_All Tracks_Generated on ' + time.strftime("%Y-%m-%d") + '.xlsx')
    return sortedTracks


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


if __name__ == '__main__':
    main()
