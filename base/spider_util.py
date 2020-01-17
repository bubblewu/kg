#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : spider_util.py
# @Author: wu gang
# @Date  : 2019-12-05
# @Desc  : 爬虫工具
# @Contact: 752820344@qq.com

import random
import time
from urllib import request

import numpy as np
import requests
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control": "no-cache",
    # "Cookie": ""
}


def get_ip_list():
    """
    获取动态代理IP（只获取了该网页的部分）
    :return: 代理IP
    """
    print("正在获取代理列表...")
    url = 'http://www.xicidaili.com/nn/'
    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    ips = soup.find(id='ip_list').find_all('tr')
    ip_list = list()
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    print("代理列表抓取成功, count: %d" % len(ip_list))
    return ip_list


def get_random_ip(ip_list):
    # print("正在设置随机代理...")
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    print("代理设置成功：%s" % proxies)
    return proxies


def download(url, encoding="utf-8", use_proxy=True):
    print("start download: %s" % url)
    time.sleep(np.random.rand() * 5)
    if use_proxy:
        ip_list = get_ip_list()
        proxy_handler = request.ProxyHandler(get_random_ip(ip_list))
        opener = request.build_opener(proxy_handler)
        req = request.Request(url, headers=headers)
        html = opener.open(req).read()
    else:
        req = request.Request(url, headers=headers)
        html = request.urlopen(req).read()
    html = str(html, encoding=encoding)
    return html


def download_requests(url, encoding="utf-8", use_proxy=True):
    print("start download: %s" % url)
    time.sleep(np.random.rand() * 5)
    if use_proxy:
        ip_list = get_ip_list()
        response = requests.get(url, headers=headers, proxies=get_random_ip(ip_list))
        response.encoding = encoding
        return response.text
    else:
        response = requests.get(url, headers=headers)
        response.encoding = encoding
        return response.text
