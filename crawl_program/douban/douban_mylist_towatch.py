# coding=UTF-8
import re
import time
from common import *

# 豆瓣账号看过电影的爬虫程序

# 在豆瓣账号中找到"想看"，将此时的url替换到此处
base_url = 'https://movie.douban.com/people/167045714/wish'
# 此处定义此豆瓣账号标记想看的电影总数
total_num = 52
# 此处定义生成文件名
file_name = 'douban_mylist_towatch_' + time.strftime("%Y-%m-%d") + '.csv'
# 此处定义文件编码
file_encoding = 'utf-8-sig'


def main():
    with open(file_name, 'w', encoding=file_encoding) as f:
        f.write('标题, 我的评分, 标记日期, 短评, 上映日期, 影片信息\n')
    for i in range(0, total_num, 15):
        url = base_url + '?start=' + str(i)
        # print(url)
        html = get_one_page(url)
        for item in parse_one_page(html, i):
            # print(item)
            re.sub('\n', '\t', item)
            write_to_csv_file(item)
        # 歇一秒
        time.sleep(1)


def write_to_csv_file(content):
    with open(file_name, 'a', encoding=file_encoding) as f:
        f.write(content+'\n')


if __name__ == '__main__':
    main()
