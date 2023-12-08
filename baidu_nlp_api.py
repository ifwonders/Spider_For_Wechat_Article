import json
import requests
from urllib.parse import urlencode

# 我的APP_ID AK SK
APP_ID = '44489551'
AK = '29mMnQRAM9nIPhRtVKLKmQEW'
SK = 'rzTFub1TswGCOgCXXYGbI6M8wD3INaPs'

"""
    Step1: get token
"""
token_url = 'https://aip.baidubce.com/oauth/2.0/token'


def fetch_token():
    params = {
        'grant_type': 'client_credentials',
        'client_id': AK,
        'client_secret': SK
    }
    post_data = urlencode(params).encode('utf-8')
    token_response = requests.post(url=token_url, data=post_data)
    # print(token_response.text)
    """ EXAMPLE:
        {"refresh_token":"25.d4827209ef3c457cac979f1e1eef3e13.315360000.2017287787.282335-44489551",
        "expires_in":2592000,
        "session_key":"9mzdC34Xyz6yqVxlm8XN\/U69vbw+ZZuG\/4IlKEJHnGOdhMEHPrRlNGV1W3nsuJvG1BA4w3MVXWwEwm0y6jrOa8gceVR0kQ==",
        "access_token":"24.0fc5a05fc7c44b816ab703a0a770839b.2592000.1704519787.282335-44489551",
        "scope":"public brain_all_scope brain_nlp_sentiment_classify brain_nlp_news_summary brain_v1_nlp_txt_keywords_extraction brain_v1_nlp_txt_monet wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian ApsMisTest_Test\u6743\u9650 vis-classify_flower lpq_\u5f00\u653e cop_helloScope ApsMis_fangdi_permission smartapp_snsapi_base smartapp_mapp_dev_manage iop_autocar oauth_tp_app smartapp_smart_game_openapi oauth_sessionkey smartapp_swanid_verify smartapp_opensource_openapi smartapp_opensource_recapi fake_face_detect_\u5f00\u653eScope vis-ocr_\u865a\u62df\u4eba\u7269\u52a9\u7406 idl-video_\u865a\u62df\u4eba\u7269\u52a9\u7406 smartapp_component smartapp_search_plugin avatar_video_test b2b_tp_openapi b2b_tp_openapi_online smartapp_gov_aladin_to_xcx",
        "session_secret":"3d71b16d175480abf86e5cdc97c8d778"}
    """
    result = json.loads(token_response.text)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


"""
    Step2: call remote http server
"""
# 情感倾向分析    帮助文档 = https://cloud.baidu.com/doc/NLP/s/zk6z52hds
sentiment_classify = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify'

# 新闻摘要       帮助文档 = https://cloud.baidu.com/doc/NLP/s/Gk6z52hu3
news_summary = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary'

# 关键词提取     帮助文档 = https://cloud.baidu.com/doc/NLP/s/rl9zkamiq
txt_keywords_extraction = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/txt_keywords_extraction'

# 文本信息提取    帮助文档 = https://cloud.baidu.com/doc/NLP/s/Tlb3dlhoo
txt_monet = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/txt_monet'


def SC(token, txt):
    """
    http method: POST
    request URL: https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify
    URL attributes: access_token
    Headers: Content-Type: application/json
    request body example: {"text": "我爱祖国"}
    :param token:
    :param txt:(str) max to 2048bits
    :return:
    list     置信度   消极可能性    积极可能性   情感划分(0负向 1中性 2正向)
    e.g.
    [{'confidence': 0.887435, 'negative_prob': 0.0506543, 'positive_prob': 0.949346, 'sentiment': 2}]
    """

    concated_url = sentiment_classify + "?charset=UTF-8&access_token=" + token
    header = {"Content-Type": "application/json"}
    json_data = json.dumps({"text": txt})

    response = requests.post(url=concated_url, headers=header, data=json_data)

    sentiment = json.loads(response.text)['items']

    return sentiment[0]


