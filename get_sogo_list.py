import requests
from bs4 import BeautifulSoup
import xlwt
import time


def save_sogo_list_file(query, max_page_limit,sogo_headers):
    xls = xlwt.Workbook()

    headers = sogo_headers

    for page_cnt in range(1, max_page_limit + 1):
        sheet1 = xls.add_sheet(sheetname=f"第{page_cnt}页")
        table_titles = ['标题', '链接', '摘要', '作者', '发表时间']
        for i in range(len(table_titles)):
            sheet1.write(0, i, table_titles[i])

        sogo_url = f"""
            https://weixin.sogou.com/weixin?query={query}&_sug_type_=1&s_from=input&_sug_=n&type=2&page={page_cnt}&ie=utf8
        """
        response = requests.get(url=sogo_url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        boxs = soup.find('div', attrs={"class": "news-box"}).find_all('li')
        row = 0
        for box in boxs:
            row += 1
            column = 0
            # 一条文字内容
            txt = box.find(name='div', attrs={"class": "txt-box"})
            # 标题
            title = txt.find('h3')
            sheet1.write(row, column, title.text)
            column += 1

            # 标题链接
            box_url = "https://weixin.sogou.com" + title.find('a').get(key="href")
            sheet1.write(row, column, box_url)
            column += 1

            # 摘要
            txt_info = txt.find('p')
            sheet1.write(row, column, txt_info.text)
            column += 1

            # 作者+发表时间
            author = txt.find('div').find('span', attrs={"class": "all-time-y2"})
            sheet1.write(row, column, author.text)
            column += 1

            Time = txt.find('div').find('span', attrs={"class": "s2"}).find('script')
            date = time.localtime(int(Time.text[-13:-3]))
            date = time.strftime("%Y-%m-%d %H:%M:%S", date)
            sheet1.write(row, column, date)
            column += 1

    file_name = f"E:\\spider_file\\sogo_{query}.xls"
    xls.save(file_name)

    return file_name
