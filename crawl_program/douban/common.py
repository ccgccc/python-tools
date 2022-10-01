import re
import sys
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'Host': 'movie.douban.com',
            # 从豆瓣网页获取cookie
            'Cookie': 'bid=3Y2pfSCmesg; ll="108288"; __gads=ID=08230217faebdaa0-22837bf11bb40099:T=1660013292:RT=1660013292:S=ALNI_MZzI-UDRuxLNiZouosmG2hVPauAdQ; _vwo_uuid_v2=D9E0105763686472294A681682148DE92|83cc250b3463f9e1e0a6bcd8ee80baf3; _ga=GA1.2.1807939346.1660013292; push_doumail_num=0; __utmv=30149280.23009; push_noty_num=0; __utma=30149280.1807939346.1660013292.1662539076.1663038388.4; __utmz=30149280.1663038388.4.3.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie/subject_search; __utma=223695111.722769447.1660013292.1662539076.1663038388.4; __utmz=223695111.1663038388.4.3.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie/subject_search; __gpi=UID=0000086898e6b35a:T=1660013292:RT=1664616077:S=ALNI_MYW-iC1aBp4PHkwrkSa0_ciVX1tZA; dbcl2="167045714:Vb1fpVbV9VI"; ck=MfFp; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1664620850%2C%22https%3A%2F%2Fsearch.douban.com%2Fmovie%2Fsubject_search%3Fsearch_text%3Dbetter%2Bcall%2Bsaul%26cat%3D1002%22%5D; _pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=0f43263e4f0cc16f.1660013292.6.1664623849.1664616337.'
        }
        response = requests.get(url, headers=headers)
        print(response)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as ex:
        print(repr(ex))
        print('\n**********')
        print('Douban cookie expired, please retrive a new cookie.')
        print('**********\n')
        sys.exit()


def parse_one_page(html, start):
    # 将爬取的网页保存到本地
    # with open('douban_mylist_' + str(start) + '.html', 'a', encoding=file_encoding) as f:
    #     f.write(html+'\n')
    soup = BeautifulSoup(html, 'lxml')
    grid_view = soup.find('div', {'class': 'grid-view'})
    item_list = grid_view.find_all('div', {'class': 'item'})
    for i in range(len(item_list)):
        item_info = item_list[i].find('div', {'class': 'info'})
        li_list = item_info.find('ul').find_all('li')
        # 标题
        title = re.sub('[,]', '，', li_list[0].find(
            'em', {'class': ''}).text.strip())
        # 影片信息
        info = li_list[1].text.strip()
        # 从影片信息中提取上映日期
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}(?!,).*?(?= )')
        releaseInfoList = pattern.findall(info)
        # print(releaseInfoList)
        releaseInfo = ' / '.join(releaseInfoList)
        # print(releaseInfo)
        match = re.match(r'\d{4}-\d{2}-\d{2}', releaseInfo)
        releaseDate = match.group(0) if match != None else ''
        # print(releaseDate)
        # 我的评分与标记日期
        rating_spans = li_list[2].find_all('span')
        if (len(rating_spans) > 1):
            rating = re.search('(?<=rating)\\d', str(
                rating_spans[0])).group().strip()
            date = rating_spans[1].text.strip()
        else:
            rating = ''
            date = rating_spans[0].text.strip()
        # 我的短评
        if (len(li_list) > 3):
            comment = re.sub('\n', '\t', li_list[3].text.strip())
        else:
            comment = ''
        print('start: ' + str(start) + ", index: " +
              str(i + 1) + ", title: " + title)
        yield title + ', ' + rating + ', ' + date + ', ' + comment + ', ' + releaseDate + ', ' + info
