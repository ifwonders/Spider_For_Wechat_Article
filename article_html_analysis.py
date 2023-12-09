from bs4 import BeautifulSoup


def html_anal(html_name):
    html = open(html_name)

    text_file_name = html_name.replace('.txt', 'content.txt')
    text = open(text_file_name,mode='x')

    soup = BeautifulSoup(html, 'lxml')

    # 文章全文内容
    all_content = soup.find('div', attrs={"class": "rich_media_wrp"})
    # print(all_content.text.strip())

    # 文章标题
    title = all_content.find('h1', attrs={"class": "rich_media_title"})
    print(title.text.strip())
    # print('=' * 30)
    text.write(title.text.strip() + '\n')
    text.write('\n'*2)

    # 文章作者 发表时间 发表地点
    meta_content = all_content.find('div', attrs={"id": "meta_content"})

    # 作者公众号
    author = meta_content.find('strong', attrs={"class": "profile_nickname"})
    WCID = meta_content.find('span', attrs={"class": "profile_meta_value"})
    # 发表时间
    publish_time = meta_content.find('em', attrs={"id": "publish_time"})
    # 发表地点
    location = meta_content.find('span', attrs={"aria-hidden": "true", "id": "js_ip_wording"})

    # print(author.text.strip())
    # print('=' * 30)
    text.write(author.text.strip() + '\n')
    text.write('\n'*2)

    # print(WCID.text.strip())
    # print('=' * 30)
    text.write(WCID.text.strip() + '\n')
    text.write('\n'*2)

    # print(publish_time.text.strip())
    # print('=' * 30)
    text.write(publish_time.text.strip() + '\n')
    text.write('\n'*2)

    # print(location.text.strip())
    # print('=' * 30)
    text.write(location.text.strip() + '\n')
    text.write('\n'*2)

    # 文章转载来源 可能存在 应该try
    # origin = all_content.find('p', attrs={"class": "original_primary_card_tips"})
    # print(origin.text.strip().replace('\n',''))
    # print('='*30)

    # 正文部分

    body = all_content.find('div',
                            attrs={"class": """rich_media_content js_underline_content autoTypeSetting24psection"""})
    paras = body.find_all('p')
    for para in paras:
        # if para.has_attr('data-check-id') is True:
        # print(para.text.strip().replace('\n', ''))
        # print('=' * 30)
        text.write(para.text.strip().replace('\n', ''))
        text.write('\n'*2)


    html.close()
    text.close()

    return text_file_name
