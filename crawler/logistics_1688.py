import os
import re
import time
import csv
import requests
from bs4 import BeautifulSoup 

url = 'http://56.1688.com/routes/shanghai.htm'  # 阿里巴巴物流上海线路
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}  # 构造头部
# # cookie = {}
# # pxs = {}  # TODO 代理池
# r = requests.get(url, headers=headers)
# soup = BeautifulSoup(r.text, 'html.parser')
# sh2other = []  # 上海到其他城市转接列表
# for x in soup.find_all(href=re.compile('.htm'), title=re.compile('上海')):
#     sh2other.append(x['href'])

# sh2other = sh2other[1:]  # 删除无用链接
# # print(sh2other)  # 测试用
# test = requests.get(sh2other[0].replace('//', 'http://', 1), headers=headers)

col_names_cn = ['routes', 'company', 'brand', 'limitation', 'price_w', 'price_l', 'min']
# 线路 	物流公司 	服务品牌 	参考时效 	单价（重货） 	单价（轻货） 	最低一票 	操作
test = requests.get('http://56.1688.com/routes/shanghai-beijing.htm', headers=headers)
test_soup = BeautifulSoup(test.text, 'html.parser')
new = test_soup.find('body', class_='layout').find('div', class_='section').find('div', class_='recoLine').find('table').find('tbody')
print(new)
