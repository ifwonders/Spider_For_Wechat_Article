import requests
from bs4 import BeautifulSoup
import xlrd


def redirect(sogo_to_weixin_url, sogo_headers):
    response = requests.get(url=sogo_to_weixin_url, headers=sogo_headers)
    soup = BeautifulSoup(response.text, 'lxml')
    scr_func = soup.find('script').text
    try:
        scr_funcs = scr_func[scr_func.index('var'):scr_func.index('window')].split(';')
    except:
        print('找不到重定向链接')
    url = ''
    for func in scr_funcs:
        try:
            url += func.strip()[func.strip().index('\'') + 1:func.strip().rindex('\'')]
        except:
            print('\n')
    return url.strip()
