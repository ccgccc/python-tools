import re
import xlwt
import requests
from bs4 import BeautifulSoup

# IMDB TOP 250 的爬虫程序

crawl_way = 1 # 爬虫方式：0-url 1-本地html
file_name = 'imdb250.xls' # excel文件名

# 创建excel工作簿与工作表
workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = workbook.add_sheet('imdb250', cell_overwrite_ok=True)
# 设置列宽
sheet.col(1).width = 256*50 # 列宽n个字符长度，256为衡量单位
sheet.col(4).width = 256*35
sheet.col(5).width = 256*40
sheet.col(6).width = 256*35
# 设置字体
font = xlwt.Font()
font.name = '等线' # 字体类型
font.height = 20*11 # 字体大小，11为字号，20为衡量单位
style = xlwt.XFStyle()
style.font = font

def get_one_page(url):
    print('fetching url: ' + url)
    response = requests.get(url)
    if response.status_code == 200:
        print('fetch completed!\nfetched results:')
        return response.text
    print('fetch url failed with status_code = ' + response.status_code + '!')
    return None

def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    tbody = soup.find('tbody', {'class': 'lister-list'})
    tr_list = tbody.find_all('tr')
    for i in range(len(tr_list)):
        movie_value = tr_list[i]
        
        strInfo = movie_value.find('td', {'class': 'titleColumn'}).text.strip()
        infos = strInfo.split('.\n')
        index = infos[0].strip() # 排名
        subInfos = re.sub(infos[0] + '[.]', '', strInfo).split('(')
        title = subInfos[0].strip() # 标题
        year = subInfos[1].split(')')[0].strip() # 年份
        
        rating = movie_value.find('td', {'class': 'ratingColumn imdbRating'}).text.strip() # 评分
        
        superlink = movie_value.find_all('a')[1]
        link = 'https://www.imdb.com' + superlink.get('href').split('/?')[0] # 链接
        infos2 = str(superlink.get('title')).split('(dir.),')
        director = infos2[0].strip() # 导演
        actor = infos2[1].strip() # 主演
        
        sheet.write(i+1, 0, int(index), style)
        sheet.write(i+1, 1, title, style)
        sheet.write(i+1, 2, float(rating), style)
        sheet.write(i+1, 3, int(year), style)
        sheet.write(i+1, 4, director, style)
        sheet.write(i+1, 5, actor, style)
        sheet.write(i+1, 6, link, style)
        #sheet.write(i+1, 6, xlwt.Formula(('HYPERLINK("%s","%s")' % (link, 'link'))), style)
        yield index + '; ' + title + '; ' + rating + '; ' + year + '; ' + director + '; ' + actor # + '; ' + link

def write_head():
    sheet.write(0, 0, 'Rank', style)
    sheet.write(0, 1, 'Title', style)
    sheet.write(0, 2, 'Rating', style)
    sheet.write(0, 3, 'Year', style)
    sheet.write(0, 4, 'Director', style)
    sheet.write(0, 5, 'Actor', style)
    sheet.write(0, 6, 'Link', style)

def main():
    write_head()
    if crawl_way == 0:
        url = 'https://www.imdb.com/chart/top'
        html = get_one_page(url)
    else:
        with open('imdb250.html', 'r', encoding='utf-8') as f:
            html = f.read()

    for item in parse_one_page(html):
        print(item)
    workbook.save(file_name)  

if __name__ == '__main__':
    main()