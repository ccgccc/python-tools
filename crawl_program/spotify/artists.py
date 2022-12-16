# Define artist to crawl
artistToCrawl = "coldplay"

# === Define artists to generate playlists
# (Search artist on spotfy (e.g. 张学友 on spotify) to get artistId)
# Define generate method: 1 - by number, 2 - by playcount
# For method 1: Define track number to add tracks
# For method 2: Define minimum playcount to add tracks
generateArtists = {
    # ---------- Split
    "coldplay": {
        "name": "Coldplay",
        "artistId": "4gzpq5DPGxSnKTe4SA8HAU",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 15
        }
    },
    "沙宝亮": {
        "name": "沙宝亮",
        "artistId": "4ef3Gqwh0lqBGVWcmNIThQ"
    },
    "汤潮": {
        "name": "汤潮",
        "artistId": "6Cw3GkCetFiwFV9blLfvfD"
    },
    "至上励合": {
        "name": "至上励合",
        "artistId": "1I07lqAx39utkxt5zkC475"
    },
    "韩磊": {
        "name": "韩磊",
        "artistId": "7puBL0AvJjalTgoPePIigh"
    },
    "徐誉滕_xu_yu_teng": {
        "name": "徐誉滕 Xu Yu Teng",
        "artistId": "1vVpQbgOTGxegFcKGCak9O"
    },
    "腾格尔": {
        "name": "腾格尔",
        "artistId": "5U99oKyYA9vz0hEmEU1NjN"
    },
    "縱貫線": {
        "name": "纵贯线",
        "artistId": "1H7vlkyLUbFo5sFhvhBh8K"
    },
    "降央卓玛": {
        "name": "降央卓玛",
        "artistId": "37prLIatkel3p0BKETTK62"
    },
    "崔健": {
        "name": "崔健",
        "artistId": "1YwBQZlsK015NpwaF8gpd9"
    },
    "唐朝": {
        "name": "唐朝",
        "artistId": "3gAbcvLOMgHwAgNPN2bo8N"
    },
    "胡歌": {
        "name": "胡歌",
        "artistId": "04T9gfyccsmxG79OSJp5r1"
    },
    "bibi_zhou": {
        "name": "周笔畅",
        "artistId": "3WHsy1Rq4vPEdRyo9P3a48"
    },
    "lowell_lo": {
        "name": "卢冠廷",
        "artistId": "0PBs3xfhn0PA6irWFrknJ4"
    },
    "劉惜君": {
        "name": "刘惜君",
        "artistId": "46OJt1hMEeXtny1BebzNMF"
    },
    "pong_nan": {
        "name": "蓝奕邦",
        "artistId": "6G7bdG4rBz6OQgKudNjoGL"
    },
    "韓紅": {
        "name": "韩红",
        "artistId": "1kLqxXjyc7OwDJopftAH86"
    },
    "邰正宵": {
        "name": "邰正宵",
        "artistId": "4t3kmZV59tEONpRUZmXjpP"
    },
    "yuki_hsu": {
        "name": "徐怀钰",
        "artistId": "06w51RzkHkpkp2x09REY7v"
    },
    "金莎": {
        "name": "金莎",
        "artistId": "0wK3rMwogVowmeXArZN29T"
    },
    "刀郎": {
        "name": "刀郎",
        "artistId": "0EUH8U3HHClbdLO3m46EOv"
    },
    "鄭智化": {
        "name": "郑智化",
        "artistId": "2DqYjQiVXvk7yFkqpVb5wX"
    },
    "lara_liang": {
        "name": "梁心颐",
        "artistId": "4VgfrD5wuAoN428fBZNSyW"
    },
    "黑豹": {
        "name": "黑豹",
        "artistId": "0zj66XhQP4EPkat7XkBYL0"
    },
    "shunza": {
        "name": "顺子",
        "artistId": "2zXcyd0DsDOxZc1nSGepMb"
    },
    "劉瑞琦": {
        "name": "刘瑞琦",
        "artistId": "4mpD7eRd38R1tUcheDWrxQ"
    },
    "六哲": {
        "name": "六哲",
        "artistId": "1iVhYU0gUs9N5kDs22AtFV"
    },
    "孟庭葦": {
        "name": "孟庭苇",
        "artistId": "2Ovp3J8JzCirwcGAgvK9cQ"
    },
    "jackie_chan": {
        "name": "成龙",
        "artistId": "0wVKXWiOMLfqmFCdCPR7Ar"
    },
    "kenny_bee": {
        "name": "钟镇涛",
        "artistId": "1SnFcgaLa1l0bV8ZOEL3Cg"
    },
    "michael_kwan": {
        "name": "关正杰",
        "artistId": "6t12u8eGw0eN6AcMtUMkoG"
    },
    "terence_siufay": {
        "name": "小肥",
        "artistId": "3AemIC066y8n3TetXWkVoE"
    },
    "fama": {
        "name": "农夫",
        "artistId": "7BcyMcADGhD6WB6XFAJFEa"
    },
    "wanting": {
        "name": "曲婉婷",
        "artistId": "2OC4lXfGEKZkbmRCcf2vTq"
    },
    "黃品源": {
        "name": "黄品源",
        "artistId": "22eZSsFE2fxLnnC9Zga25b"
    },
    "shirley_kwan": {
        "name": "关淑怡",
        "artistId": "14hV8HTKYMZ5nzeaLdLp63"
    },
    "卓文萱": {
        "name": "卓文萱",
        "artistId": "5XHBjJm3bCgQCjpnInCxfT"
    },
    "cass_phang": {
        "name": "彭羚",
        "artistId": "0RkQt8LMVrxCjQb9BxpBfF"
    },
    "gary_chaw": {
        "name": "曹格",
        "artistId": "1mfzcypCggFwpCJ1gmi8BK"
    },
    "steve_chou": {
        "name": "周传雄",
        "artistId": "1Qneon4tYZ7srVOU91bTsO"
    },
    "tiger_hu": {
        "name": "胡彦斌",
        "artistId": "3PpIzdLny8HwTnKp9joXdj"
    },
    "nicky_lee": {
        "name": "李玖哲",
        "artistId": "6DuHQk8gJbyVlhajer8IuF"
    },
    "coco_lee": {
        "name": "李玟",
        "artistId": "3ioHf138TiMxYRCWmC8yJX"
    },
    "kenji_wu": {
        "name": "吴克群",
        "artistId": "1MgybycH8k36NX0Ifzlddb"
    },
    "dave_wong": {
        "name": "王杰",
        "artistId": "5XMnJOQbE6OuOvcV8fn3Wg"
    },
    "lizhi": {
        "name": "李志",
        "artistId": "1fqb04dI9vaEcGDbIVrcib"
    },
    "michael_wong": {
        "name": "光良",
        "artistId": "26SQFo2qNNGOxh2PUAsTeO"
    },
    "jeff_chang": {
        "name": "张信哲",
        "artistId": "2dw80Uni5l7wd9zZFn7Ltu"
    },
    # === Crawled
    # "sally_yeh": {
    #     "name": "叶蒨文",
    #     "artistId": "7Bx0SBZoIX73eywmBcdqFb"
    # },
    "eve_ai": {
        "name": "艾怡良",
        "artistId": "6eLpNMX3ZygSrUuxAlIWIx"
    },
    "jane_zhang": {
        "name": "张靓颖",
        "artistId": "7qJmFr579WC8MMGj4PiWdu"
    },
    "christine_fan": {
        "name": "范玮琪",
        "artistId": "1q7sCl0vg0EcaFdRz0XDGg"
    },
    "hebe_tien": {
        "name": "田馥甄",
        "artistId": "14bJhryXGk6H6qlGzwj3W5"
    },
    "jolin_tsai": {
        "name": "蔡依林",
        "artistId": "1r9DuPTHiQ7hnRRZ99B8nL"
    },
    "fish_leong": {
        "name": "梁静茹",
        "artistId": "3aIDSTKS9yH745GUQBxDcS"
    },
    "dazhuang": {
        "name": "大壮",
        "artistId": "0JvihWUI0PyC4sEJGVwrAg"
    },
    "gaojin": {
        "name": "高进",
        "artistId": "0GjIwBSdhGj3vLVoCunPzm"
    },
    "xianzi": {
        "name": "弦子",
        "artistId": "2CBuGdj5Nmgx1VfrgLnGoJ"
    },
    "houxian": {
        "name": "后弦",
        "artistId": "46leOMfvDoDoujesrjjbeG"
    },
    "benxi": {
        "name": "本兮",
        "artistId": "41WH5ZIopoJCdOhkYDmblM"
    },
    "xuliang": {
        "name": "徐良",
        "artistId": "6sqXIwIIs1LWj6OQuBVPpR"
    },
    "silence_wang": {
        "name": "汪苏泷",
        "artistId": "0PdNEiQ3MsJGCEgE13Tz60"
    },
    "haomeimei": {
        "name": "好妹妹",
        "artistId": "55WwHAHZZasWq8QM0LF5JR"
    },
    "songdongye": {
        "name": "宋冬野",
        "artistId": "5aJFmaCc09jEz9ghzppUxo"
    },
    "jike_junyi": {
        "name": "吉克隽逸",
        "artistId": "2dIGGnfI63aDJNR6eL50AZ"
    },
    "chris_lee": {
        "name": "李宇春",
        "artistId": "02VPWD8AZ7qSuug0dM4Hk1"
    },
    "kuaizixiongdi": {
        "name": "筷子兄弟",
        "artistId": "6R2AgShAYIEOkulvSSant5"
    },
    "yangkun": {
        "name": "杨坤",
        "artistId": "7Dc62n8zZBrx6SsNDfmF9O"
    },
    "yu_quan": {
        "name": "羽泉",
        "artistId": "4jkXpEWzunLc5WnHSEiDMf"
    },
    "escape_plan": {
        "name": "逃跑计划",
        "artistId": "3eJTjQEMzEeoS4n6aJXhKM"
    },
    "wowkie_da": {
        "name": "大张伟",
        "artistId": "3RIgMUtdfRx98Lm5bXM3GD"
    },
    "huaeryuedui": {
        "name": "花儿乐队",
        "artistId": "1ipRvm81MI5PnM6mmBppmy"
    },
    "mc_hotdog": {
        "name": "MC HotDog",
        "artistId": "4maR8o69pil8CrclOiFVVW"
    },
    "zhangzhenyue": {
        "name": "张震岳",
        "artistId": "6PNEi9i2MxUgRufqYr76Xt"
    },
    "jordan_chan": {
        "name": "陈小春",
        "artistId": "4EefQ1H6Qg9W5Gv7eVLC9U"
    },
    "ekin_cheng": {
        "name": "郑伊健",
        "artistId": "2DNe29u3NiB7u8k8RS5IuD"
    },
    "nanquanmama": {
        "name": "南拳妈妈",
        "artistId": "48Smhc0ISwYYRSad1uXSns"
    },
    "by2": {
        "name": "BY2",
        "artistId": "3DOs7Bsr9x4eJHqv6ViPvR"
    },
    "feiyuqing": {
        "name": "费玉清",
        "artistId": "6aSJ9LaNaHOKiPchLDYGYl"
    },
    "harlem_yu": {
        "name": "庾澄庆",
        "artistId": "6VbRanWSU3pdDhJnhSfGmY"
    },
    "deserts_chang": {
        "name": "张悬",
        "artistId": "7v9Il42LvvTeSfmf1bwfNx"
    },
    "justin_lo": {
        "name": "侧田",
        "artistId": "3lva01D3HtmlEKjuxAZ7bC"
    },
    "pakho_chau": {
        "name": "周柏豪",
        "artistId": "38t0Qk7AJg7YdrXmOC6TH1"
    },
    "ronald_cheng": {
        "name": "郑中基",
        "artistId": "66FF9LF0uO3W1zxEN0m8uN"
    },
    "aaron_kwok": {
        "name": "郭富城",
        "artistId": "3lbgPpyP2yep0sqwWTgasT"
    },
    "leon_lai": {
        "name": "黎明",
        "artistId": "0ubIxkefJsoYY8JXc2HJoa"
    },
    "yangpeian": {
        "name": "杨培安",
        "artistId": "5zxmrXIwrLuSfIJM3Dz6y1"
    },
    "tianzhen": {
        "name": "田震",
        "artistId": "09mk8X1qeA7JlMHMSmqw7c"
    },
    "naying": {
        "name": "那英",
        "artistId": "35ig3ZjuqVyGeovLsj4xNm"
    },
    "liuhuan": {
        "name": "刘欢",
        "artistId": "3K4aEHMBQbW2hJVAhooLGy"
    },
    "joey_yung": {
        "name": "容祖儿",
        "artistId": "2zzKlxMsKTPMsZacZCPRNA"
    },
    "yisa_yu": {
        "name": "郁可唯",
        "artistId": "75CM5fojYdKYD0xYSFh22Z"
    },
    # "della": {
    #     "name": "丁当",
    #     "artistId": "1EUq1MC4vfYYxcVK9aJnXf"
    # },
    "khalil_fong": {
        "name": "方大同",
        "artistId": "1YrtUPrWcPfgdl9BaD9nhd"
    },
    "will_pan": {
        "name": "潘玮柏",
        "artistId": "7fCFxj1GCRqwFZEP4iJRw0"
    },
    "maobuyi": {
        "name": "毛不易",
        "artistId": "6gvSKE72vF6N20LfBqrDmm"
    },
    "sandy_lam": {
        "name": "林忆莲",
        "artistId": "3K2hOAx9MPhduvDf2qguro"
    },
    "sammi_cheng": {
        "name": "郑秀文",
        "artistId": "3XCnp5UV5wnNw49Xuka9qH"
    },
    "david_tao": {
        "name": "陶喆",
        "artistId": "40tNK2YedBV2jRFAHxpifB"
    },
    "teresa_teng": {
        "name": "邓丽君",
        "artistId": "3ienC90A5I1X3irDyQoqWZ"
    },
    "she": {
        "name": "S.H.E",
        "artistId": "2lWShxOL8iTlI0pmtVKvEh"
    },
    "eric_chou": {
        "name": "周兴哲",
        "artistId": "5fEQLwq1BWWQNR8GzhOIvi"
    },
    # "lady_gaga": {
    #     "name": "Lady Gaga",
    #     "artistId": "1HY2Jd0NmPuamShAr6KMms"
    # },
    "camila_cabello": {
        "name": "Camila Cabello",
        "artistId": "4nDoRrQiYLoBzwC5BhVJzF"
    },
    "snoop_dogg": {
        "name": "Snoop Dogg",
        "artistId": "7hJcb9fa4alzcOq3EaNPoG"
    },
    "david_bowie": {
        "name": "David Bowie",
        "artistId": "0oSGxfWSnnOXhD2fKuz2Gy"
    },
    "whitney_houston": {
        "name": "Whitney Houston",
        "artistId": "6XpaIBNiVzIetEPCWDvAFP"
    },
    "beyonce": {
        "name": "Beyoncé",
        "artistId": "6vWDO969PvNqNYHIOW5v0m"
    },
    "selena_gomez": {
        "name": "Selena Gomez",
        "artistId": "0C8ZW7ezQVs4URX5aX7Kqx"
    },
    "rihanna": {
        "name": "Rihanna",
        "artistId": "5pKCCKE2ajJHZ9KAiaK11H"
    },
    "justin_bieber": {
        "name": "Justin Bieber",
        "artistId": "1uNFoZAHBGtllmzznpCI3s"
    },
    "queen": {
        "name": "Queen",
        "artistId": "1dfeR4HaWDbWqFHLkxsg1d"
    },
    "the_beatles": {
        "name": "The Beatles",
        "artistId": "3WrFJ7ztbogyGnTHbHJFl2"
    },
    "eminem": {
        "name": "Eminem",
        "artistId": "7dGJo4pcD2V6oG8kP0tJRR"
    },
    "ed_sheeran": {
        "name": "Ed Sheeran",
        "artistId": "6eUKZXaKkcviH0Ku9w2n3V"
    },
    "zhangjie": {  # 待定
        "name": "张杰",
        "artistId": "75udD9hen8NeHTe92rUNLa"
    },
    "zhoushen": {
        "name": "周深",
        "artistId": "0BezPR1Hn38i8qShQKunSD"
    },
    "wuqingfeng": {
        "name": "吴青峰",
        "artistId": "5a5vu4RzsAHdKN0aYyblZ8"
    },
    "sodagreen": {
        "name": "苏打绿",
        "artistId": "3WYT2b8pOLsLsqSaoWYr7U"
    },
    # "jackson_wang": {
    #     "name": "王嘉尔",
    #     "artistId": "1kfWoWgCugPkyxQP8lkRlY"
    # },
    "arong": {
        "name": "阿冗",
        "artistId": "3dTgjg7lzUGiD3NwcGCK1n"
    },
    "xinyuetuan": {
        "name": "信乐团",
        "artistId": "1YfpT6Dl8tJDmYQKWRoxjn"
    },
    "linzhixuan": {
        "name": "林志炫",
        "artistId": "6O9BAkGBRRzHUDrWqdT68r"
    },
    "jason_chan": {
        "name": "陈柏宇",
        "artistId": "1IDuSpntFl2Mutofvrrutc"
    },
    "huxia": {
        "name": "胡夏",  # 2010-12-14
        "artistId": "3iRqbMhzyOyoCkmmMRxLWR"
    },
    "huangling": {
        "name": "黄龄",
        "artistId": "6OAQlHABRwPJYVTkaSmiJ9"
    },
    "sa_dingding": {
        "name": "萨顶顶",  # 2007-01-01
        "artistId": "5HCoNna7Jrw9YGVvo4lg1a"
    },
    "li_yugang": {
        "name": "李玉刚",  # 2010-01-01
        "artistId": "3PI2UCRk6X5prLnFr05QQK"
    },
    "laolang-2": {
        "name": "老狼2",
        "artistId": "0xNZutIrvMMbw2u9ww3oMD"
    },
    "laolang": {
        "name": "老狼",  # 1995-05-01
        "artistId": "1piwhsT7JM9pBzmLcLCg8v"
    },
    "chyi_chin": {  # 1985-12-15
        "name": "齐秦",
        "artistId": "4VhiuMC32Qj7pVW3e6Nlms"
    },
    "hins_cheung": {
        "name": "张敬轩",
        "artistId": "2MVfNjocvNrE03cQuxpsWK"
    },
    "cheer_chen": {
        "name": "陈绮贞",
        "artistId": "4m0xrEWYU0yCUFMaga015T"
    },
    "aska_yang": {
        "name": "杨宗纬",
        "artistId": "2SOrfXWlb17EoCqupfGX4u"
    },
    "a_lin": {
        "name": "黄丽玲",
        "artistId": "28gf2piFx6cAKOMIwcky5a"
    },
    "lala_hsu": {
        "name": "徐佳莹",
        "artistId": "3dI4Io8XE33J2o04ZwjR0Y",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 大雨將至
        }
    },
    # === Candidates
    # "leslie_cheung": {
    #     "name": "张国荣",  # 1978-01-01
    #     "artistId": "2g0QLUYku8AuPVK2udRV7i",
    #     "generateInfo": {
    #         "generateMethod": 1,
    #         "number": 30  # 拒絕再玩
    #     }
    # },
    # "lironghao": {
    #     "name": "李荣浩",  # 2013-09-16
    #     "artistId": "0rTP0x4vRFSDbhtqcCqc8K",
    #     "generateInfo": {
    #         "generateMethod": 1,
    #         "number": 20  # 作曲家
    #     }
    # },
    "joker_xue": {
        "name": "薛之谦",  # 2006-06-09
        "artistId": "1cg0bYpP5e2DNG0RgK2CMN",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 怪咖
        }
    },
    "angela_chang": {
        "name": "张韶涵",  # 2003-05-01
        "artistId": "4txug0T3vYc9p20tuhfCUa",
        "filterAlbums": False,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 不害怕，Missing：淋雨一直走、篇章
        }
    },
    "rene_liu": {
        "name": "刘若英",  # 1992-08-07
        "artistId": "6qzfo7jiO4OrhxrvPFPlWX",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 15  # 我很好
        }
    },
    "wubai": {
        "name": "伍佰",  # 1992-04-16
        "artistId": "5H8TJITZE1sPjVR2ACzXNS",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 與妳到永久
        }
    },
    "jonathan_lee": {
        "name": "李宗盛",  # 1985-03-27
        "artistId": "2TXF68WgfTZlipUvLBsQre",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 在晴朗的天空下(粵)
        }
    },
    "luodayou": {
        "name": "罗大佑",  # 1981-11-18
        "artistId": "7tuWI2luTp61HHGmviWid8",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 閃亮的日子
        }
    },
    "danny_chan": {
        "name": "陈百强",  # 1979-01-01
        "artistId": "0Q43SYcicELiBaGB9N9aBI",
        "generateInfo": {
            "generateMethod": 1,
            "number": 15  # 凝望
        }
    },
    "kary_ng": {
        "name": "吴雨霏",  # 2003-01-01
        "artistId": "3B9ZmIcte26paTCaI1PFKE",
        "generateInfo": {
            "generateMethod": 1,
            "number": 15  # 雞蛋愛石頭，Missing: 生生世世爱
        }
    },
    "tylor_swift": {
        "name": "Tylor Swift",  # 2006-10-24
        "artistId": "06HL4z0CvFAxyc27GXpf02",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # Cruel Summer
        }
    },
    "zhangyusheng": {
        "name": "张雨生",  # 1988-05-01
        "artistId": "3LefT7hR0PJgShJNQoPns5",
        "generateInfo": {
            "generateMethod": 1,
            "number": 9  # 一天到晚游泳的魚
        }
    },
    "sarah_chen": {
        "name": "陈淑桦",  # 1971-01-01
        "artistId": "19tf1og71pOYoYOdqyozs2",
        "generateInfo": {
            "generateMethod": 1,
            "number": 7  # 你走你的路
        }
    },
    "richie_jen": {
        "name": "任贤齐",  # 1990-01-01
        "artistId": "0zjNCSqeDIxn63crtDx7G2",
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 花好月圓夜 - 廣東版
        }
    },
    "grasshopper": {
        "name": "草蜢",  # 1988-02-26
        "artistId": "5IxPdROZmnCyD6TBuSJMYE",
        "filterAlbums": False,
        "generateInfo": {
            "generateMethod": 1,
            "number": 7  # 半點心
        }
    },
    "charlene_choi": {
        "name": "蔡卓妍",  # 2003
        "artistId": "6wBoKKHhGDrxVtp6XMFpIP",
        "generateInfo": {
            "generateMethod": 1,
            "number": 5  # 明明
        }
    },
    "twins": {
        "name": "Twins",  # 2001-08-15
        "artistId": "7jXoGtR69J2iYCefc58MZX",
        "generateInfo": {
            "generateMethod": 1,
            "number": 12  # 我很想愛他
        }
    },
    "kay_tse": {
        "name": "谢安琪",  # 2005-05-06
        "artistId": "6XtWdWAC7rNqXwbs8hGqP9",
        "generateInfo": {
            "generateMethod": 1,
            "number": 7  # 年度之歌
        }
    },
    "miriam_yeung": {
        "name": "杨千嬅",  # 1998
        "artistId": "1rxk3vAYWeiBD2Q6FCezcl",
        "generateInfo": {
            "generateMethod": 1,
            "number": 9  # 飛女正傳
        }
    },
    "leo_ku": {
        "name": "古巨基",  # 1995-08-15
        "artistId": "4F0XzHNcfvvA2I0rGqIwAQ",
        "generateInfo": {
            "generateMethod": 1,
            "number": 5  # 勁歌. 金曲2 (情歌王)
        }
    },
    # ===== Collections
    # ----- Collection : 慧
    # "kelly_chen": {
    #     "name": "陈慧琳",  # 1990-01-01
    #     "artistId": "7KyaSSJ8uTv7Unev4z2Qc7",
    #     "generateInfo": {
    #         "generateMethod": 1,
    #         "number": 6  # 誰願放手
    #     }
    # },
    "vivian_chow": {
        "name": "周慧敏",  # 1988
        "artistId": "4bzVQLX2gMBQVMINdAGElJ",
        "generateInfo": {
            "generateMethod": 1,
            "number": 9  # 自作多情
        }
    },
    "priscilla_chan": {
        "name": "陈慧娴",  # 1984-01-01
        "artistId": "5SLOTZhruJRRGgIRtTSPc5",
        "generateInfo": {
            "generateMethod": 1,
            "number": 6  # 人生何處不相逢
        }
    },
    # ----- Collection : Big Four
    "edmond_leung": {
        "name": "梁汉文",
        "artistId": "1THfyLd3iyJYJ6X2U36K0y",
        "generateInfo": {
            "generateMethod": 1,
            "number": 2  # 纏綿遊戲
        }
    },
    "william_so": {
        "name": "苏永康",
        "artistId": "2oK5cSlJAH5s2Kx5e1zcvh",
        "generateInfo": {
            "generateMethod": 1,
            "number": 14  # 愛一個人好難
        }
    },
    "dicky_cheung-2": {
        "name": "张卫健2",
        "artistId": "3de8fL3wVnfUEtOlGIoFy5",
        "filterAlbums": False,
        "mustMainArtist": True
    },
    "andy_hui": {
        "name": "许志安",
        "artistId": "1q8BvOdpOtapWOIgO26sOn",
        "generateInfo": {
            "generateMethod": 1,
            "number": 22  # 愛妳
        }
    },
    "dicky_cheung": {
        "name": "张卫健",
        "artistId": "05U40G1dajZMe9KdTG8LTo",
        "filterAlbums": False,
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 把酒狂歌
        }
    },
    "big_four": {
        "name": "Big Four",
        "artistId": "5aV8N1m8QyReq34R3qeUx0",
        "filterAlbums": False,
        "generateInfo": {
            "generateMethod": 1,
            "number": 4  # Big Four
        }
    },
    # ----- Collection 2: 粤语前辈
    "george_lam": {
        "name": "林子祥",  # 1976
        "artistId": "7rxRHujzUzobMEbtoE297s",
        "filterAlbums": True,
        "generateInfo": {
            "generateMethod": 1,
            # "number": 11  # 數字人生
            "number": 15  # 祝福你
        }
    },
    "alan_tam": {
        "name": "谭咏麟",  # 1975, 1973 温拿
        "artistId": "5vWJrDpmd5vrDpdmgxqC5u",
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 講不出再見
        }
    },
    "sam_hui": {
        "name": "许冠杰",  # 1970
        "artistId": "1SglpJrPltamdJLLwInIL7",
        "filterAlbums": False,
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 梨渦淺笑
        }
    },
    # ----- Collection 1: 音乐诗人
    "zhengjun": {
        "name": "郑钧",
        "artistId": "5nbhd53CLcjfp7U8NDDzHw",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 4
        }
    },
    "lijian": {
        "name": "李健",
        "artistId": "47FbECPoJxk1TjHVZPzVzG",
        "filterAlbums": False,
        "generateInfo": {
            "generateMethod": 1,
            "number": 1
        }
    },
    "xuwei": {
        "name": "许巍",
        "artistId": "3qObkSIVSfNNDL1vbwL2N2",
        "generateInfo": {
            "generateMethod": 1,
            "number": 5
        }
    },
    "pushu": {
        "name": "朴树",
        "artistId": "6lJ36ifxOD2oUsdMdLRPN4",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 5
        }
    },
    # ===== Generated Artists
    "wakin_chau": {
        "name": "周华健",
        "artistId": "6wcIBaOvA9XNGgPujYZZ7L",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 最近比較煩
        }
    },
    "fenghuangchuanqi": {
        "name": "凤凰传奇",
        "artistId": "64NFGuC9PjqtNyJqnnTXh5",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "anita_mui": {
        "name": "梅艳芳",
        "artistId": "06RD8CxzApXzuhHx54BhQL",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "phil_chang": {
        "name": "张宇",
        "artistId": "7g65zUBhUAbiu4pAcoyWRd",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "shawn_mendes": {
        "name": "Shawn Mendes",
        "artistId": "7n2wHs1TKAczGzO7Dd2rGr",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "amei_chang": {
        "name": "张惠妹",
        "artistId": "6noxsCszBEEK04kCehugOp",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "andy_lau": {
        "name": "刘德华",
        "artistId": "2n3uDrupL8UtFSeZhY38MS",
        "generateInfo": {
            "generateMethod": 1,
            "number": 30
        }
    },
    "hacken_lee": {
        "name": "李克勤",
        "artistId": "3PV11RNUoGfX9tMN2wVljB",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "tanya_chua": {
        "name": "蔡健雅",
        "artistId": "376pcuw4IgWBMOUwCr8kIm",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "michael_jackson": {
        "name": "Michael Jackson",
        "artistId": "3fMbdgg4jU18AjLCKBhRSm",
        "generateInfo": {
            "generateMethod": 1,
            "number": 50
        }
    },
    "ariana_grande": {
        "name": "Ariana Grande",
        "artistId": "66CXWjxzNUsdJxJ2JdwvnR",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "huahua": {
        "name": "华晨宇",  # 2013年快乐男声全国总冠军
        "artistId": "7v7bP8NfcMYh4sDADEAy6Z",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "billie_eilish": {
        "name": "Billie Eilish",
        "artistId": "6qqNVTkY8uBg9cP3Jd7DAH",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "stefanie_sun": {
        "name": "孙燕姿",
        "artistId": "0SIXZXJCAhNU8sxK0qm7hn",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "jam_hsiao": {
        "name": "萧敬腾",  # 2007年台湾第一届超级星光大道踢馆成名
        "artistId": "4AJcTAMOLkRl3vf4syay8Q",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "adele": {
        "name": "Adele",
        "artistId": "4dpARuHxo51G3z768sgnrY",
        "generateInfo": {
            "generateMethod": 2,
            "number": 100000000
        }
    },
    "mayday": {
        "name": "五月天",
        "artistId": "16s0YTFcyjP4kgFwt7ktrY",
        "generateInfo": {
            "generateMethod": 1,
            "number": 30
        }
    },
    "karen_mok": {
        "name": "莫文蔚",
        "artistId": "6jlz5QSUqbKE4vnzo2qfP1",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "faye_wong": {
        "name": "王菲",
        "artistId": "3df3XLKuqTQ6iOSmi0K3Wp",
        "generateInfo": {
            "generateMethod": 1,
            "number": 35
        }
    },
    "wangfeng": {
        "name": "汪峰",
        "artistId": "10LslMPb7P5j9L2QXGZBmM",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "beyond": {
        "name": "Beyond",
        "artistId": "4F5TrtYYxsVM1PhbtISE5m",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "leehom_wang": {
        "name": "王力宏",
        "artistId": "2F5W6Rsxwzg0plQ0w8dSyt",
        "generateInfo": {
            "generateMethod": 1,
            "number": 25
        }
    },
    "xusong": {
        "name": "许嵩",
        "artistId": "2hgxWUG24w1cFLBlPSEVcV",
        "generateInfo": {
            "generateMethod": 1,
            "number": 25
        }
    },
    "jj_lin": {
        "name": "林俊杰",
        "artistId": "7Dx7RhX0mFuXhCOUgB01uM",
        "generateInfo": {
            "generateMethod": 2,
            "number": 6000000
        }
    },
    "g_e_m": {
        "name": "邓紫棋",
        "artistId": "7aRC4L63dBn3CiLDuWaLSI",
        "generateInfo": {
            "generateMethod": 1,
            "number": 30
        }
    },
    "bruno_mars": {
        "name": "Bruno Mars",
        "artistId": "0du5cEVh5yTK9QJze8zA0C",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "eason_chan": {
        "name": "陈奕迅",
        "artistId": "2QcZxAgcs2I1q7CtCkl6MI",
        "filterAlbums": False,
        "generateInfo": {
            "generateMethod": 2,
            "number": 5000000
        }
    },
    "jay_chou": {
        "name": "周杰伦",
        "artistId": "2elBjNSdBE2Y3f0j1mjrql",
        "generateInfo": {
            "generateMethod": 2,
            "number": 5000000
        }
    },
    "jacky_cheung": {
        "name": "张学友",
        "artistId": "1Hu58yHg2CXNfDhlPd7Tdd",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 50
        }
    }
}

# === Define other artists
otherArtists = {
    "gillian_chung": {
        "name": "钟欣潼",  # 放低過去
        "artistId": "7ICw984KHxGz5WtEzfjxG3"
    },
    "haoyun": {
        "name": "郝云",
        "artistId": "7rHYKc9hKD1bCHiuKv2R09"
    },
    "hailun": {
        "name": "海伦",
        "artistId": "2f9O9Vy7xlAghr07uxXYMh"
    },
    # ---------- Don"t belong here
    "tones_and_i": {
        "name": "Tones And I",
        "artistId": "2NjfBq1NflQcKSeiDooVjY"
    },
    # ---------- Spotify only
    # "chenyifa": {
    #     "name": "陈一发",
    #     "artistId": "10xtjTRMlKZ7aFx6VBQlSj"
    # },
    # "namewee": {
    #     "name": "黄明志",
    #     "artistId": "24jrxG0tKcwgAzsLuPzyMi"
    # },
    # ---------- More hits (>3)
    # ----- 流行
    "gebilaofan": {
        "name": "隔壁老樊",
        "artistId": "1lGtvqG3JDiT3bbnJaCxfe"
    },
    "zhangbichen": {  # *
        "name": "张碧晨",  # 2014年中国好声音第三季年度冠军
        "artistId": "7n6JzP9GxGVVzXG0t0gLu3"
    },
    "zhousihan-2": {
        "name": "周思涵",
        "artistId": "0ba03M9f4Zxx9oSqpKmo2T"
    },
    "zhousihan": {  # *
        "name": "阿涵",
        "artistId": "0Nu7uGMynoaIdKnfLRgxJ8"
    },
    "renran": {  # ***
        "name": "任然",
        "artistId": "6f4srX54JFrLNK4aTJe2Sc"
    },
    "asi": {  # **
        "name": "阿肆",
        "artistId": "4yamiVzQPYBb02ceSu0jaI",
        "filterAlbums": False
    },
    # ----- 民谣
    "huazhou": {
        "name": "花粥",
        "artistId": "148sD27V3Nr0XFl3TZNwmw"
    },
    "zhaolei-2": {
        "name": "赵雷2",
        "artistId": "7EP8l31VxgD0MAOwh7uez5"
    },
    "zhaolei": {
        "name": "赵雷",
        "artistId": "2KwZ9xnULczo0Z7Y7Bp57R"
    },
    "chenli": {  # **
        "name": "陈粒",
        "artistId": "3SyC3U06X0DjdWd2Jf6V8Q"
    },
    "xiechunhua": {
        "name": "谢春花",
        "artistId": "0gYt4XG9A0hyZW7rt745ZY"
    },
    # ---------- One hit (<4)
    "bojue-2": {
        "name": "伯爵Johnny2",
        "artistId": "7xzC31BgSOWsAvun3j2bSS"
    },
    "bojue": {
        "name": "伯爵Johnny",
        "artistId": "2DCXAxaM4TdCBDtx2deFn2"
    },
    "huatong": {
        "name": "花僮",  # 2013年星光大道月亚军，2014年最美和声第二季孙楠战队12强学员
        "artistId": "3bUk9TeFsLn98GnfKIzMua"
    },
    "angang": {
        "name": "暗杠",
        "artistId": "21IJ2VE7Rmqk9YMfTtE1wZ"
    },
    "jinzhiwen": {
        "name": "金志文",  # 2012年中国好声音第一季杨坤组冠军、年度总决赛第4名
        "artistId": "1p8mNyT18G4coJooY8NTGN"
    },
    "suyunying": {
        "name": "苏运莹",  # 2015年中国好歌曲第二季全国总决赛亚军
        "artistId": "63tzlZxY9iaOeUnmGfwlyA",
        "filterAlbums": False
    },
    "baoshi_gem": {
        "name": "宝石Gem",  # 2019年参加中国新说唱2019
        "artistId": "0p0KwawjbChNZh3O0L3z8i"
    },
    "zhaoyingjun": {
        "name": "赵英俊",  # 2004年我型我秀全国20强
        "artistId": "393qzhbUiZuv7pqKjjUSqq"
    },
    "maixiaodou": {
        "name": "麦小兜",
        "artistId": "6sgZgnXFneErJ5HtO9bj9t"
    },
    "mailajiaoyeyongquan": {
        "name": "买辣椒也用券",
        "artistId": "3nG9ei7y7HUPIN8nE5Nyyx"
    },
    "xujiahao": {
        "name": "烟(许佳豪)",
        "artistId": "2DXogZyZTpItlsIGCG6Qpt"
    },
    "yuanyawei": {
        "name": "袁娅维",  # 2012年中国好声音第一季刘欢组四强
        "artistId": "70paW48PtCtUjtndElrjrL"
    },
    "kelly_yu": {
        "name": "于文文",
        "artistId": "5R56NYbLCC2HpOwlYBnmeN"
    },
    "yinqueshiting": {
        "name": "音阙诗听",
        "artistId": "6JZIgN9gEgNSS8lY5pmwbx"
    },
    "liushuang": {
        "name": "柳爽",
        "artistId": "7vzmSiBMYT0aSIjHFoWbhV"
    },
    "zhanzhanyuluoluo": {
        "name": "展展与罗罗",
        "artistId": "7jqlVGxCx6cj6o9FPmO98s"
    },
    "daiquan": {
        "name": "戴荃",
        "artistId": "20vLqxWyyRuMaNpMsgZOI6"
    },
    "rensuxi": {
        "name": "任素汐",
        "artistId": "16rAFXQVz2WBpTH9uc1LA8"
    },
    "fangdongdemao": {
        "name": "房东的猫",
        "artistId": "6oxtUCWftDouZzeso3oXcF"
    },
    "madi": {
        "name": "马頔",
        "artistId": "6INLZbPHXGj6ERrjFGPYD6"
    },
    "maliang": {
        "name": "马良",
        "artistId": "713WTosB61RDO5KwQtNKQA"
    },
    "luxianshenyuedui": {
        "name": "鹿先森乐队",
        "artistId": "4SklOYXOJe2H6R1Vz2gc0F"
    },
    "xufei": {
        "name": "许飞",  # 2006年超级女生第三届全国总决赛第6名
        "artistId": "7jQNVznzEejg5gU5B0AmfQ"
    },
    "chenhongyu": {
        "name": "陈鸿宇",
        "artistId": "7ukU2IyqxXp80Jnxf4lzTv"
    },
    "wangerlang-2": {
        "name": "王贰浪2",
        "artistId": "6qXHEV470p1bYHxkTSVrRs"
    },
    "wangerlang": {
        "name": "王贰浪",
        "artistId": "6jNRSV0cd0kL5Tfz6JPxZA"
    },
    "wangheye": {
        "name": "王赫野",
        "artistId": "2sAy0e2cL6jbo0ukxlxWNJ"
    },
    "usa_for_africa": {
        "name": "U.S.A. For Africa",
        "artistId": "7sF6m3PpW6G6m6J2gzzmzM"
    },
    "liujinrui": {
        "name": "刘瑾睿",
        "artistId": "0ySwuPxQeg9GsjWO92RVLF"
    },
    "baisong": {
        "name": "柏松",
        "artistId": "5dGgQ6EQsfOPRiv2V0b846"
    },
    # ---------- Nah
    "gai_zhouyan": {
        "name": "GAI周延",  # 2017年中国有嘻哈第一季并列冠军
        "artistId": "37EUUUGKMLP6KSKrN9q39m"
    }
}

artists = otherArtists | generateArtists
