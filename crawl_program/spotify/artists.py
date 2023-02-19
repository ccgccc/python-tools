# Define artist to crawl
artistToCrawl = "queen"

# === Define artists to generate playlists
# (Search artist on spotfy (e.g. 张学友 on spotify) to get artistId)
# Define generate method: 1 - by number, 2 - by playcount
# For method 1: Define track number to add tracks
# For method 2: Define minimum playcount to add tracks
generateArtists = {
    "queen": {
        "name": "Queen",  # 1973-02-05
        "artistId": "1dfeR4HaWDbWqFHLkxsg1d",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  #
        }
    },
    "jonathan_lee": {
        "name": "李宗盛",  # 1985-03-27
        "artistId": "2TXF68WgfTZlipUvLBsQre",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 25  # 聽見有人叫妳寶貝
        },
        "excludeTracks": {
            # 演唱会串烧
            "3XKYMHHwcQZUiZmojZ2ES5": "別怕我傷心/聽見有人叫你寶貝/愛情少尉/愛如潮水(OT:愛你的餘溫) - Live",
            "1b5VyMuRN2Hzg6WV5RbcmC": "在晴朗的天空下(粵)"  # 真心英雄粤语版
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
    "julie_sue": {
        "name": "苏芮",  # 1983-01-01
        "artistId": "0B2g2ZF6jP0WkaZb33iPhX",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 15
        },
        "excludeTracks": {
            "4FtvRL1kxZAQIxbpfJDIPY": "酒矸倘賣嘸"  # 重复
        }
    },
    "teresa_teng": {
        "name": "邓丽君",  # 1970-01-01
        "artistId": "3ienC90A5I1X3irDyQoqWZ",
        "generateInfo": {
            "generateMethod": 1,
            "number": 25
        },
        "includeTracks": {
            "58atR1rjI1gYtusJheguZU": "路邊野花不要採"
        },
        "excludeTracks": {
            "7BvRirLX1FGRM7Ud03kQoU": "Tsugunai"  # 重复，即 つぐない (偿还)
        }
    },
    # ----- Split
    # --- Crawled
    "camila_cabello": {
        "name": "Camila Cabello",  # 2015-04-14
        "artistId": "4nDoRrQiYLoBzwC5BhVJzF"
    },
    "selena_gomez": {
        "name": "Selena Gomez",  # 2009-01-01
        "artistId": "0C8ZW7ezQVs4URX5aX7Kqx"
    },
    "justin_bieber": {
        "name": "Justin Bieber",  # 2009-01-01
        "artistId": "1uNFoZAHBGtllmzznpCI3s"
    },
    "ed_sheeran": {
        "name": "Ed Sheeran",  # 2009
        "artistId": "6eUKZXaKkcviH0Ku9w2n3V"
    },
    "lady_gaga": {
        "name": "Lady Gaga",  # 2008
        "artistId": "1HY2Jd0NmPuamShAr6KMms"
    },
    "tylor_swift": {
        "name": "Tylor Swift",  # 2006-10-24
        "artistId": "06HL4z0CvFAxyc27GXpf02",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # Cruel Summer
        }
    },
    "rihanna": {
        "name": "Rihanna",  # 2005-01-01
        "artistId": "5pKCCKE2ajJHZ9KAiaK11H"
    },
    "beyonce": {
        "name": "Beyoncé",  # 1998-03-31
        "artistId": "6vWDO969PvNqNYHIOW5v0m"
    },
    "eminem": {
        "name": "Eminem",  # 1996-11-12
        "artistId": "7dGJo4pcD2V6oG8kP0tJRR"
    },
    "snoop_dogg": {
        "name": "Snoop Dogg",  # 1993
        "artistId": "7hJcb9fa4alzcOq3EaNPoG"
    },
    "whitney_houston": {
        "name": "Whitney Houston",  # 1983-04-18
        "artistId": "6XpaIBNiVzIetEPCWDvAFP"
    },
    "david_bowie": {
        "name": "David Bowie",  # 1967-06-01
        "artistId": "0oSGxfWSnnOXhD2fKuz2Gy"
    },
    "the_beatles": {
        "name": "The Beatles",  # 1963-03-22
        "artistId": "3WrFJ7ztbogyGnTHbHJFl2"
    },
    # ** 香港新生代 **
    "mike_tsang": {
        "name": "曾比特",  # 2021-01-08
        "artistId": "33oY0RTyXAMYBM6QSImuo7"
    },
    "terence_lam": {
        "name": "林家谦",  # 2019-01-11
        "artistId": "3tvtGR8HzMHDbkLeZrFiBI"
    },
    "kwan_gor": {
        "name": "吴业坤",  # 2014-04-01
        "artistId": "5vJp6mhsvKyUPZI1bU0c07"
    },
    "gin_lee": {
        "name": "李幸倪",  # 2014-01-01
        "artistId": "0UtXMxHMXhwQUI6G6TFDt1"
    },
    "fred_cheng": {
        "name": "郑俊弘",  # 2013-12-17
        "artistId": "6eUofOqC7jS5aPeTa1a71y"
    },
    "aga": {
        "name": "AGA",  # 2013-01-01
        "artistId": "1opXC6lrFxsiDks53X5d3Q"
    },
    "hubert_wu": {
        "name": "胡鸿钧",  # 2012-07-11
        "artistId": "0OZ5IlVdYIK1Et3nW6aTO5"
    },
    "ruco_chan": {
        "name": "陈展鹏",  # 2012-06-06
        "artistId": "0PlNec0FUQF9KiSX1PiVRs"
    },
    "mag_lam": {
        "name": "林欣彤",  # 2011-08-18
        "artistId": "2fTmvcWWFIP66KlIvWlnlL"
    },
    "shiga_lin": {
        "name": "连诗雅",  # 2010-11-19
        "artistId": "5Uw3hCC51pNjdsD2MOs72K"
    },
    "jinny_ng": {
        "name": "吴若希",  # 2010-11-09
        "artistId": "03OP7wr6EAMFBmDiaRsdbf"
    },
    "phil_lam": {
        "name": "林奕匡",  # 2010-09-26 *
        "artistId": "2pYLo2RugZpdhYRub5nKcV"
    },
    "supper_moment": {
        "name": "Supper Moment",  # 2010-08-06
        "artistId": "29Ukw6Kx8IyOABZFklKpaX"
    },
    "c_allstar": {
        "name": "C AllStar",  # 2010
        "artistId": "0ip5ivJzpy0v4DWVVKxc4D"
    },
    "alfred_hui": {
        "name": "许廷铿",  # 2010 *
        "artistId": "0GCtLaB5rBjoUpQdXogZzj"
    },
    "rubberband": {
        "name": "RubberBand",  # 2008-09-26
        "artistId": "7uzBKhYbCKBs53kDrO4Suc"
    },
    "joyce_cheng": {
        "name": "郑欣宜",  # 2008-06-02
        "artistId": "1y4HuOPsPuo8bBIzk5CXsV"
    },
    "juno_mak": {
        "name": "麦浚龙",  # 2008
        "artistId": "6YlGm6QDrC3TOknYcHjt62"
    },
    "ken_hung": {
        "name": "洪卓立",  # 2007-07-19 *
        "artistId": "0sQMt1Llvcuza8oLKB9bmi"
    },
    "pakho_chau": {
        "name": "周柏豪",  # 2007-07-14 *
        "artistId": "38t0Qk7AJg7YdrXmOC6TH1"
    },
    "jason_chan": {
        "name": "陈柏宇",  # 2007-05-03 *
        "artistId": "1IDuSpntFl2Mutofvrrutc"
    },
    "terence_siufay": {
        "name": "小肥",  # 2007-01-01
        "artistId": "3AemIC066y8n3TetXWkVoE"
    },
    "vincy_chan": {
        "name": "泳儿",  # 2006-07-27
        "artistId": "1ehwpBADazgPy9ypV77FMx"
    },
    "justin_lo": {
        "name": "侧田",  # 2006-03-24
        "artistId": "3lva01D3HtmlEKjuxAZ7bC"
    },
    "kelvin_kwan": {
        "name": "关楚耀",  # 2006-01-01
        "artistId": "7fYTOkMd8M1Xwcl1fB4tjs"
    },
    "khalil_fong": {
        "name": "方大同",  # 2005-11-16
        "artistId": "1YrtUPrWcPfgdl9BaD9nhd"
    },
    "janice_vidal": {
        "name": "卫兰",  # 2005-05-26
        "artistId": "68gYAqni9tSrACmLCp4qoM"
    },
    "fama": {
        "name": "农夫",  # 2005-04-07
        "artistId": "7BcyMcADGhD6WB6XFAJFEa"
    },
    "ivana_wong": {
        "name": "王菀之",  # 2005-01-01
        "artistId": "27WDr8Ky1j0LtgY82Ttk5S"
    },
    "pong_nan": {
        "name": "蓝奕邦",  # 2004-09-17
        "artistId": "6G7bdG4rBz6OQgKudNjoGL"
    },
    "raymond_lam": {
        "name": "林峰",  # 2004-07-19
        "artistId": "4KCnzC71azFAYCKmD1bJOK"
    },
    "endy_chow": {
        "name": "周国贤",  # 2004-03-18
        "artistId": "5r0xeBSRKRJ5Dm63XzTZhE"
    },
    "fiona_sit": {
        "name": "薛凯琪",  # 2004-03-18
        "artistId": "0tqxh7MvZ301BVW4e0p3Sa"
    },
    "eman_lam": {
        "name": "林二汶",  # 2002-12-01
        "artistId": "3SJsybXfmMSrXcwpK56YuU"
    },
    "chet_lam": {
        "name": "林一峰",  # 2002-07-02
        "artistId": "0eE5MIp5hONB0TxIJS5H48"
    },
    "charmaine_fong": {
        "name": "方皓玟",  # 2002-07-01
        "artistId": "1DgBVE3lCnC7Osg9zpAt6N"
    },
    "hins_cheung": {
        "name": "张敬轩",  # 2002-01-01
        "artistId": "2MVfNjocvNrE03cQuxpsWK"
    },
    "alex_fong": {
        "name": "方力申",  # 2001.08.01
        "artistId": "709dAbhS0sezd0SUJImqg4"
    },
    "denise_ho": {
        "name": "何韵诗",  # 2001-07-01
        "artistId": "4yN0M1P08hXwuDi81G6O5U"
    },
    # *** 香港新生代 End ***
    # --- hongkong
    "jackson_wang": {
        "name": "王嘉尔",  # 2014-02-17
        "artistId": "1kfWoWgCugPkyxQP8lkRlY"
    },
    "louis_koo": {
        "name": "古天乐",  # 2000
        "artistId": "4IyiZtwIUAgoijPHAecLUp"
    },
    "joey_yung": {
        "name": "容祖儿",  # 1999-03-05
        "artistId": "2zzKlxMsKTPMsZacZCPRNA"
    },
    "jordan_chan": {
        "name": "陈小春",  # 1996-08-01
        "artistId": "4EefQ1H6Qg9W5Gv7eVLC9U"
    },
    "ronald_cheng": {
        "name": "郑中基",  # 1996-01-01
        "artistId": "66FF9LF0uO3W1zxEN0m8uN"
    },
    "gigi_leung": {
        "name": "梁咏琪",  # 1995-11-01
        "artistId": "1kvvEkC7PQfgfqtCi9YQau"
    },
    "ekin_cheng": {
        "name": "郑伊健",  # 1992-08-14
        "artistId": "2DNe29u3NiB7u8k8RS5IuD"
    },
    "david_lui": {
        "name": "吕方",  # 1991-11-01
        "artistId": "6CexlJ1wj79N50NMxRBfUa"
    },
    "jackie_chan": {
        "name": "成龙",  # 1991-01-01
        "artistId": "0wVKXWiOMLfqmFCdCPR7Ar"
    },
    "anthony_wong": {
        "name": "黄耀明",  # 1990-01-01
        "artistId": "16J0pDSrYEctKiVYogq2aI"
    },
    "tat_ming_pair": {
        "name": "达明一派",  # 1986-03-27
        "artistId": "2cvtzIo0OSIAkyr7LisIT6"
    },
    "zhangmingmin": {
        "name": "张明敏",  # 1982-12-11
        "artistId": "6z9Fa9tGIj8AiQ6Kn75b3T"
    },
    "lowell_lo": {
        "name": "卢冠廷",  # 1981-01-01
        "artistId": "0PBs3xfhn0PA6irWFrknJ4"
    },
    "michael_kwan": {
        "name": "关正杰",  # 1979-01-01
        "artistId": "6t12u8eGw0eN6AcMtUMkoG"
    },
    "adam_cheng": {
        "name": "郑少秋",  # 1978-01-01
        "artistId": "4f25nycVenTs04Y7lYuS8U"
    },
    "kenny_bee": {
        "name": "钟镇涛",  # 1976-01-01
        "artistId": "1SnFcgaLa1l0bV8ZOEL3Cg"
    },
    "paula_tsui": {
        "name": "徐小凤",  # 1973-12-19
        "artistId": "4285Dv04KV2gVNx8hCG1Aw"
    },
    "roman_tam": {
        "name": "罗文",  # 1971-05-15
        "artistId": "7Kb6okLNmQmENkjdGA2HgO"
    },
    "jenny_tseng": {
        "name": "甄妮",  # 1970-01-01
        "artistId": "6U7CvLXWSS3t3a9iwY52oA"
    },
    # --- mainland
    "shanyichun": {
        "name": "单依纯",  # 2020-09-04
        "artistId": "7rXM91kSsqGzvYANukdQJD"
    },
    "arong": {
        "name": "阿冗",  # 2019-11-06
        "artistId": "3dTgjg7lzUGiD3NwcGCK1n"
    },
    "ayouyou": {
        "name": "阿悠悠",  # 2019-04-18
        "artistId": "52aRYqJrRSmGfJbWwvAOYs"
    },
    "azora_chin": {
        "name": "尤长靖",  # 2018-07-19
        "artistId": "40e9OFBP4xVmpLccI1FYiI"
    },
    "tangchao": {
        "name": "汤潮",  # 2018-02-05
        "artistId": "6Cw3GkCetFiwFV9blLfvfD"
    },
    "gaojin": {
        "name": "高进",  # 2018-01-05
        "artistId": "0GjIwBSdhGj3vLVoCunPzm"
    },
    "jiaomaiqi": {
        "name": "焦迈奇",  # 2017-12-20
        "artistId": "1FyPWrq6lU8yPFM7IXj6oH"
    },
    "maobuyi": {
        "name": "毛不易",  # 2017-09-01
        "artistId": "6gvSKE72vF6N20LfBqrDmm"
    },
    "tfboys": {
        "name": "TFBOYS",  # 2016-08-26
        "artistId": "1dywcVTpMrP7VmQUhngSce"
    },
    "liangbo": {
        "name": "梁博",  # 2016-08-06
        "artistId": "5exi2vO8Knathaq5p8Okre"
    },
    "jin_wenqi": {
        "name": "金玟岐",  # 2015-12-09
        "artistId": "4ieCG6ylz8VnMkGMkiWpbd"
    },
    "benxi": {
        "name": "本兮",  # 2015-08-01
        "artistId": "41WH5ZIopoJCdOhkYDmblM"
    },
    "zhoushen": {
        "name": "周深",  # 2014-04-23
        "artistId": "0BezPR1Hn38i8qShQKunSD"
    },
    "xiaojian": {
        "name": "小贱",  # 2014
        "artistId": "3UOBqLsumc6pz9nc2nL4A9"
    },
    "jike_junyi": {
        "name": "吉克隽逸",  # 2013-12-06
        "artistId": "2dIGGnfI63aDJNR6eL50AZ"
    },
    "ada_zhuang": {
        "name": "庄心妍",  # 2013
        "artistId": "42l9R70OWvywz9JN9DCVOM"
    },
    "liuruiqi": {
        "name": "刘瑞琦",  # 2013
        "artistId": "4mpD7eRd38R1tUcheDWrxQ"
    },
    "dazhuang": {
        "name": "大壮",  # 2012-07-02
        "artistId": "0JvihWUI0PyC4sEJGVwrAg"
    },
    "wanting": {
        "name": "曲婉婷",  # 2012-01-01
        "artistId": "2OC4lXfGEKZkbmRCcf2vTq"
    },
    "wowkie_da": {
        "name": "大张伟",  # 2012
        "artistId": "3RIgMUtdfRx98Lm5bXM3GD"
    },
    "houxian": {
        "name": "后弦",  # 2011-07-29
        "artistId": "46leOMfvDoDoujesrjjbeG"
    },
    "aqiao": {
        "name": "阿悄",  # 2010-06-01
        "artistId": "09uuM5dpTq7YBFZvbpn1qd"
    },
    "jiangyangzhuoma": {
        "name": "降央卓玛",  # 2010-04-07
        "artistId": "37prLIatkel3p0BKETTK62"
    },
    "liuxijun": {
        "name": "刘惜君",  # 2010-01-01
        "artistId": "46OJt1hMEeXtny1BebzNMF"
    },
    "xuliang": {
        "name": "徐良",  # 2010-01-01
        "artistId": "6sqXIwIIs1LWj6OQuBVPpR"
    },
    "silence_wang": {
        "name": "汪苏泷",  # 2010-01-01
        "artistId": "0PdNEiQ3MsJGCEgE13Tz60"
    },
    "li_yugang": {
        "name": "李玉刚",  # 2010.01.01
        "artistId": "3PI2UCRk6X5prLnFr05QQK"
    },
    "bibi_zhou": {
        "name": "周笔畅",  # 2009
        "artistId": "3WHsy1Rq4vPEdRyo9P3a48"
    },
    "top_combine": {
        "name": "至上励合",  # 2008-10-26
        "artistId": "1I07lqAx39utkxt5zkC475"
    },
    "escape_plan": {
        "name": "逃跑计划",  # 2008-05-01
        "artistId": "3eJTjQEMzEeoS4n6aJXhKM"
    },
    "yisa_yu": {
        "name": "郁可唯",  # 2008-01-01
        "artistId": "75CM5fojYdKYD0xYSFh22Z"
    },
    "della": {
        "name": "丁当",  # 2007-07-03
        "artistId": "1EUq1MC4vfYYxcVK9aJnXf"
    },
    "huangling": {
        "name": "黄龄",  # 2007.5.31
        "artistId": "6OAQlHABRwPJYVTkaSmiJ9"
    },
    "kuaizixiongdi": {
        "name": "筷子兄弟",  # 2007-05-31
        "artistId": "6R2AgShAYIEOkulvSSant5"
    },
    "lingdianyuedui": {
        "name": "零点乐队",  # 2007-05-29
        "artistId": "7sG313wn1AOWrsAfLEx3pM"
    },
    "daodang": {
        "name": "刀郎",  # 2007-05-18
        "artistId": "0EUH8U3HHClbdLO3m46EOv"
    },
    "chris_lee": {
        "name": "李宇春",  # 2006-09-15
        "artistId": "02VPWD8AZ7qSuug0dM4Hk1"
    },
    "jane_zhang": {
        "name": "张靓颖",  # 2006-01-01
        "artistId": "7qJmFr579WC8MMGj4PiWdu"
    },
    "huge": {
        "name": "胡歌",  # 2006
        "artistId": "04T9gfyccsmxG79OSJp5r1"
    },
    "xianzi": {
        "name": "弦子",  # 2005-07-08
        "artistId": "2CBuGdj5Nmgx1VfrgLnGoJ"
    },
    "jinsha": {
        "name": "金莎",  # 2005-04-23
        "artistId": "0wK3rMwogVowmeXArZN29T"
    },
    "zhangjie": {  # 待定
        "name": "张杰",  # 2005.03.15
        "artistId": "75udD9hen8NeHTe92rUNLa"
    },
    "zhengyuan": {
        "name": "郑源",  # 2005-01-01
        "artistId": "0zFibeNnPW3pxo2nUqCu0w"
    },
    "sa_dingding": {
        "name": "萨顶顶",  # 2004.12.01
        "artistId": "5HCoNna7Jrw9YGVvo4lg1a"
    },
    "shabaoliang": {
        "name": "沙宝亮",  # 2003-05-01
        "artistId": "4ef3Gqwh0lqBGVWcmNIThQ"
    },
    "hanhong": {
        "name": "韩红",  # 2002-11-01
        "artistId": "1kLqxXjyc7OwDJopftAH86"
    },
    "yangkun": {
        "name": "杨坤",  # 2002.05.01
        "artistId": "7Dc62n8zZBrx6SsNDfmF9O"
    },
    "tiger_hu": {
        "name": "胡彦斌",  # 2002
        "artistId": "3PpIzdLny8HwTnKp9joXdj"
    },
    "tongyangyuedui": {
        "name": "痛仰乐队",  # 2001-01-01
        "artistId": "1KkPfPiuNxdjuGhwIb6hBC"
    },
    "yu_quan": {
        "name": "羽泉",  # 1999-11-16
        "artistId": "4jkXpEWzunLc5WnHSEiDMf"
    },
    "huaeryuedui": {
        "name": "花儿乐队",  # 1999-11-11
        "artistId": "1ipRvm81MI5PnM6mmBppmy"
    },
    "tenggeer": {
        "name": "腾格尔",  # 1999-06-16
        "artistId": "5U99oKyYA9vz0hEmEU1NjN"
    },
    "shunza": {
        "name": "顺子",  # 1997-11-11
        "artistId": "2zXcyd0DsDOxZc1nSGepMb"
    },
    "lengmo": {
        "name": "冷漠",  # 1997-03-01
        "artistId": "1e1i9fonmXyUGtJngqFiby"
    },
    "hanlei": {
        "name": "韩磊",  # 1997-03-01
        "artistId": "7puBL0AvJjalTgoPePIigh"
    },
    "tianzhen": {
        "name": "田震",  # 1995-09-30
        "artistId": "09mk8X1qeA7JlMHMSmqw7c"
    },
    "naying": {
        "name": "那英",  # 1994-01-01
        "artistId": "35ig3ZjuqVyGeovLsj4xNm"
    },
    "dou_wei": {
        "name": "窦唯",  # 1993-06-18
        "artistId": "7xMGjlJ3a6wH3LrwiWEJvx"
    },
    "heibaoyuedui": {
        "name": "黑豹乐队",  # 1992-12-22
        "artistId": "0zj66XhQP4EPkat7XkBYL0"
    },
    "tangchaoyuedui": {
        "name": "唐朝",  # 1992-12-11
        "artistId": "3gAbcvLOMgHwAgNPN2bo8N"
    },
    "sunnan": {
        "name": "孙楠",  # 1990.01.01
        "artistId": "0CxNT2689kPeISWh2eLMZO"
    },
    "maoamin": {
        "name": "毛阿敏",  # 1989-09-19
        "artistId": "5h4JXGFKmlIEInbDcHAHw3"
    },
    "cuijian": {
        "name": "崔健",  # 1989-02-01
        "artistId": "1YwBQZlsK015NpwaF8gpd9"
    },
    "liuhuan": {
        "name": "刘欢",  # 1986.01.01
        "artistId": "3K4aEHMBQbW2hJVAhooLGy"
    },
    # --- taiwan
    "vicky_chen": {
        "name": "陈忻玥",  # 2017-12-19
        "artistId": "01u3qI3xMGFvktXyRSMGRZ"
    },
    "eve_ai": {
        "name": "艾怡良",  # 2012-10-24
        "artistId": "6eLpNMX3ZygSrUuxAlIWIx"
    },
    "huxia": {
        "name": "胡夏",  # 2010-12-14
        "artistId": "3iRqbMhzyOyoCkmmMRxLWR"
    },
    "nickthereal": {
        "name": "周汤豪",  # 2010-07-16
        "artistId": "1fHw35wWkpOw05sswFSl70"
    },
    "liuzhe": {
        "name": "六哲",  # 2010.06.21
        "artistId": "1iVhYU0gUs9N5kDs22AtFV"
    },
    "cindy_yen": {
        "name": "袁咏琳",  # 2009-10-30
        "artistId": "3IXhSUXNXO7Z6GnYufgpKR"
    },
    "zongguanxian": {
        "name": "纵贯线",  # 2009
        "artistId": "1H7vlkyLUbFo5sFhvhBh8K"
    },
    "xuyuteng": {
        "name": "徐誉滕",  # 2008-10-15
        "artistId": "1vVpQbgOTGxegFcKGCak9O"
    },
    "william_chan": {
        "name": "陈伟霆",  # 2008-09-05
        "artistId": "0lTHF5hgNUeMetVJEBWwvx"
    },
    "by2": {
        "name": "BY2",  # 2008-07-18
        "artistId": "3DOs7Bsr9x4eJHqv6ViPvR"
    },
    "rachel_liang": {
        "name": "梁文音",  # 2008-01-01
        "artistId": "4rdSHzO4enUlVxdQeHPGTp"
    },
    "wuqingfeng": {
        "name": "吴青峰",  # 2007-12-31
        "artistId": "5a5vu4RzsAHdKN0aYyblZ8"
    },
    "waa_wei": {
        "name": "魏如萱",  # 2007-11-08
        "artistId": "190bkHbFrRvEhcB7Zpuv3y"
    },
    "yoga_lin": {
        "name": "林宥嘉",  # 2007-10-05
        "artistId": "1GPoTgvXd5OqZMF1akOsV2"
    },
    "aska_yang": {
        "name": "杨宗纬",  # 2007-10-05
        "artistId": "2SOrfXWlb17EoCqupfGX4u"
    },
    "fahrenheit": {
        "name": "飞轮海",  # 2006-06-01
        "artistId": "37Ge9MTQaJqJknImNwYhWF"
    },
    "yangpeian": {
        "name": "杨培安",  # 2006-01-01
        "artistId": "5zxmrXIwrLuSfIJM3Dz6y1"
    },
    "gary_chaw": {
        "name": "曹格",  # 2005-12-30
        "artistId": "1mfzcypCggFwpCJ1gmi8BK"
    },
    "lara_liang": {
        "name": "梁心颐",  # 2005-11-01
        "artistId": "4VgfrD5wuAoN428fBZNSyW"
    },
    "deserts_chang": {
        "name": "张悬",  # 2005-09-30
        "artistId": "7v9Il42LvvTeSfmf1bwfNx"
    },
    "nicky_lee": {
        "name": "李玖哲",  # 2005-04-22
        "artistId": "6DuHQk8gJbyVlhajer8IuF"
    },
    "sodagreen": {
        "name": "苏打绿",  # 2004-05-30
        "artistId": "3WYT2b8pOLsLsqSaoWYr7U"
    },
    "nanquanmama": {
        "name": "南拳妈妈",  # 2004-05-12
        "artistId": "48Smhc0ISwYYRSad1uXSns"
    },
    "mc_jin": {
        "name": "欧阳靖",  # 2004.01.01
        "artistId": "1TwLg1dl8iHh2AZsH88whn"
    },
    "show_luo": {
        "name": "罗志祥",  # 2003-11-21
        "artistId": "33ApZ6LzfimooQNIKqf4jo"
    },
    "xinyuetuan": {
        "name": "信乐团",  # 2003-04-11
        "artistId": "1YfpT6Dl8tJDmYQKWRoxjn"
    },
    "sam_lee": {
        "name": "李圣杰",  # 2002-06-27
        "artistId": "7ya3wFqG9X35S7L7XSrE2i"
    },
    "ricky_hsiao": {
        "name": "萧煌奇",  # 2002-06-27
        "artistId": "0E6oEhZZtQvj811iXQFLrB"
    },
    "fan_yi_chen": {
        "name": "范逸臣",  # 2002-06-04
        "artistId": "2Z7qQ1slMaPjLOCXBqshct"
    },
    "ado": {
        "name": "阿杜",  # 2002-04-03
        "artistId": "24C7uNrWX2Iidb6X63vTGz"
    },
    "will_pan": {
        "name": "潘玮柏",  # 2002-01-01
        "artistId": "7fCFxj1GCRqwFZEP4iJRw0"
    },
    "f4": {
        "name": "F4",  # 2001-08-27
        "artistId": "1JadFMFTjfKAVtOqbrgv0X"
    },
    "mc_hotdog": {
        "name": "MC HotDog",  # 2001-02-16
        "artistId": "4maR8o69pil8CrclOiFVVW"
    },
    "kenji_wu": {
        "name": "吴克群",  # 2000
        "artistId": "1MgybycH8k36NX0Ifzlddb"
    },
    "landy_wen": {
        "name": "温岚",  # 1999-12-15
        "artistId": "3yMtvgD2LCo6Ws4Z08fTFj"
    },
    "dick_and_cowboy": {
        "name": "迪克牛仔",  # 1999-01-01
        "artistId": "0cnqUQJBnf0AeIjyOX2xGF"
    },
    "power_station": {
        "name": "动力火车",  # 1997-10-07
        "artistId": "6zCAdMK7SVxKyGMnAc26Cy"
    },
    "jimmy_lin": {
        "name": "林志颖",  # 1996-12-05
        "artistId": "3ZCIwlsAdItKVQk6V68Ho7"
    },
    "victor_wong": {
        "name": "品冠",  # 1996-10-24
        "artistId": "70ht8hGTKjvbPJ37xVO9cW"
    },
    "valen_hsu": {
        "name": "许茹芸",  # 1995-01-01
        "artistId": "0iW8EYj3iP2gpO5eU2Pvta"
    },
    "michael_wong": {
        "name": "光良",  # 1994-02-07
        "artistId": "26SQFo2qNNGOxh2PUAsTeO"
    },
    "zhangzhenyue": {
        "name": "张震岳",  # 1993-07-01
        "artistId": "6PNEi9i2MxUgRufqYr76Xt"
    },
    "mengtingwei": {
        "name": "孟庭苇",  # 1991-01-01
        "artistId": "2Ovp3J8JzCirwcGAgvK9cQ"
    },
    "huangpinyuan": {
        "name": "黄品源",  # 1990-06-30
        "artistId": "22eZSsFE2fxLnnC9Zga25b"
    },
    "tiger_huang": {
        "name": "黄小琥",  # 1990-06-01
        "artistId": "6KCusBln9NTESgcuI0DlUz"
    },
    "zhengzhihua": {
        "name": "郑智化",  # 1990-03-01
        "artistId": "2DqYjQiVXvk7yFkqpVb5wX"
    },
    "winnie_hsin": {
        "name": "辛晓琪",  # 1990-01-01
        "artistId": "75UZxcclb8ahAZl69xMKLJ"
    },
    "ejun_lee": {
        "name": "李翊君",  # 1989-01-01
        "artistId": "39YbP9PakVwqfXFtRdn5vI"
    },
    "xiaohudui": {
        "name": "小虎队",  # 1989-04-01
        "artistId": "3mEfTOV1940pc4FCYYwNIQ"
    },
    "jeremy_chang": {
        "name": "张洪量",  # 1989-01-01
        "artistId": "2WhSJLdTSsN3cqiuLe44Cc"
    },
    "jeff_chang": {
        "name": "张信哲",  # 1988-09-22
        "artistId": "2dw80Uni5l7wd9zZFn7Ltu"
    },
    "zhao_chuan": {
        "name": "赵传",  # 1988-08-04
        "artistId": "2deH7GtKAGqNAYCtsruIQ8"
    },
    "samuel_tai": {
        "name": "邰正宵",  # 1988
        "artistId": "4t3kmZV59tEONpRUZmXjpP"
    },
    "dave_wong": {
        "name": "王杰",  # 1987-12-19
        "artistId": "5XMnJOQbE6OuOvcV8fn3Wg"
    },
    "harlem_yu": {
        "name": "庾澄庆",  # 1986-12-12
        "artistId": "6VbRanWSU3pdDhJnhSfGmY"
    },
    "eric_moo": {
        "name": "巫启贤",  # 1986.12.01
        "artistId": "7y52WmTUJZQU7m83zYfoV2"
    },
    "sky_wu": {
        "name": "伍思凯",  # 1986-09-01
        "artistId": "7pAOT0acNprtWarxvyM5LZ"
    },
    "steve_chou": {
        "name": "周传雄",  # 1986-04-01
        "artistId": "1Qneon4tYZ7srVOU91bTsO"
    },
    "chyi_chin": {
        "name": "齐秦",  # 1985-12-15
        "artistId": "4VhiuMC32Qj7pVW3e6Nlms"
    },
    "angus_tung": {
        "name": "童安格",  # 1985-05-13
        "artistId": "3TAeauNOPNU1TP7V3nHjKY"
    },
    "zhangqingfang": {
        "name": "张清芳",  # 1985
        "artistId": "1Op5w4ztYgqOsN8KydGEfp"
    },
    "chiang_yu-heng": {
        "name": "姜育恒",  # 1984
        "artistId": "0Nb4cyosZVQQ5x3QxZkVJL"
    },
    "coco_lee": {
        "name": "李玟",  # 1982
        "artistId": "3ioHf138TiMxYRCWmC8yJX"
    },
    "deanie_ip": {
        "name": "叶德娴",  # 1981-07-10
        "artistId": "4fgSPILePGaLs90nNtal3X"
    },
    "chyi_yu": {
        "name": "齐豫",  # 1979-01-01
        "artistId": "5E94Yc9O9D4N3oTr4SzJLx"
    },
    "feiyuqing": {
        "name": "费玉清",  # 1971-01-01
        "artistId": "6aSJ9LaNaHOKiPchLDYGYl"
    },
    "tsai_chin": {
        "name": "蔡琴",  # 1970-02-01
        "artistId": "0hXEo26JJ0u5lD763cTvRW"
    },
    # ==== 民谣
    "zuoxiaozuzhou": {
        "name": "左小祖咒",  # 1998.10.31
        "artistId": "4vxioc97hgfD8zIEbfFBZP"
    },
    "zhangruoshui": {
        "name": "张若水",  # 2017.6.05
        "artistId": "1e1SBWjGspT4KuuDZAHPcI"
    },
    "haiweiba": {
        "name": "海尾巴",  # 2021.08.30
        "artistId": "6MBqbSKEMSX8hYj2GmBt1t"
    },
    "ln_party": {
        "name": "昨夜派对",  # 2019.09.03
        "artistId": "59MFqh1jNapkIS6bqoTjIX"
    },
    "xiaoliu": {
        "name": "小六",  # 2018.12.04
        "artistId": "2en090WOuRJMvwgOODDzuR"
    },
    "liulimin": {
        "name": "刘莉旻",  # 2017.02.15
        "artistId": "26BDquR2kESolItPDlDXx7"
    },
    "xujun": {
        "name": "许钧",  # 2016.08.26
        "artistId": "3kU8TgZ3WouCr0GDkYnPbN"
    },
    "lujingzhou": {
        "name": "鹿京周",  # 2016-06-15
        "artistId": "5N9jkiZ8FolT1fZU7A7UgI"
    },
    "zhuangdafei": {
        "name": "庄达菲",  # 2016.5.24
        "artistId": "6FAEeyf2nMghNBoFFE9DQV"
    },
    "fengzi": {
        "name": "风子",  # 2014.11.17
        "artistId": "22yTMqlBXEbAcL3STX5ey2"
    },
    "liushuang": {
        "name": "柳爽",  # 2014.02.05
        "artistId": "7vzmSiBMYT0aSIjHFoWbhV"
    },
    "haomeimei": {
        "name": "好妹妹",  # 2012.07.05
        "artistId": "55WwHAHZZasWq8QM0LF5JR"
    },
    # ----- Collection :
    "maliang": {
        "name": "马良",  # 2018.08.14
        "artistId": "713WTosB61RDO5KwQtNKQA"
    },
    "chenhongyu": {
        "name": "陈鸿宇",  # 2016.03.01
        "artistId": "7ukU2IyqxXp80Jnxf4lzTv"
    },
    "madi": {
        "name": "马頔",  # 2013.07.10
        "artistId": "6INLZbPHXGj6ERrjFGPYD6"
    },
    "zhaolei": {
        "name": "赵雷",  # 2011.08.07
        "artistId": "2KwZ9xnULczo0Z7Y7Bp57R"
    },
    "zhaolei-2": {
        "name": "赵雷2",
        "artistId": "7EP8l31VxgD0MAOwh7uez5"
    },
    # ----- Collection :
    "xiechunhua": {
        "name": "谢春花",  # 2016.06.21
        "artistId": "0gYt4XG9A0hyZW7rt745ZY"
    },
    "chenli": {  # **
        "name": "陈粒",  # 2015.02.02
        "artistId": "3SyC3U06X0DjdWd2Jf6V8Q"
    },
    "fangdongdemao": {
        "name": "房东的猫",  # 2015.01.01
        "artistId": "6oxtUCWftDouZzeso3oXcF"
    },
    "huazhou": {
        "name": "花粥",  # 2012.03.03
        "artistId": "148sD27V3Nr0XFl3TZNwmw"
    },
    # ----- Collection :
    "floruit_show": {
        "name": "福禄寿",  # 2018.09.02
        "artistId": "08R79pzvOjaPaU3YOGFspZ"
    },
    "luxianshenyuedui": {
        "name": "鹿先森乐队",  # 2016.11.09
        "artistId": "4SklOYXOJe2H6R1Vz2gc0F"
    },
    "yanbaeryuedui": {
        "name": "烟把儿",  # 2014.06.12
        "artistId": "6CivYgdvK9LYT1gj8Jd9ev"
    },
    "diuhuocheyuedui": {
        "name": "丢火车",  # 2008.06.23
        "artistId": "32LfBpNksY6Hegjif5kyVN"
    },
    "wutiaoren": {
        "name": "五条人",  # 2008.09.25
        "artistId": "6NQwuxgsebzIzixLkAHDCT"
    },
    "yehaiziyuedui": {
        "name": "野孩子",  # 2000.08.01
        "artistId": "2VEgQum6bFrsImZgqxxg1L"
    },
    # ----- Collection :
    "erbai": {
        "name": "贰佰",  # 2014.03.25
        "artistId": "1uLtjg16pURFbIEsdp1XWz"
    },
    "haoyun": {
        "name": "郝云",  # 2008.03.05
        "artistId": "7rHYKc9hKD1bCHiuKv2R09"
    },
    # ----- Collection :
    "songdongye": {
        "name": "宋冬野",  # 2013.08.26
        "artistId": "5aJFmaCc09jEz9ghzppUxo"
    },
    "yaoshisan": {
        "name": "尧十三",  # 2008.01.02
        "artistId": "017rAXpcsnXpHaPKdKbbsJ"
    },
    "lizhi": {
        "name": "李志",  # 2005
        "artistId": "1fqb04dI9vaEcGDbIVrcib"
    },
    # ----- Collection :
    "valley_children": {
        "name": "小娟&山谷里的居民",  # 2007.02.06
        "artistId": "5kggU4ADmSLyUtrnEMMB45"
    },
    "zhouyunpeng": {
        "name": "周云蓬",  # 2004.10.01
        "artistId": "0dmiv2QPPnG4JlJ05QH6nh"
    },
    # ----- Collection :
    "mafei": {
        "name": "马飞",  # 2014.04.24
        "artistId": "5mkR7uUsJM0hKUmIx4lpqr"
    },
    "matiao": {
        "name": "马条",  # 2009.02.11
        "artistId": "1ng1KwfjSjnRo44TE8ovtL"
    },
    "zhonglifeng": {
        "name": "钟立风",  # 2006.03.25
        "artistId": "1YOY2N3DvznXjloTYGRF6E"
    },
    # ----- Collection :
    "xiaohe": {
        "name": "小河",  # 2002.12.01
        "artistId": "3HQtVlagT1RApOFulrNoJ6"
    },
    "xiaohe-2": {
        "name": "小河与寻谣计划",
        "artistId": "2EQaYTsagYgRssoLjg7jc9"
    },
    "zhangweiwei": {
        "name": "张玮玮",  # 2008.8.11
        "artistId": "4xeb2oTygsZaLfPNFpowi9"
    },
    "wanxiaoli": {
        "name": "万晓利",  # 2002.12.01
        "artistId": "1T2LQiNaPlo5Ke7XMQq39D"
    },
    "wanxiaoli-2": {
        "name": "万晓利2",
        "artistId": "5q8TJt4PBR0eXaRFcXUsMm"
    },
    # ----- Collection :
    "shuimunianhua": {
        "name": "水木年华",  # 2001.10.01
        "artistId": "1jebNwQMcbQxpbzlW9j7Gu",
        "generateInfo": {
            "generateMethod": 1,
            "number": 5
        }
    },
    "shuimunianhua-2": {
        "name": "水木年华2",
        "artistId": "59oZhkDlvOwLrOOQtlzG5o"
    },
    "yepei": {
        "name": "叶蓓",  # 1999.01.01
        "artistId": "0m0rriPCYLgXXb3D8hHYFp",
        "generateInfo": {
            "generateMethod": 1,
            "number": 5
        }
    },
    "yepei-2": {
        "name": "叶蓓2",
        "artistId": "13UktfkM0Z8TgbemrxsSzv"
    },
    "laolang": {
        "name": "老狼",  # 1995.05.01
        "artistId": "1piwhsT7JM9pBzmLcLCg8v",
        "generateInfo": {
            "generateMethod": 1,
            "number": 10
        }
    },
    "laolang-2": {
        "name": "老狼2",
        "artistId": "0xNZutIrvMMbw2u9ww3oMD"
    },
    # === Candidates
    "kary_ng": {
        "name": "吴雨霏",  # 2003-01-01
        "artistId": "3B9ZmIcte26paTCaI1PFKE",
        "generateInfo": {
            "generateMethod": 1,
            "number": 15  # 雞蛋愛石頭，Missing: 生生世世爱
        }
    },
    "sammi_cheng": {
        "name": "郑秀文",  # 1986-11-26
        "artistId": "3XCnp5UV5wnNw49Xuka9qH",
        "generateInfo": {
            "generateMethod": 1,
            "number": 30  # maybe 20
        }
    },
    # ---
    # ---
    "lala_hsu": {
        "name": "徐佳莹",  # 2009-05-29
        "artistId": "3dI4Io8XE33J2o04ZwjR0Y",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 大雨將至
        }
    },
    "a_lin": {
        "name": "黄丽玲",  # 2006-02-10
        "artistId": "28gf2piFx6cAKOMIwcky5a"
    },
    "ella_chen": {
        "name": "陈嘉桦",  # 2004
        "artistId": "1DNci4XjJlglg629j3yO5n"
    },
    "hebe_tien": {
        "name": "田馥甄",  # 2005-09-28
        "artistId": "14bJhryXGk6H6qlGzwj3W5",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 一一
        }
    },
    "selina": {
        "name": "任家萱",  # 2004
        "artistId": "322fcjb9quEAxAXtmWyNeJ"
    },
    "she": {
        "name": "S.H.E",  # 2001-09-11
        "artistId": "2lWShxOL8iTlI0pmtVKvEh",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 說你愛我
        }
    },
    "christine_fan": {
        "name": "范玮琪",  # 2001-08-01
        "artistId": "1q7sCl0vg0EcaFdRz0XDGg"
    },
    "genie_chuo": {
        "name": "卓文萱",  # 2001-07-26
        "artistId": "5XHBjJm3bCgQCjpnInCxfT"
    },
    "where_chou": {
        "name": "周蕙",  # 2000-05-01
        "artistId": "0T1grpeZ4qvXm7ALeRPKno"
    },
    "penny_tai": {
        "name": "戴佩妮",  # 2000
        "artistId": "0qmPs7q4bykvrS8NMZk7ud"
    },
    "cheer_chen": {
        "name": "陈绮贞",  # 1998-07-14
        "artistId": "4m0xrEWYU0yCUFMaga015T",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 一一
        }
    },
    "yuki_hsu": {
        "name": "徐怀钰",  # 1998-01-16
        "artistId": "06w51RzkHkpkp2x09REY7v"
    },
    "linzhixuan": {
        "name": "林志炫",  # 1996
        "artistId": "6O9BAkGBRRzHUDrWqdT68r"
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
    # === Candidates for collections
    "sarah_chen": {
        "name": "陈淑桦",  # 1971-01-01
        "artistId": "19tf1og71pOYoYOdqyozs2",
        "generateInfo": {
            "generateMethod": 1,
            "number": 7  # 你走你的路
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
    "richie_jen": {
        "name": "任贤齐",  # 1990-01-01
        "artistId": "0zjNCSqeDIxn63crtDx7G2",
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 花好月圓夜 - 廣東版
        }
    },
    "eric_chou": {
        "name": "周兴哲",  # 2014-08-01
        "artistId": "5fEQLwq1BWWQNR8GzhOIvi",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 5  # 永不失聯的愛
        }
    },
    # ---
    # ---
    "grasshopper": {
        "name": "草蜢",  # 1988-02-26
        "artistId": "5IxPdROZmnCyD6TBuSJMYE",
        "generateInfo": {
            "generateMethod": 1,
            "number": 7  # 半點心
        }
    },
    "kelly_chen": {
        "name": "陈慧琳",  # 1990-01-01
        "artistId": "7KyaSSJ8uTv7Unev4z2Qc7",
        "generateInfo": {
            "generateMethod": 1,
            "number": 6  # 誰願放手
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
    "miriam_yeung": {
        "name": "杨千嬅",  # 1998
        "artistId": "1rxk3vAYWeiBD2Q6FCezcl",
        "generateInfo": {
            "generateMethod": 1,
            "number": 9  # 飛女正傳
        }
    },
    "candy_lo": {
        "name": "卢巧音",  # 1998
        "artistId": "51ZbCFgOspWvhBjd1DUYEV",
        "generateInfo": {
            "generateMethod": 1,
            "number": 7  # 進退
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
    "charlene_choi": {
        "name": "蔡卓妍",  # 2003
        "artistId": "6wBoKKHhGDrxVtp6XMFpIP",
        "generateInfo": {
            "generateMethod": 1,
            "number": 5  # 明明
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
    # == Collections
    # ----- Collection : 宝丽金四小花
    "karen_tong": {
        "name": "汤宝如",  # 1992.11.03
        "artistId": "6sXdLBqJ6oMyEWJ4NclB7N"
    },
    "vivian_lai": {
        "name": "黎瑞恩",  # 1991.11.15
        "artistId": "1c18L1dF6HDTrAqYt4qMlI"
    },
    "linda_wong": {
        "name": "王馨平",  # 1991.11.15
        "artistId": "4IXXzNbCXjsSLhUOkLAKWB"
    },
    "winnie_lau": {
        "name": "刘小慧",  # 1991.10.01
        "artistId": "0mj5ojsCPzMpVMG5v11Kp1"
    },
    # ----- Collection : 四大天王
    "aaron_kwok": {
        "name": "郭富城",  # 1990.09.25
        "artistId": "3lbgPpyP2yep0sqwWTgasT"
    },
    "leon_lai": {
        "name": "黎明",  # 1990.07.06
        "artistId": "0ubIxkefJsoYY8JXc2HJoa"
    },
    # ----- Collection 5: Big Four
    "big_four": {
        "name": "Big Four",  # 2010
        "artistId": "5aV8N1m8QyReq34R3qeUx0",
        "generateInfo": {
            "generateMethod": 1,
            "number": 4  # Big Four
        }
    },
    "dicky_cheung": {
        "name": "张卫健",  # 1992.08.01
        "artistId": "05U40G1dajZMe9KdTG8LTo",
        "mustMainArtist": True,
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 把酒狂歌
        }
    },
    "dicky_cheung-2": {
        "name": "张卫健2",
        "artistId": "3de8fL3wVnfUEtOlGIoFy5",
        "mustMainArtist": True
    },
    "edmond_leung": {
        "name": "梁汉文",  # 1991.01.18
        "artistId": "1THfyLd3iyJYJ6X2U36K0y",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 4  # 纏綿遊戲
        }
    },
    "william_so": {
        "name": "苏永康",  # 1989.09.01
        "artistId": "2oK5cSlJAH5s2Kx5e1zcvh",
        "generateInfo": {
            "generateMethod": 1,
            "number": 14  # 愛一個人好難
        }
    },
    "andy_hui": {
        "name": "许志安",  # 1988.05.05
        "artistId": "1q8BvOdpOtapWOIgO26sOn",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 愛妳
        }
    },
    # ----- Collection 4: 天后替补席/次天后
    "cass_phang": {
        "name": "彭羚",  # 1990-12-01
        "artistId": "0RkQt8LMVrxCjQb9BxpBfF",
        "generateInfo": {
            "generateMethod": 1,
            "number": 7
        }
    },
    "shirley_kwan": {
        "name": "关淑怡",  # 1989-01-01
        "artistId": "14hV8HTKYMZ5nzeaLdLp63",
        "generateInfo": {
            "generateMethod": 1,
            "number": 4
        },
        "includeTracks": {
            "3Uv5gs1WK4J0OmTXsD5qxV": "深夜港灣"
        }
    },
    "cally_kwong": {
        "name": "邝美云",  # 1985-01-01
        "artistId": "0Dx75BcGd0qLi7y1kqRlad",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 2
        },
        "includeTracks": {
            "0CaFwm8pjAwd6UVp226sZQ": "寂寞的風"
        }
    },
    # ----- Collection 3: 四大女天王/四大天后
    "vivian_chow": {
        "name": "周慧敏",  # 1988
        "artistId": "4bzVQLX2gMBQVMINdAGElJ",
        # "filterAlbums": False,
        "generateInfo": {
            "generateMethod": 1,
            "number": 9  # 自作多情
        }
    },
    "priscilla_chan": {
        "name": "陈慧娴",  # 1984-01-01
        "artistId": "5SLOTZhruJRRGgIRtTSPc5",
        # "filterAlbums": False,
        "generateInfo": {
            "generateMethod": 1,
            "number": 6  # 人生何處不相逢
        }
    },
    "sandy_lam": {
        "name": "林忆莲",  # 1985
        "artistId": "3K2hOAx9MPhduvDf2qguro",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 不必在乎我是誰
        }
    },
    "sally_yeh": {
        "name": "叶蒨文",  # 1983-06-30
        "artistId": "7Bx0SBZoIX73eywmBcdqFb",
        # "filterAlbums": False,
        "generateInfo": {
            "generateMethod": 1,
            "number": 7  # 曾經心痛
        }
    },
    # ----- Collection 2: 粤语前辈
    "george_lam": {
        "name": "林子祥",  # 1976.01.01
        "artistId": "7rxRHujzUzobMEbtoE297s",
        "filterAlbums": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 15  # 祝福你
        }
    },
    "alan_tam": {
        "name": "谭咏麟",  # 1979.2.20, 1973 温拿
        "artistId": "5vWJrDpmd5vrDpdmgxqC5u",
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 講不出再見
        }
    },
    "sam_hui": {
        "name": "许冠杰",  # 1971.12.01
        "artistId": "1SglpJrPltamdJLLwInIL7",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 10  # 梨渦淺笑
        }
    },
    # ----- Collection 1: 音乐诗人
    "zhengjun": {
        "name": "郑钧",  # 1994-06-01
        "artistId": "5nbhd53CLcjfp7U8NDDzHw",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 4  # 赤裸裸
        }
    },
    "lijian": {
        "name": "李健",  # 2003-09-01
        "artistId": "47FbECPoJxk1TjHVZPzVzG",
        "generateInfo": {
            "generateMethod": 1,
            "number": 1  # 贝加尔湖畔
        }
    },
    "xuwei": {
        "name": "许巍",  # 1995-09-30
        "artistId": "3qObkSIVSfNNDL1vbwL2N2",
        "generateInfo": {
            "generateMethod": 1,
            "number": 5  # 旅行
        }
    },
    "pushu": {
        "name": "朴树",  # 1999-01-01
        "artistId": "6lJ36ifxOD2oUsdMdLRPN4",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 5  # 白樺林
        }
    },
    # == Generated Artists
    "maroon_5": {
        "name": "Maroon 5",
        "artistId": "04gDigrS5kc9YWfZHwBETP",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # Daylight
        },
        "excludeTracks": {
            "6FRLCMO5TUHTexlWo8ym1W": "Girls Like You (feat. Cardi B)",  # 重复
            "2sLS4tVaEoMYrNS67PVz0V": "She Will Be Loved - Acoustic"  # 重复
        }
    },
    "rene_liu": {
        "name": "刘若英",  # 1992-08-07, 奶茶
        "artistId": "6qzfo7jiO4OrhxrvPFPlWX",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
            # "number": 15  # 我很好
        },
        "excludeTracks": {
            "6uuIh4ZiwG3cu2C3XCr0vy": "繼續-給十五歲的自己 - Live"  # 重复，演唱会版本
        }
    },
    "rainie_yang": {
        "name": "杨丞琳",  # 2005-09-09, 可爱教主
        "artistId": "0MEchSWR9pJvw1S5CV3Kuk",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 忘課
        }
    },
    "cyndi_wang": {
        "name": "王心凌",  # 2003-02-01, 流行教主
        "artistId": "3AroL2oDPiAnMpTmIQv3KP",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 心電心
        }
    },
    "angela_chang": {
        "name": "张韶涵",  # 2003-05-01, 电眼教主
        "artistId": "4txug0T3vYc9p20tuhfCUa",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 不害怕，Missing：淋雨一直走、篇章
        },
        "includeTracks": {
            "1N1cLClnWhZRTuZR2TCam6": "篇章"  # 张韶涵2
        },
        "excludeTracks": {
            "02T2R6fMzSZq4pRXtW94rH": "隱形的翅膀"  # 重复，演唱会版本
        }
    },
    "onerepublic": {
        "name": "OneRepublic",  # 2007.03.29
        "artistId": "5Pwc4xIPtQLFEnJriah9YJ",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 15  # Sunshine
        }
    },
    "elva_hsiao": {
        "name": "萧亚轩",  # 1999-11-17
        "artistId": "6yTAPw3o7oDH7lhj34jvbH",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 敢傷
        }
    },
    "fish_leong": {
        "name": "梁静茹",  # 1999-09-17
        "artistId": "3aIDSTKS9yH745GUQBxDcS",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 問
            # "number": 30  # 失憶
        }
    },
    "jolin_tsai": {
        "name": "蔡依林",  # 1999-09-10, 流行教主
        "artistId": "1r9DuPTHiQ7hnRRZ99B8nL",
        "filterTrackByName": True,
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 40  # 你睡醒再看
        }
    },
    "david_tao": {
        "name": "陶喆",  # 1997-12-06
        "artistId": "40tNK2YedBV2jRFAHxpifB",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "imagine_dragons": {
        "name": "Imagine Dragons",
        "artistId": "53XhwfbYqKCa1cC15pYq2q",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "lironghao": {
        "name": "李荣浩",  # 2010.09.09
        "artistId": "0rTP0x4vRFSDbhtqcCqc8K",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 作曲家
        }
    },
    "joker_xue": {
        "name": "薛之谦",  # 2006-06-09
        "artistId": "1cg0bYpP5e2DNG0RgK2CMN",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 怪咖
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
    "leslie_cheung": {
        "name": "张国荣",  # 1978-01-01
        "artistId": "2g0QLUYku8AuPVK2udRV7i",
        "generateInfo": {
            "generateMethod": 1,
            "number": 30  # 拒絕再玩
        }
    },
    "coldplay": {
        "name": "Coldplay",  # 1999-01-01
        "artistId": "4gzpq5DPGxSnKTe4SA8HAU",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 15  # Everglow
        }
    },
    "wakin_chau": {
        "name": "周华健",  # 1987-02-28
        "artistId": "6wcIBaOvA9XNGgPujYZZ7L",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20  # 最近比較煩
        }
    },
    "fenghuangchuanqi": {
        "name": "凤凰传奇",  # 2005-04-01
        "artistId": "64NFGuC9PjqtNyJqnnTXh5",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "anita_mui": {
        "name": "梅艳芳",  # 1983
        "artistId": "06RD8CxzApXzuhHx54BhQL",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "phil_chang": {
        "name": "张宇",  # 1995
        "artistId": "7g65zUBhUAbiu4pAcoyWRd",
        "filterTrackByName": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "shawn_mendes": {
        "name": "Shawn Mendes",  # 2014-11-04
        "artistId": "7n2wHs1TKAczGzO7Dd2rGr",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "amei_chang": {
        "name": "张惠妹",  # 1996-07-12
        "artistId": "6noxsCszBEEK04kCehugOp",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "andy_lau": {
        "name": "刘德华",  # 1983-12-01
        "artistId": "2n3uDrupL8UtFSeZhY38MS",
        "generateInfo": {
            "generateMethod": 1,
            "number": 30
        }
    },
    "hacken_lee": {
        "name": "李克勤",  # 1986-01-01
        "artistId": "3PV11RNUoGfX9tMN2wVljB",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "tanya_chua": {
        "name": "蔡健雅",  # 1997-08-01
        "artistId": "376pcuw4IgWBMOUwCr8kIm",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "michael_jackson": {
        "name": "Michael Jackson",  # 1972-01-24
        "artistId": "3fMbdgg4jU18AjLCKBhRSm",
        "generateInfo": {
            "generateMethod": 1,
            "number": 50
        }
    },
    "ariana_grande": {
        "name": "Ariana Grande",  # 2008-09-30
        "artistId": "66CXWjxzNUsdJxJ2JdwvnR",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "huahua": {
        "name": "华晨宇",  # 2013-11-22, 2013年快乐男声全国总冠军
        "artistId": "7v7bP8NfcMYh4sDADEAy6Z",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "billie_eilish": {
        "name": "Billie Eilish",  # 2016-11-17
        "artistId": "6qqNVTkY8uBg9cP3Jd7DAH",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "stefanie_sun": {
        "name": "孙燕姿",  # 2000
        "artistId": "0SIXZXJCAhNU8sxK0qm7hn",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "jam_hsiao": {
        "name": "萧敬腾",  # 2007-08-03, 2007年台湾第一届超级星光大道踢馆成名
        "artistId": "4AJcTAMOLkRl3vf4syay8Q",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "adele": {
        "name": "Adele",  # 2008-01-20
        "artistId": "4dpARuHxo51G3z768sgnrY",
        "generateInfo": {
            "generateMethod": 2,
            "number": 100000000
        }
    },
    "mayday": {
        "name": "五月天",  # 1999-07-07
        "artistId": "16s0YTFcyjP4kgFwt7ktrY",
        "generateInfo": {
            "generateMethod": 1,
            "number": 30
        }
    },
    "karen_mok": {
        "name": "莫文蔚",  # 1993-07-01
        "artistId": "6jlz5QSUqbKE4vnzo2qfP1",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "faye_wong": {
        "name": "王菲",  # 1989-01-01
        "artistId": "3df3XLKuqTQ6iOSmi0K3Wp",
        "generateInfo": {
            "generateMethod": 1,
            "number": 35
        }
    },
    "wangfeng": {
        "name": "汪峰",  # 2000-10-10
        "artistId": "10LslMPb7P5j9L2QXGZBmM",
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "beyond": {
        "name": "Beyond",  # 1986-01-01
        "artistId": "4F5TrtYYxsVM1PhbtISE5m",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "leehom_wang": {
        "name": "王力宏",  # 1995-12-17
        "artistId": "2F5W6Rsxwzg0plQ0w8dSyt",
        "generateInfo": {
            "generateMethod": 1,
            "number": 25
        }
    },
    "xusong": {
        "name": "许嵩",  # 2007-03-21
        "artistId": "2hgxWUG24w1cFLBlPSEVcV",
        "generateInfo": {
            "generateMethod": 1,
            "number": 25
        }
    },
    "jj_lin": {
        "name": "林俊杰",  # 2003-04-01
        "artistId": "7Dx7RhX0mFuXhCOUgB01uM",
        "generateInfo": {
            "generateMethod": 1,
            "number": 40
        }
    },
    "g_e_m": {
        "name": "邓紫棋",  # 2009
        "artistId": "7aRC4L63dBn3CiLDuWaLSI",
        "generateInfo": {
            "generateMethod": 1,
            "number": 30
        }
    },
    "bruno_mars": {
        "name": "Bruno Mars",  # 2009-01-27
        "artistId": "0du5cEVh5yTK9QJze8zA0C",
        "filterAlbums": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 20
        }
    },
    "eason_chan": {
        "name": "陈奕迅",  # 1997-01-10
        "artistId": "2QcZxAgcs2I1q7CtCkl6MI",
        "generateInfo": {
            "generateMethod": 1,
            "number": 50
        }
    },
    "jay_chou": {
        "name": "周杰伦",  # 2000-11-06
        "artistId": "2elBjNSdBE2Y3f0j1mjrql",
        "generateInfo": {
            "generateMethod": 1,
            "number": 100
        },
        "excludeTracks": {
            "6iTu6axECEKNS13qL3XOfw": "不能說的秘密"  # 重复&演唱会版本
        }
    },
    "jacky_cheung": {
        "name": "张学友",  # 1985-01-01
        "artistId": "1Hu58yHg2CXNfDhlPd7Tdd",
        "mustMainArtist": True,
        "generateInfo": {
            "generateMethod": 1,
            "number": 50
        },
        "excludeTracks": {
            "3EON61J0AHJxHYwVqmJXez": "In Love with You"  # 重复&演唱会版本
        }
    }
}

# == Define other artists
otherArtists = {
    "gillian_chung": {
        "name": "钟欣潼",  # 2003, 放低過去
        "artistId": "7ICw984KHxGz5WtEzfjxG3"
    },
    "hailun": {
        "name": "海伦",  # 2018-05-25
        "artistId": "2f9O9Vy7xlAghr07uxXYMh"
    },
    # ----- Don"t belong here
    "tones_and_i": {
        "name": "Tones And I",
        "artistId": "2NjfBq1NflQcKSeiDooVjY"
    },
    # ----- Spotify only
    "chenyifa": {
        "name": "陈一发",
        "artistId": "10xtjTRMlKZ7aFx6VBQlSj"
    },
    "namewee": {
        "name": "黄明志",
        "artistId": "24jrxG0tKcwgAzsLuPzyMi"
    },
    # ----- More hits (>3)
    # ----- 流行
    "gebilaofan": {
        "name": "隔壁老樊",  # 2019-04-18
        "artistId": "1lGtvqG3JDiT3bbnJaCxfe"
    },
    "zhangbichen": {  # *
        "name": "张碧晨",  # 2014-07-18, 2014年中国好声音第三季年度冠军
        "artistId": "7n6JzP9GxGVVzXG0t0gLu3"
    },
    "zhousihan": {  # *
        "name": "周思涵",  # 2015-11-06
        "artistId": "0Nu7uGMynoaIdKnfLRgxJ8"
    },
    "zhousihan-2": {
        "name": "周思涵2",
        "artistId": "0ba03M9f4Zxx9oSqpKmo2T"
    },
    "renran": {  # ***
        "name": "任然",  # 2014
        "artistId": "6f4srX54JFrLNK4aTJe2Sc"
    },
    "asi": {  # **
        "name": "阿肆",  # 2012-12-01
        "artistId": "4yamiVzQPYBb02ceSu0jaI"
    },
    # ----- One hit (<4)
    "bojue": {
        "name": "伯爵Johnny",  # 2020-11-26
        "artistId": "2DCXAxaM4TdCBDtx2deFn2"
    },
    "bojue-2": {
        "name": "伯爵Johnny2",
        "artistId": "7xzC31BgSOWsAvun3j2bSS"
    },
    "huatong": {
        "name": "花僮",  # 2013-01-01, 2013年星光大道月亚军, 2014年最美和声第二季孙楠战队12强学员
        "artistId": "3bUk9TeFsLn98GnfKIzMua"
    },
    "angang": {
        "name": "暗杠",  # 2019-09-09
        "artistId": "21IJ2VE7Rmqk9YMfTtE1wZ"
    },
    "jinzhiwen": {
        "name": "金志文",  # 2012-02-08, 2012年中国好声音第一季杨坤组冠军、年度总决赛第4名
        "artistId": "1p8mNyT18G4coJooY8NTGN"
    },
    "suyunying": {
        "name": "苏运莹",  # 2015-03-13, 2015年中国好歌曲第二季全国总决赛亚军
        "artistId": "63tzlZxY9iaOeUnmGfwlyA"
    },
    "baoshi_gem": {
        "name": "宝石Gem",  # 2019-09-02, 2019年参加中国新说唱2019
        "artistId": "0p0KwawjbChNZh3O0L3z8i"
    },
    "zhaoyingjun": {
        "name": "赵英俊",  # 2016-04-07, 2004年我型我秀全国20强
        "artistId": "393qzhbUiZuv7pqKjjUSqq"
    },
    "maixiaodou": {
        "name": "麦小兜",  # 2017-10-24
        "artistId": "6sgZgnXFneErJ5HtO9bj9t"
    },
    "mailajiaoyeyongquan": {
        "name": "买辣椒也用券",  # 2016-08-03
        "artistId": "3nG9ei7y7HUPIN8nE5Nyyx"
    },
    "xujiahao": {
        "name": "烟(许佳豪)",  # 2021-05-27
        "artistId": "2DXogZyZTpItlsIGCG6Qpt"
    },
    "yuanyawei": {
        "name": "袁娅维",  # 2011-11-29, 2012年中国好声音第一季刘欢组四强
        "artistId": "70paW48PtCtUjtndElrjrL"
    },
    "kelly_yu": {
        "name": "于文文",  # 2016-02-05
        "artistId": "5R56NYbLCC2HpOwlYBnmeN"
    },
    "yinqueshiting": {
        "name": "音阙诗听",  # 2017-02-14
        "artistId": "6JZIgN9gEgNSS8lY5pmwbx"
    },
    "zhanzhanyuluoluo": {
        "name": "展展与罗罗",  # 2019-02-22
        "artistId": "7jqlVGxCx6cj6o9FPmO98s"
    },
    "daiquan": {
        "name": "戴荃",  # 2015-01-30
        "artistId": "20vLqxWyyRuMaNpMsgZOI6"
    },
    "rensuxi": {
        "name": "任素汐",  # 2016
        "artistId": "16rAFXQVz2WBpTH9uc1LA8"
    },
    "xufei": {
        "name": "许飞",  # 2007.06.04, 2006年超级女生第三届全国总决赛第6名
        "artistId": "7jQNVznzEejg5gU5B0AmfQ"
    },
    "wangerlang": {
        "name": "王贰浪",  # 2018
        "artistId": "6jNRSV0cd0kL5Tfz6JPxZA"
    },
    "wangerlang-2": {
        "name": "王贰浪2",
        "artistId": "6qXHEV470p1bYHxkTSVrRs"
    },
    "wangheye": {
        "name": "王赫野",  # 2021-03-11
        "artistId": "2sAy0e2cL6jbo0ukxlxWNJ"
    },
    "usa_for_africa": {
        "name": "U.S.A. For Africa",  # 1985
        "artistId": "7sF6m3PpW6G6m6J2gzzmzM"
    },
    "liujinrui": {
        "name": "刘瑾睿",  # 2018-07-11
        "artistId": "0ySwuPxQeg9GsjWO92RVLF"
    },
    "baisong": {
        "name": "柏松",  # 2019-05-08
        "artistId": "5dGgQ6EQsfOPRiv2V0b846"
    },
    # ----- Nah
    "gai_zhouyan": {
        "name": "GAI周延",  # 2017-08-16, 2017年中国有嘻哈第一季并列冠军
        "artistId": "37EUUUGKMLP6KSKrN9q39m"
    }
}

artists = otherArtists | generateArtists
