#!/usr/bin/env python
# encoding=utf-8
"""
爬取豆瓣图书TOP250 - 完整示例代码
"""
import os
import codecs
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://book.douban.com/top250/'


def download_page(url):
    return requests.get(
        url,
        headers={
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }).content


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    book_list_soup = soup.find('div', attrs={'class': 'indent'})

    book_name_list = []

    for book_li in book_list_soup.find_all('table'):
        detail = book_li.find('div', attrs={'class': 'pl2'})
        book_name = detail.find('a').get_text(strip=True)

        book_name_list.append(book_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return book_name_list, next_page['href']
    return book_name_list, None


def main():
    url = DOWNLOAD_URL
    save_dir = {
        'path':
        os.path.join(
            os.path.dirname(__file__).replace(
                os.path.dirname(__file__), 'dataset')),
        'filename':
        'dbbooks'
    }
    # TODO 调整存储文本
    with codecs.open(
            os.path.join(save_dir['path'], save_dir['filename']),
            'wb',
            encoding='utf-8') as fp:
        print(os.getcwd())
        while url:
            html = download_page(url)
            books, url = parse_html(html)
            fp.write(u'{books}\n'.format(books='\n'.join(books)))


if __name__ == '__main__':
    main()
