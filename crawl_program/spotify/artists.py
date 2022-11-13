# Deine artist to crawl
artistToCrawl = 'hacken_lee'

# Deine artists to generate playlists
# (Search artist on spotfy (e.g. 张学友 on spotify) to get artistId)
# Define generate method: 1 - by number, 2 - by playcount
# For method 1: Define track number to add tracks
# For method 2: Define minimum playcount to add tracks
generateArtists = {
    'andy_lau': {
        'name': '刘德华',
        'artistId': '2n3uDrupL8UtFSeZhY38MS',
        'generateInfo': {
            'generateMethod': 1,
            'number': 30
        }
    },
    'hacken_lee': {
        'name': '李克勤',
        'artistId': '3PV11RNUoGfX9tMN2wVljB',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'tanya_chua': {
        'name': '蔡健雅',
        'artistId': '376pcuw4IgWBMOUwCr8kIm',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'michael_jackson': {
        'name': 'Michael Jackson',
        'artistId': '3fMbdgg4jU18AjLCKBhRSm',
        'generateInfo': {
            'generateMethod': 1,
            'number': 50
        }
    },
    'ariana_grande': {
        'name': 'Ariana Grande',
        'artistId': '66CXWjxzNUsdJxJ2JdwvnR',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'huahua': {
        'name': '华晨宇',  # 2013年快乐男声全国总冠军
        'artistId': '7v7bP8NfcMYh4sDADEAy6Z',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'billie_eilish': {
        'name': 'Billie Eilish',
        'artistId': '6qqNVTkY8uBg9cP3Jd7DAH',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'stefanie_sun': {
        'name': '孙燕姿',
        'artistId': '0SIXZXJCAhNU8sxK0qm7hn',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'jam_hsiao': {
        'name': '萧敬腾',  # 2007年台湾第一届超级星光大道踢馆成名
        'artistId': '4AJcTAMOLkRl3vf4syay8Q',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'adele': {
        'name': 'Adele',
        'artistId': '4dpARuHxo51G3z768sgnrY',
        'generateInfo': {
            'generateMethod': 2,
            'number': 100000000
        }
    },
    'mayday': {
        'name': '五月天',
        'artistId': '16s0YTFcyjP4kgFwt7ktrY',
        'generateInfo': {
            'generateMethod': 1,
            'number': 30
        }
    },
    'karen_mok': {
        'name': '莫文蔚',
        'artistId': '6jlz5QSUqbKE4vnzo2qfP1',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'faye_wong': {
        'name': '王菲',
        'artistId': '3df3XLKuqTQ6iOSmi0K3Wp',
        'generateInfo': {
            'generateMethod': 1,
            'number': 30
        }
    },
    'wangfeng': {
        'name': '汪峰',
        'artistId': '10LslMPb7P5j9L2QXGZBmM',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'beyond': {
        'name': 'Beyond',
        'artistId': '4F5TrtYYxsVM1PhbtISE5m',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'leehom_wang': {
        'name': '王力宏',
        'artistId': '2F5W6Rsxwzg0plQ0w8dSyt',
        'generateInfo': {
            'generateMethod': 1,
            'number': 25
        }
    },
    'xusong': {
        'name': '许嵩',
        'artistId': '2hgxWUG24w1cFLBlPSEVcV',
        'generateInfo': {
            'generateMethod': 1,
            'number': 25
        }
    },
    'jj_lin': {
        'name': '林俊杰',
        'artistId': '7Dx7RhX0mFuXhCOUgB01uM',
        'generateInfo': {
            'generateMethod': 2,
            'number': 6000000
        }
    },
    'g_e_m': {
        'name': '邓紫棋',
        'artistId': '7aRC4L63dBn3CiLDuWaLSI',
        'generateInfo': {
            'generateMethod': 1,
            'number': 30
        }
    },
    'bruno_mars': {
        'name': 'Bruno Mars',
        'artistId': '0du5cEVh5yTK9QJze8zA0C',
        'generateInfo': {
            'generateMethod': 1,
            'number': 20
        }
    },
    'eason_chan': {
        'name': '陈奕迅',
        'artistId': '2QcZxAgcs2I1q7CtCkl6MI',
        'generateInfo': {
            'generateMethod': 2,
            'number': 5000000
        }
    },
    'jay_chou': {
        'name': '周杰伦',
        'artistId': '2elBjNSdBE2Y3f0j1mjrql',
        'generateInfo': {
            'generateMethod': 2,
            'number': 5000000
        }
    },
    'jacky_cheung': {
        'name': '张学友',
        'artistId': '1Hu58yHg2CXNfDhlPd7Tdd',
        'generateInfo': {
            'generateMethod': 1,
            'number': 50
        }
    }
}

# Define other artists
otherArtists = {
    'haoyun': {
        'name': '郝云',
        'artistId': '7rHYKc9hKD1bCHiuKv2R09'
    },
    'hailun': {
        'name': '海伦',
        'artistId': '2f9O9Vy7xlAghr07uxXYMh'
    },
    # Don't belong here
    # 'tylor_swift': {
    #     'name': 'Taylor Swift',
    #     'artistId': '06HL4z0CvFAxyc27GXpf02'
    # },
    # 'tones_and_i': {
    #     'name': 'Tones And I',
    #     'artistId': '2NjfBq1NflQcKSeiDooVjY'
    # },
    # Spotify only
    # 'chenyifa': {
    #     'name': '陈一发',
    #     'artistId': '10xtjTRMlKZ7aFx6VBQlSj'
    # },
    # 'namewee': {
    #     'name': '黄明志',
    #     'artistId': '24jrxG0tKcwgAzsLuPzyMi'
    # },
    # More hits (>3)
    'zhousihan-2': {
        'name': '周思涵',
        'artistId': '0ba03M9f4Zxx9oSqpKmo2T'
    },
    'zhousihan': {
        'name': '阿涵',
        'artistId': '0Nu7uGMynoaIdKnfLRgxJ8'
    },
    'chenli': {
        'name': '陈粒',
        'artistId': '3SyC3U06X0DjdWd2Jf6V8Q'
    },
    'zhangbichen': {
        'name': '张碧晨',  # 2014年中国好声音第三季年度冠军
        'artistId': '7n6JzP9GxGVVzXG0t0gLu3'
    },
    'gebilaofan': {
        'name': '隔壁老樊',
        'artistId': '1lGtvqG3JDiT3bbnJaCxfe'
    },
    'zhaolei-2': {
        'name': '赵雷2',
        'artistId': '7EP8l31VxgD0MAOwh7uez5'
    },
    'zhaolei': {
        'name': '赵雷',
        'artistId': '2KwZ9xnULczo0Z7Y7Bp57R'
    },
    'xiechunhua': {
        'name': '谢春花',
        'artistId': '0gYt4XG9A0hyZW7rt745ZY'
    },
    'huazhou': {
        'name': '花粥',
        'artistId': '148sD27V3Nr0XFl3TZNwmw'
    },
    'asi': {
        'name': '阿肆',
        'artistId': '4yamiVzQPYBb02ceSu0jaI'
    },
    # One hit (<4)
    'bojue-2': {
        'name': '伯爵Johnny2',
        'artistId': '7xzC31BgSOWsAvun3j2bSS'
    },
    'bojue': {
        'name': '伯爵Johnny',
        'artistId': '2DCXAxaM4TdCBDtx2deFn2'
    },
    'huatong': {
        'name': '花僮',  # 2013年星光大道月亚军，2014年最美和声第二季孙楠战队12强学员
        'artistId': '3bUk9TeFsLn98GnfKIzMua'
    },
    'angang': {
        'name': '暗杠',
        'artistId': '21IJ2VE7Rmqk9YMfTtE1wZ'
    },
    'jinzhiwen': {
        'name': '金志文',  # 2012年中国好声音第一季杨坤组冠军、年度总决赛第4名
        'artistId': '1p8mNyT18G4coJooY8NTGN'
    },
    'suyunying': {
        'name': '苏运莹',  # 2015年中国好歌曲第二季全国总决赛亚军
        'artistId': '63tzlZxY9iaOeUnmGfwlyA'
    },
    'baoshi_gem': {
        'name': '宝石Gem',  # 2019年参加中国新说唱2019
        'artistId': '0p0KwawjbChNZh3O0L3z8i'
    },
    'zhaoyingjun': {
        'name': '赵英俊',  # 2004年我型我秀全国20强
        'artistId': '393qzhbUiZuv7pqKjjUSqq'
    },
    'maixiaodou': {
        'name': '麦小兜',
        'artistId': '6sgZgnXFneErJ5HtO9bj9t'
    },
    'mailajiaoyeyongquan': {
        'name': '买辣椒也用券',
        'artistId': '3nG9ei7y7HUPIN8nE5Nyyx'
    },
    'xujiahao': {
        'name': '烟(许佳豪)',
        'artistId': '2DXogZyZTpItlsIGCG6Qpt'
    },
    'yuanyawei': {
        'name': '袁娅维',  # 2012年中国好声音第一季刘欢组四强
        'artistId': '70paW48PtCtUjtndElrjrL'
    },
    'kelly_yu': {
        'name': '于文文',
        'artistId': '5R56NYbLCC2HpOwlYBnmeN'
    },
    'yinqueshiting': {
        'name': '音阙诗听',
        'artistId': '6JZIgN9gEgNSS8lY5pmwbx'
    },
    'liushuang': {
        'name': '柳爽',
        'artistId': '7vzmSiBMYT0aSIjHFoWbhV'
    },
    'zhanzhanyuluoluo': {
        'name': '展展与罗罗',
        'artistId': '7jqlVGxCx6cj6o9FPmO98s'
    },
    'daiquan': {
        'name': '戴荃',
        'artistId': '20vLqxWyyRuMaNpMsgZOI6'
    },
    'rensuxi': {
        'name': '任素汐',
        'artistId': '16rAFXQVz2WBpTH9uc1LA8'
    },
    'fangdongdemao': {
        'name': '房东的猫',
        'artistId': '6oxtUCWftDouZzeso3oXcF'
    },
    'madi': {
        'name': '马頔',
        'artistId': '6INLZbPHXGj6ERrjFGPYD6'
    },
    'maliang': {
        'name': '马良',
        'artistId': '713WTosB61RDO5KwQtNKQA'
    },
    'luxianshenyuedui': {
        'name': '鹿先森乐队',
        'artistId': '4SklOYXOJe2H6R1Vz2gc0F'
    },
    'xufei': {
        'name': '许飞',  # 2006年超级女生第三届全国总决赛第6名
        'artistId': '7jQNVznzEejg5gU5B0AmfQ'
    },
    'chenhongyu': {
        'name': '陈鸿宇',
        'artistId': '7ukU2IyqxXp80Jnxf4lzTv'
    },
    'wangerlang-2': {
        'name': '王贰浪2',
        'artistId': '6qXHEV470p1bYHxkTSVrRs'
    },
    'wangerlang': {
        'name': '王贰浪',
        'artistId': '6jNRSV0cd0kL5Tfz6JPxZA'
    },
    'wangheye': {
        'name': '王赫野',
        'artistId': '2sAy0e2cL6jbo0ukxlxWNJ'
    },
    'usa_for_africa': {
        'name': 'U.S.A. For Africa',
        'artistId': '7sF6m3PpW6G6m6J2gzzmzM'
    },
    'liujinrui': {
        'name': '刘瑾睿',
        'artistId': '0ySwuPxQeg9GsjWO92RVLF'
    },
    'baisong': {
        'name': '柏松',
        'artistId': '5dGgQ6EQsfOPRiv2V0b846'
    },
    # Nah
    # 'gai_zhouyan': {
    #     'name': 'GAI周延',  # 2017年中国有嘻哈第一季并列冠军
    #     'artistId': '37EUUUGKMLP6KSKrN9q39m'
    # }
}

artists = otherArtists | generateArtists
