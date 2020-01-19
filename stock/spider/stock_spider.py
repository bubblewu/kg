#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : stock_spider.py
# @Author: wu gang
# @Date  : 2020-01-17
# @Desc  : 同花顺上股票信息抓取
# @Contact: 752820344@qq.com
import base.spider_util as su
from bs4 import BeautifulSoup


def get_html(url):
    html = su.download_requests(url, encoding="gbk", use_proxy=False)
    soup = BeautifulSoup(html, features="lxml")
    # print(soup.prettify())
    return soup


def get_total_page(url):
    soup = get_html(url)
    page_info = soup.find(name="span", attrs={"class": "page_info"})
    total_page = page_info.text[2:]  # 1/186
    print("总共%s页" % total_page)
    return total_page


def start():
    base_url = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{page}/ajax/1/"
    total_page = get_total_page(base_url.format(page=1))
    for i in range(int(total_page)):
        i = i + 1
        print(base_url.format(page=i))


if __name__ == '__main__':
    start()


