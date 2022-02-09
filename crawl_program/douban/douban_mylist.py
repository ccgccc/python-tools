# coding=UTF-8
import re
import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# 豆瓣账号看过电影的爬虫程序

## 在豆瓣账号中找到看过，将此时的url替换到此处
base_url = 'https://movie.douban.com/people/167045714/collect'
## 此处定义此豆瓣账号标记看过的电影总数
total_num = 1111
## 此处定义生成文件名
file_name = 'douban_mylist.csv'
## 此处定义文件编码
file_encoding = 'utf-8-sig'

def get_one_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html, start):
    # with open('douban_mylist_' + str(start) + '.html', 'a', encoding=file_encoding) as f:
    #     f.write(html+'\n')
    soup = BeautifulSoup(html, 'lxml')
    grid_view = soup.find('div', {'class': 'grid-view'})
    item_list = grid_view.find_all('div', {'class': 'item'})
    for i in range(len(item_list)):
        item_info = item_list[i].find('div', {'class': 'info'})
        li_list = item_info.find('ul').find_all('li')
        # 标题
        title = re.sub('[,]', '，', li_list[0].find('em', {'class': ''}).text.strip())
        # 影片信息
        info = li_list[1].text.strip()
        # 我的评分与标记日期
        rating_spans = li_list[2].find_all('span')
        if (len(rating_spans) > 1):
            rating = re.search('(?<=rating)\\d', str(rating_spans[0])).group().strip()
            date = rating_spans[1].text.strip()
        else:
            rating = ''
            date = rating_spans[0].text.strip()
        # 我的短评
        if (len(li_list) > 3):
            comment = re.sub('\n', '\t', li_list[3].text.strip())
        else:
            comment = ''
        print('start: ' + str(start) + ", index: " + str(i + 1) + ", title: " + title)
        yield title + ', ' + rating + ', ' + date + ', ' + comment + ', ' + info

def write_to_file(content):
    with open(file_name, 'a', encoding=file_encoding) as f:
        f.write(content+'\n')

def main(start):
    url = base_url + '?start=' + str(start)
    html = get_one_page(url)
    for item in parse_one_page(html, start):
        # print(item)
        re.sub('\n', '\t', item)
        write_to_file(item)

if __name__ == '__main__':
    with open(file_name, 'w', encoding=file_encoding) as f:
        f.write('标题, 我的评分, 标记日期, 短评, 影片信息\n')
    for i in range(0, total_num, 15):
        main(start=i)
        time.sleep(1)