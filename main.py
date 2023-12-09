from selenium import webdriver
import time
import get_sogo_list
import xlrd
import redirect
import get_article_content
import article_html_analysis
import os
import shutil


if __name__ == '__main__':
    shutil.rmtree('E:\spider_file')
    os.mkdir('E:\spider_file')

    sogo_headers = {
        "Cookie": "ABTEST=7|1701786932|v1; SUID=2F820A702B83A20A00000000656F3534; IPLOC=CN3301; SUID=2F820A701C608C0A00000000656F3535; SUV=0026E51F700A822F656F356770C52947; SNUID=238E077C0C0A07C825FBA4040DC92032; ariaDefaultTheme=undefined",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    }

    # 第一步 保存搜狗搜索数据到表格
    file_name = get_sogo_list.save_sogo_list_file(query="五月天假唱", max_page_limit=2, sogo_headers=sogo_headers)

    # 第二步 由搜狗链接重定向到微信公众号链接
    xls = xlrd.open_workbook_xls(file_name)
    for sheet in xls.sheets():
        for row in range(1, sheet.nrows):
            sogo_to_weixin_url = sheet.cell(rowx=row, colx=1).value
            article_name = sheet.name + str(row)
            weixin_url = redirect.redirect(sogo_to_weixin_url=sogo_to_weixin_url, sogo_headers=sogo_headers)

            try:
                # 第三步 保存网页内容部分的源代码
                html_name = get_article_content.save_article(weixin_url, article_name)

                # 第四步 对源代码解析并保存正文内容
                text_name = article_html_analysis.html_anal(html_name)
            except UnicodeDecodeError:
                print('文件编码错误')
            except AttributeError:
                print('找不到该内容的正文部分或该链接内容失效')
            # except:
            #     print('未知错误')

            # 第五步 上传内容到百度模型分析
