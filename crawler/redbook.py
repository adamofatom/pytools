import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


url = 'http://www.xicidaili.com/nn/'
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
ip_list = get_ip_list(url, headers=headers)
proxies = get_random_ip(ip_list)

file1 = r"d:\Adam\redbook1.xls"
file2 = r"d:\Adam\redbook2.xlsx"
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)
df1.iloc[:, 2]
df2.iloc[:, 2]
df = pd.concat([df1.iloc[:, 2], df2.iloc[:, 2]], ignore_index=True)
d = {}

user_name = []
link = []
follows = []
fans = []
likes = []
notes = []

s = requests.session()
s.keep_alive = False


def rb_crawler(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }
    if url.find("user"):
        try:
            r = requests.get(url, headers=headers, proxies=proxies)
            soup = BeautifulSoup(r.text, 'html.parser')
            user_name.append(soup.find(class_="user-name").text)
            link.append(url)
            follows.append(soup.find(class_="follows-num").text)
            fans.append(soup.find(class_="fans-num").text)
            likes.append(soup.find(class_="liked-num").text)
            notes.append(
                int(
                    soup.find(class_="cube-tab-item active").find("small")
                    .text.replace("·", "")))
        except requests.exceptions.ConnectionError:
            print("Connection refused")

    else:
        print(url + " 链接有误")


for url in df:
    rb_crawler(url)
    time.sleep(2)
    print(url + "已完成")

d["name"] = user_name
d["link"] = link
d["follows"] = follows
d["fans"] = fans
d["likes"] = likes
d["notes"] = notes

df = pd.DataFrame(data=d)
if __name__ == "__main__":
    df.to_excel(r"d:\Adam\rbresult.xlsx")
