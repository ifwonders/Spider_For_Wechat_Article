from selenium import webdriver
import time
import get_sogo_list
import xlrd
import redirect
import get_article_content

# url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1701962647&ver=4942&signature=DUf21LVCFZ5vCZG4iku3wafUBUlxEj84f7g5YA0E0XdxBZeJviFxX6gJidb3QrNN1S7FoqN0n7Ykp6fHxAqVZnEbsWJHhF2nYgDmoS55tLOD09bTuQSagDEyAcnFLUdN&new=1'
#
# driver = webdriver.Firefox()
# driver.get(url)
# driver.find_element(by=)

if __name__ == '__main__':
    sogo_headers = {
        "Cookie":"ABTEST=7|1701786932|v1; SUID=2F820A702B83A20A00000000656F3534; IPLOC=CN3301; SUID=2F820A701C608C0A00000000656F3535; SUV=0026E51F700A822F656F356770C52947; SNUID=238E077C0C0A07C825FBA4040DC92032; ariaDefaultTheme=undefined",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    }

    # 第一步 保存搜狗搜索数据到表格
    file_name = get_sogo_list.save_sogo_list_file(query="123", max_page_limit=2, sogo_headers=sogo_headers)

    # 第二部 由搜狗链接重定向到微信公众号链接
    xls = xlrd.open_workbook_xls(file_name)
    for sheet in xls.sheets():
        for row in range(1, sheet.nrows):
            sogo_to_weixin_url = sheet.cell(rowx=row, colx=1).value
            article_name = sheet.name+str(row)
            weixin_url = redirect.redirect(sogo_to_weixin_url=sogo_to_weixin_url, sogo_headers=sogo_headers)

            get_article_content.save_article(weixin_url,article_name)