# Spotify name : Netease name
# traditional Chinese
specialSongNames = {
    # 张学友  All
    'jacky_cheung': {
        '祇願一生愛一人': '只愿一生爱一人',
        '袛有情永在': '只有情永在',
        '我醒著做夢': '我醒着做梦',
        '祇有你不知道': '只有你不知道'
    },
    # 周杰伦  All
    'jay_chou': {
        '等你下課': '等你下课 (with 杨瑞代)',
        '愛在西元前': '爱在西元前',
        '爸我回來了': '爸，我回来了',
        '蛇 舞': '蛇舞',
        '花 海': '花海',
        '免費教學錄影帶': '免费教学录影带'
    },
    # 陈奕迅 All
    'eason_chan': {
        'Wu Ren Zhi Jing': '无人之境',
        '孤獨患者(國)': '孤独患者'
    },
    # Bruno Mars  All
    'bruno_mars': {
    },
    # 邓紫棋  Missing: 漂向北方(with 黄明志)
    'g_e_m': {
        '畫': '画 (Live Piano Session II)',
        'WALK ON WATER': 'Walk On Water'
    },
    # 林俊杰  Missing: Lose Control(电影尚气主题曲)
    'jj_lin': {
        'Bedroom': 'Bedroom (feat. Anne-Marie)',
        'Stay With You': 'Stay With You (英文版)'
    },
    # 许嵩  All
    'xusong': {
    },
    # 王力宏  Missing: 漂向北方(with 黄明志)
    'leehom_wang': {
    },
    # Beyond  Missing: 长城、岁月无声
    'beyond': {
    },
    # 汪峰  All
    'wangfeng': {
    },
    # 王菲  All
    'faye_wong': {
        '執迷不悔': '执迷不悔 (粤语版)',
        '你快樂所以我快樂': '你快乐所以我快乐 (Live)'
    },
    # 莫文蔚  All
    'kare_mok': {
    },
    # 五月天  All
    'mayday': {
        '好好': '好好 (想把你写成一首歌)',
        '青春の彼方 / 盛夏光年': '盛夏光年',
        '愛情的模樣 Life Live': '爱情的模样',
        '知足(07\'最知足版)': '知足 (07 最知足版)'
    },
    # Adele  All
    'adele': {
        'Send My Love': 'Send My Love (To Your New Lover)',
        'Skyfall': 'Skyfall (Full Length)'
    },
    # 萧敬腾  All
    'jam_hsiao': {
        '矜持': '矜持 (Studio Live)',
        '袖手旁觀': '袖手旁观 (Studio Live)'
    },
    # 孙燕姿  All
    'stefanie_sun': {
        'Stay With You': 'Stay With You (英文版)',
        '克卜勒': '克卜勒'
    },
    # Billie Eilish  All
    'billie_eilish': {
    },
    # 华晨宇  All
    'huahua': {
    },
    # Ariana Grande  All
    'ariana_grande': {
        'Save Your Tears': 'Save Your Tears (Remix)'
    },
    # Michael Jackson  Missing: Don’t Matter To Me
    'michael_jackson': {
        'Rock with You': 'Rock With You',
        'P.Y.T.': 'P.Y.T. (Pretty Young Thing)',
        'We Are The World': 'We Are the World (Live)',
        'Give In to Me': 'Give in to Me',
        'Another Part of Me': 'Another Part Of Me'
    }
}

# Not included in netease artist songs
# simplified Chinese
specialSongIds = {
    # 周杰伦
    'jay_chou': {
        '屋顶': 298317,
        '画沙': 324859
    },
    # 邓紫棋
    'g_e_m': {
        '手心的蔷薇': 29848657
    },
    # Bruno Mars
    'bruno_mars': {
        'Young, Wild & Free': 1934807,
        'Billionaire': 21806689
    },
    # 林俊杰
    'jj_lin':  {
        '期待你的爱': 34040694
    },
    # 王菲
    'faye_wong':  {
        '因为爱情': 64317
    },
    # 五月天
    'mayday': {
        '黑暗骑士': 25794008
    },
    # 萧敬腾
    'jam_hsiao': {
        '一眼瞬间': 326899
    },
    # Billie Eilish
    'billie_eilish': {
        'Bored': 468738965
    },
    # Michael Jackson
    'michael_jackson': {
        'Don’t Matter To Me': 574926603
    }
}

# Netease not good song source，e.g. 你的名字 我的姓氏(友个人演唱会1999)
replaceSongIds = {
    # 张学友
    'jacky_cheung': {
        '你的名字 我的姓氏': 188728
    }
}

# Not included because of spotify repeated song names
repeatedSongs = {
    # 陈奕迅
    'eason_chan': [{
        'K歌之王__国(反正是我)': 67364
    }],
    # 王菲
    'faye_wong': [{
        '执迷不悔 (国语版)': 300603
    }],
    # Michael Jackson
    'michael_jackson': [{
        'Love Never Felt So Good': 1299086142
    }]
}

# Netease sensitive words
sensitiveWords = {
    '长城': '长Cheng',
    '岁月无声': '岁月WuSheng'
}
