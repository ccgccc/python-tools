import requests
from common import *

# ****************************************
#        Get netease user's info
# ****************************************


# User Detail
url = baseUrl + '/user/detail'
params = {
    'uid': myUserId
}
userDetail = requests.get(url, headers=headers, params=params).json()
# print(json.dumps(userDetail, ensure_ascii=False))
print('User Id:', userDetail['profile']['userId'])
print('Nickname:', userDetail['profile']['nickname'])
print('Level:', userDetail['level'])
print('Listen Songs:', userDetail['listenSongs'])
print('Follows:', userDetail['profile']['follows'])
print('Followeds:', userDetail['profile']['followeds'])

url = baseUrl + '/user/account'
params = {
    'uid': myUserId
}
userAccount = requests.get(url, headers=headers, params=params).json()
# print(json.dumps(userAccount, ensure_ascii=False))
print('UserName:', userAccount['profile']['userName'])
# print('UserName:', userAccount['account']['userName'])

url = baseUrl + '/user/subcount'
params = {
    'uid': myUserId
}
userSubcount = requests.get(url, headers=headers, params=params).json()
# print(json.dumps(userSubcount, ensure_ascii=False))
print('Followed Artists:', userSubcount['artistCount'])
print('Created Playlists:', userSubcount['createdPlaylistCount'])
print('Subscribed Playlists:', userSubcount['subPlaylistCount'])