def NS(token, content, max_summary_len, title=""):
    """
    http method: POST
    request URL: https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary
    URL attributes: access_token
    Headers: Content-Type: application/json
    request body example: {"title": "麻省理工学院为无人机配备RFID技术，进行仓库货物管理","content": "麻省理工学院的研究团队xxx","max_summary_len":200}
    :param token:
    :param content:_necessary
    :param max_summary_len:_necessary
    :param title:_unnecessary
    :return: (str) summary
    """

    concated_url = news_summary + "?charset=UTF-8&access_token=" + token
    header = {"Content-Type": "application/json"}
    json_data = json.dumps({"title": title, "content": content, "max_summary_len": max_summary_len})

    response = requests.post(url=concated_url, headers=header, data=json_data)

    summary = json.loads(response.text)['summary']

    return summary


def TKE(token, txt, num=0):
    """
    http method: POST
    request URL: https://aip.baidubce.com/rpc/2.0/nlp/v1/txt_keywords_extraction
    URL attributes: access_token
    Headers: Content-Type: application/json
    request body example: {"text":["学习书法，就选唐颜真卿《颜勤礼碑》原碑与对临「第1节」"],"num":4}
    :param token:
    :param txt:(array[]) necessary
    :param num:(int) unnecessary
    :return: (list)keywords
    """
    concated_url = txt_keywords_extraction + "?charset=UTF-8&access_token=" + token
    header = {"Content-Type": "application/json"}

    if num is not 0:
        json_data = json.dumps({"text": txt, "num": num})
    else:
        json_data = json.dumps({"text": txt})

    response = requests.post(url=concated_url, headers=header, data=json_data)

    keywords = json.loads(response.text)['results']

    return keywords


def TM(token, content_list,  content="", query_list="", query=""):
    """
    http method: POST
    request URL: https://aip.baidubce.com/rpc/2.0/nlp/v1/txt_keywords_extraction
    URL attributes: access_token
    Headers: Content-Type: application/json
    request body example:
    {
    "content_list":[
        {
            "content":"俄对乌空袭是对克里米亚大桥爆炸事件的回应。当地时间10月10日，乌克兰国家紧急事务局表示，空袭影响了乌克兰八个州和基辅市的关键基础设施，部分地区处于断水、断电状态。乌克兰能源部长加卢先科表示，当天能源系统遭到的攻击是自俄乌冲突开始以来最大的一次。据乌克兰国家紧急事务局10月11日通报的最新数据，10日俄罗斯对乌克兰各地的导弹打击已造成乌方19人死亡、105人受伤。",
            "query_list":[
                {
                    "query":"空袭时间"
                },
                {
                    "query":"死亡人数"
                }
            ]
        },
        {
            "content":"《如果我爱你》是由海润影视与明道工作室联合出品，徐辅军执导，明道、李沁、胡兵、白歆惠、狄杰等人气明星联袂主演的浪漫偶像剧。剧情跌宕起伏，非常精彩。",
            "query_list":[
                {
                    "query":"如果我爱你的出品公司"
                },
                {
                    "query":"主演"
                }
            ]
        }
    ]
}
    :param token:
    :param content_list:(list) 输入的文本列表，支持不超过2段的文本进行批量提取
    :param content:(str) 输入文本，每段文本不超过450个字符
    :param query_list:(list) 用户自定义的短语（或问题）列表，每段文本的短语（或问题）数量不超过5个
    :param query:(str) 用户自定义的短语（或问题）
    :return:(list) information
    """
    concated_url = txt_keywords_extraction + "?charset=UTF-8&access_token=" + token
    header = {"Content-Type": "application/json"}
    json_data = json.dumps({"content_list": content_list})

    response = requests.post(url=concated_url, headers=header, data=json_data)

    information = json.loads(response.text)['results_list']

    return information

if __name__ == '__main__':
    test_txt1 = '我爱祖国'

    # get access token
    token = fetch_token()

    # make request
    SC(token, test_txt1)
