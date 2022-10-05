import time
from common import *


# Defin cookie in cookie.txt
headers['cookie'] = readFileContent('cookie.txt')


# Sure check
sureCheck()

# Get all follows
follows = getFollows(myUserId)
# print(json.dumps(follows, ensure_ascii=False))
# writeJsonToFile(follows, 'all_my_follows_bak_2022-10-05')
followUsers = {follow['userId']: follow['nickname']
               for follow in follows['follow']}
print(followUsers)
print('Total:', len(followUsers))

# Unfollow all
for followId, userName in followUsers.items():
    print('Unfollowing', userName)
    res = unfollowUser(followId)
    print(res, res.text)
    time.sleep(3)
