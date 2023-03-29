# 基于爬取的新闻文本计算指标值
import json
import requests
import os

with open(os.path.join('.', 'map.json'), 'r', encoding='utf-8') as f:
    lang_mapping = json.load(f)


def get_all_indicator(type, content):
    URL = 'http://192.168.128.125:25001/common/all'
    data = {'lg_type': type, 'lg_text': content}
    response = requests.post(URL, data)
    json_data = json.loads(response.text)
    data = json_data['data']
    return data


for type in lang_mapping:
    dir_name = lang_mapping[type]
    dir_path = os.path.join('.', dir_name)
    files = os.listdir(dir_path)
    dic_obj = dict()
    for file in files:
        file_path = os.path.join(dir_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[1:]  # 去除第一行来源
            content = "".join([line.strip() for line in lines])
            indicators = get_all_indicator(type, content)
            for key in indicators:
                if key in dic_obj:
                    dic_obj[key] += indicators[key]
                else:
                    dic_obj[key] = indicators[key]

    with open('./indicators.txt', 'a', encoding='utf-8') as _f:
        _f.write('--- {} ---\n'.format(type))
        for key in dic_obj:
            _f.write('  {} : {}\n'.format(key, dic_obj[key] / len(files)))
