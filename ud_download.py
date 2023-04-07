import random
import requests
import json
import os

ua_list = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]

WEBSIT_PREFIX_URL = 'https://www3.nhk.or.jp'

def get_response_data(url, headers):
    response = requests.get(url, headers)
    json_data = json.loads(response.text)
    data = json_data['data']
    return data


def create_txt_file(index, data, dirname):
    cur_path = '{}\\{}'.format(os.getcwd(), dirname)
    if not os.path.exists(cur_path):
        os.makedirs(cur_path)
    filename = 'news{}.txt'.format(index)
    filepath = os.path.join(cur_path, filename)
    with open(filepath, 'w+', encoding='utf-8') as f:
        detail = data['detail']
        origin_url = WEBSIT_PREFIX_URL + data['page_url']
        f.write('FROM:{}'.format(origin_url))
        f.write('\n')
        f.write(detail.strip().replace('<br />', '').replace('\n', ''))


def download_news(language, dirname, start = 0):
    print('--- getting {} data ---'.format(language))
    LIST_URL = 'https://nwapi.nhk.jp/nhkworld/rdnewsweb/v7b/{}/outline/list.json'.format(
        language
    )
    DOWNLOAD_URL = 'https://nwapi.nhk.jp/nhkworld/rdnewsweb/v6b/{}/detail/'.format(language)
    LIMIT = 5
    headers = {'User-Agent': ua_list[random.randint(0, len(ua_list))]}
    news_list = get_response_data(LIST_URL, headers)
    i = start
    while i < LIMIT:
        dic_data = get_response_data(DOWNLOAD_URL + news_list[i]['id'], headers)
        create_txt_file(i + 1, dic_data, dirname)
        i = i + 1

if __name__ == '__main__':
    with open('./map.json', 'r', encoding='utf-8') as f:
        json_mapping = json.load(f)

    # json_mapping including lg_code & storing directory name
    # for _ in json_mapping:
    #     _path_storing_dir_name = json_mapping[_]
    #     _path_storing_dir_path = '{}\\{}'.format(os.getcwd(), _path_storing_dir_name)
    #     pass

    download_news('ur', json_mapping['ur'])


