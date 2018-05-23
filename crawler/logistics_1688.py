#!/usr/bin/env python
# encoding=utf-8
import os
import re
import time
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

url = 'http://56.1688.com/routes/shanghai.htm'  # 阿里巴巴物流上海线路
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}
# 构造头部
# cookie = {}
# pxs = {}  # TODO 代理池
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
sh2other = []  # 上海到其他城市转接列表
for x in soup.find_all(href=re.compile('.htm'), title=re.compile('上海')):
    sh2other.append(x['href'].replace('//', 'http://', 1))

sh2other = sh2other[1:]  # 删除无用链接


def save2csv(data):
    save_dir = {
        'path':
        os.path.join(
            os.path.dirname(__file__).replace(
                os.path.dirname(__file__), 'dataset')),
        'fn':
        data.iloc[0, 0].replace(' ', '') + '.csv'
    }
    data.to_csv(os.path.join(save_dir['path'], save_dir['fn']), index=False)


def crawler(url):
    temp = []
    col_names = [
        'route', 'company', 'brand', 'limitation', 'price_w', 'price_l', 'min',
        'x'
    ]
    # 线路 	物流公司 	服务品牌 	参考时效 	单价（重货） 	单价（轻货） 	最低一票 abnormal
    test = requests.get(url, headers=headers)
    test_soup = BeautifulSoup(test.text, 'html.parser')
    new = test_soup.find(
        'body', class_='layout').find(
            'div', class_='section').find(
                'div', class_='recoLine').find('table').find('tbody')

    for x in new.find_all('td'):
        if re.search('简介', x.text):
            continue
        temp.append(x.text.strip().replace('\r\n', ''))

    a = np.reshape(temp, (int(len(temp) / 8), 8))
    df = pd.DataFrame(data=a, columns=col_names)
    if not df.empty:  # 判断df是否为空，居然还会有空集，这是万万没想到的。。。
        save2csv(df)
        print('%s is ok. \n' % url)
        time.sleep(10)


def main():
    try:
        for u in sh2other:
            crawler(u)
    except Exception:
        print('error')


if __name__ == '__main__':
    main()
