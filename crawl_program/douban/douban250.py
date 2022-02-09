# coding=UTF-8
import re
import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# 豆瓣电影 Top 250 的爬虫程序

## 此处定义生成文件名
file_name = 'douban250.csv'
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
    # with open('douban250_' + str(start) + '.html', 'a', encoding=file_encoding) as f:
    #   f.write(html+'\n')
    soup = BeautifulSoup(html, 'lxml')
    ol_list = soup.find('ol', {'class': 'grid_view'})
    li_list = ol_list.find_all('li')
    for i in range(len(li_list)):
        # print('start: ' + str(start) + ", index: " + str(i))
        move_value = li_list[i]
        index = move_value.find('em', {'class': ''}).text.strip()
        title = move_value.find('span', {'class': 'title'}).text.strip()
        strInfo = re.search('(?<=>).*?(?=<br/>)', str(move_value.select_one('.bd p')), re.S | re.M).group().strip()
        newStrInfo = re.sub('导演:', '', strInfo)
        newStrInfo = re.sub('主演:', ',', newStrInfo)
        newStrInfo = re.sub('主演', ',', newStrInfo)
        newStrInfo = re.sub('主...', ',', newStrInfo)
        newStrInfo = re.sub('&amp', ',&amp', newStrInfo)
        infos = newStrInfo.split(',')
        director = infos[0].strip()
        if len(infos) > 1:
            actor = infos[1].strip()
            actor = '...' if(actor == '') else actor
        else:
            actor = '...'
        strInfo2 = re.search('(?<=<br/>).*?(?=<)', str(move_value.select_one('.bd p')), re.S | re.M).group().strip()
        infos2 = strInfo2.split('/')
        year = infos2[0].strip()
        area = infos2[1].strip()
        type = infos2[2].strip()
        rating = move_value.find('span', {'class': 'rating_num'}).text.strip()
        quote_span = move_value.find('span', {'class': 'inq'});
        quote = '' if quote_span is None else quote_span.text.strip()    
        yield index + ', ' + title + ', ' + rating + ', ' + year + ', ' + area + ', ' + type + ', ' + director + ', ' + actor + ', ' + quote

def write_to_file(content):
    with open(file_name, 'a', encoding=file_encoding) as f:
        f.write(content+'\n')

def main(start):
    url = 'https://movie.douban.com/top250?start=' + str(start)
    html = get_one_page(url)
    for item in parse_one_page(html, start):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    with open(file_name, 'w', encoding=file_encoding) as f:
        f.write('排名, 标题, 评分, 年份, 制片国家/地区, 类型, 导演, 主演\n')
    for i in range(0, 250, 25):
        main(start=i)
        time.sleep(1)