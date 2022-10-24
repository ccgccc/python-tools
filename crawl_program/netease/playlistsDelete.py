import time
from os import listdir
from os.path import isfile, join
from artists import *
from common import *

# ****************************************
#   Remove netease user's all playlists
# ****************************************

# Excel formula: =CONCATENATE(B2,": '",TRIM(C2),"',")
playlistToKeep = {
    553778357: 'ccgccc喜欢的音乐',
    7671476276: '汪峰 Most Played Songs',
    7669598709: 'Beyond Most Played Songs',
    7669681504: '王力宏 Most Played Songs',
    7669602741: '许嵩 Most Played Songs',
    7669746296: '林俊杰 Most Played Songs',
    7669735197: '邓紫棋 Most Played Songs',
    7669779415: 'Bruno Mars Most Played Songs',
    7669584701: '陈奕迅 Most Played Songs',
    7669372164: '周杰伦 Most Played Songs',
    7669698351: '张学友 Most Played Songs',
    7170398690: 'ccgccc的2021年度歌单',
    5432812189: 'ccgccc的2020年度歌单',
    3163991842: 'ccgccc的2019年度歌单',
    2611454231: 'ccgccc的2018年度歌单',
    7127137659: 'Learn MV',
    7101716751: 'Learned',
    7178619569: 'Maybe Learned',
    7180217796: 'Almost Learned',
    7029730958: 'Learn',
    7101765375: 'To Learn',
    7093094134: 'Probably Learn',
    7045566896: 'Maybe Learn',
    7140236506: 'Learn Waitlist',
    6936670073: 'her like',
}
# Defin cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


fileName = 'playlists/all_my_playlists_bak_' + time.strftime("%Y-%m-%d")
playlists = loadJsonFromFile(fileName)
playlistIds = list(map(lambda playlist: playlist['id'], filter(
    lambda playlist: playlist['userId'] == myUserId, playlists['playlist'])))
print(playlistIds)
print('Total:', len(playlistIds))

playlistIdsToKeep = set(playlistToKeep.keys())
print(playlistIdsToKeep)
print('To Keep:', len(playlistIdsToKeep))

playlistIdsToRemove = set(playlistIds) - playlistIdsToKeep
playlistIdsToRemove = list(map(lambda x: str(x), playlistIdsToRemove))
print(playlistIdsToRemove)
print('To Remove:', len(playlistIdsToRemove))

deleteIdsStr = ','.join(playlistIdsToRemove)
print('\nTo Delete:', deleteIdsStr)
deletePlaylist(deleteIdsStr)
