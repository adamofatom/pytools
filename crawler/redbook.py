import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
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


def rb_crawler(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }
    if url.find("user"):
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        user_name.append(soup.find(class_="user-name").text)
        link.append(url)
        follows.append(soup.find(class_="follows-num").text)
        fans.append(soup.find(class_="fans-num").text)
        likes.append(soup.find(class_="liked-num").text)
        notes.append(
            int(
                soup.find(
                    class_="cube-tab-item active").find("small").text.replace(
                        "·", "")))
    else:
        print(url + " 链接有误")


for url in df:
    rb_crawler(url)
    time.sleep(5)
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
