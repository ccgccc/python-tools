import re
import xlwt
import requests
from bs4 import BeautifulSoup

# IMDB 个人创建电影列表的爬虫程序

crawl_way = 1 # 爬虫方式：0-url 1-本地html
file_name = 'imdb_mylist.xls' # excel文件名

if crawl_way == 0:
    imdb_lists = ['ls020993998', 'ls020993852', 'ls020993814', 'ls020993839', 'ls020993880', 'ls020993884', 'ls020996697', 'ls025002125']
else:
    imdb_lists = ['Drama', 'Comedy', 'Fiction', 'Action&Adventure', 'Mystery', 'Thriller&Horror', 'Animation', 'Others']
    #imdb_lists = ['Animation', 'Others']

# 创建excel工作簿
workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
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

def parse_one_page(html, page, sheet):
    soup = BeautifulSoup(html, 'lxml')
    lister_list = soup.find('div', {'class': 'lister-list'})
    lister_item_list = lister_list.find_all('div', {'class': 'lister-item mode-detail'})
    print(len(lister_item_list))
    begin_index = (page - 1) * 100 + 1
    for i in range(len(lister_item_list)):
        movie_value = lister_item_list[i]
        
        strInfo = movie_value.find('h3', {'class': 'lister-item-header'}).text.strip()
        infos = strInfo.split('.\n')
        index = infos[0].strip() # 排名
        subStrInfo = re.sub(infos[0] + '[.]', '', strInfo)
        subInfos = subStrInfo.split('(')
        title = subInfos[0].strip() # 标题
        #year = re.sub(title + '[(]', '', subInfos).strip()[-5:-1] # 年份
        year = re.findall('(\d+)', re.sub(title, '', subStrInfo).strip())[0] # 年份
        
        rating_part = movie_value.find('span', {'class': 'ipl-rating-star__rating'})
        rating = rating_part.text.strip() if(rating_part != None) else str(0) # 评分
        
        superlink = movie_value.find('a')
        link = 'https://www.imdb.com' + superlink.get('href').split('/?')[0] # 链接
        
        strInfo2 = movie_value.find_all('p', {'class': 'text-muted text-small'})[1].text.strip()
        newStrInfo2 = re.sub('\s', '', strInfo2)
        newStrInfo2 = re.sub(',', ', ', newStrInfo2)
        newStrInfo2 = re.sub('Directors:', '', newStrInfo2)
        newStrInfo2 = re.sub('Director:', '', newStrInfo2)
        newStrInfo2 = re.sub('Stars:', '', newStrInfo2)
        infos2 = newStrInfo2.split('|')
        director = infos2[0] # 导演
        stars = infos2[1] if(len(infos2) > 1) else '...' # 主演
        
        description = movie_value.find('p', {'class': ''}).text.strip().split('See full summary')[0].strip() # 简介
        
        sheet.write(i+begin_index, 0, int(index), style)
        sheet.write(i+begin_index, 1, title, style)
        sheet.write(i+begin_index, 2, float(rating), style)
        sheet.write(i+begin_index, 3, int(year), style)
        sheet.write(i+begin_index, 4, director, style)
        sheet.write(i+begin_index, 5, stars, style)
        sheet.write(i+begin_index, 6, link, style)
        sheet.write(i+begin_index, 7, description, style)
        #sheet.write(i+1, 6, xlwt.Formula(('HYPERLINK("%s","%s")' % (link, 'link'))), style)
        yield index + '; ' + title + '; ' + rating + '; ' + year + '; ' + director + '; ' + stars #+ '; ' + description

def write_head(sheet):
    sheet.write(0, 0, 'Rank', style)
    sheet.write(0, 1, 'Title', style)
    sheet.write(0, 2, 'Rating', style)
    sheet.write(0, 3, 'Year', style)
    sheet.write(0, 4, 'Director', style)
    sheet.write(0, 5, 'Stars', style)
    sheet.write(0, 6, 'Link', style)
    sheet.write(0, 7, 'Description', style)

def create_sheet(html):
    soup = BeautifulSoup(html, 'lxml')
    list_name = soup.find('h1', {'class': 'header list-name'}).text.strip()
    list_num = soup.find('div', {'class': 'desc lister-total-num-results'}).text.strip().split(' ')[0]
    sheet = workbook.add_sheet(list_name, cell_overwrite_ok=True)
    sheet.col(1).width = 256*20 # 列宽n个字符长度，256为衡量单位
    sheet.col(4).width = 256*20
    sheet.col(5).width = 256*25
    sheet.col(7).width = 256*256-1
    write_head(sheet)
    return list_name, list_num, sheet

def main():
    info_list = [[0] * 2 for i in range(len(imdb_lists))]
    index = 0
    for imdb_list in imdb_lists:
        if crawl_way == 0:
            url = 'https://www.imdb.com/list/' + imdb_list
            html = get_one_page(url)
        else:
            with open(imdb_list + ' - IMDb1.html', 'r', encoding='utf-8') as f:
                html = f.read()
        list_name, list_num, sheet = create_sheet(html)
        info_list[index][0] = list_name
        info_list[index][1] = list_num
        index += 1
        
        print('\n\n******************************************************************************************')
        print('List: ' + list_name + ', ListNum: ' + list_num)
        for i in range(int(int(list_num)/100) + 1):
            page = i + 1
            print('\nList: ' + list_name + ', Page: ' + str(page) + ', Num: ', end = '')
            if crawl_way == 0:
                url = 'https://www.imdb.com/list/' + imdb_list + '/?page=' + page
                html = get_one_page(url)
            else:
                with open(imdb_list + ' - IMDb' + str(page) + '.html', 'r', encoding='utf-8') as f:
                    html = f.read()
            for item in parse_one_page(html, page, sheet):
                print(item)

    # 统计
    print('\n\n********************************** Statistic ********************************************')
    sheet = workbook.add_sheet('Statistic', cell_overwrite_ok=True)
    total_num = 0
    for i in range(len(info_list)):
        print(info_list[i][0] + ': ', info_list[i][1])
        total_num += int(info_list[i][1])
        sheet.write(i, 0, info_list[i][0], style)
        sheet.write(i, 1, int(info_list[i][1]), style)
    print('TotalNum: ', total_num)
    sheet.write(len(info_list), 0, 'Total', style)
    sheet.write(len(info_list), 1, total_num, style)

    # 保存文件
    workbook.save(file_name)  

if __name__ == '__main__':
    main()