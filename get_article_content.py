import requests
from bs4 import BeautifulSoup
import  bs4
bs4.element.Tag

def save_article(weixin_url,article_name):

    file_name = f"E:\\spider_file\\{article_name.strip().replace(' ','')[0:7]}.txt"

    url = weixin_url

    headers = {
        "Cookie":"ua_id=BDPvKjylfq1m60plAAAAAIQ1rCG9u-SZqgt0tSg1DcQ=; _clck=1fq1l2|1|fh4|0; wxuin=01240968194862; xid=52cbecc4aec78f5c0e954efc29e5c48e; mm_lang=zh_CN; rewardsn=; wxtokenkey=777",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    }

    response = requests.get(url, headers)
    # print(response.status_code)
    # print(response.text)
    print(url)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        # 文章链接失效
        content = (soup.find('body', attrs={"id": "activity-detail"})
                   .find('div', attrs={"id": "js_article"})
                   .find('div', attrs={"id": "js_base_container"})
                   .find('div', attrs={"id": "page-content"})
                   .find('div', attrs={"class": "rich_media_area_primary_inner"}))
    except:
        return "Error"

    file = open(file=file_name,mode='w+',encoding='utf-8')
    file.write(str(content))
    file.close()

    return file_name
