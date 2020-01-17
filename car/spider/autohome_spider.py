#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : autohome_spider.py
# @Author: wu gang
# @Date  : 2020-01-15
# @Desc  : 汽车品牌和车系获取(汽车之家)
# @Contact: 752820344@qq.com

import base.spider_util as su
from bs4 import BeautifulSoup
import numpy as np
import time


def save(data_list, file):
    with open(file, mode="w", encoding="UTF-8") as w:
        for line in data_list:
            w.write(line + "\n")
    print("save info successfully: %s" % file)


def get_brands():
    data_list = list()
    # 品牌名、车型数量、地址
    data_list.append("brand,car_count,url")
    url = "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1&brandId=0&fctId=0&seriesId=0"
    html = su.download_requests(url, encoding="gb2312", use_proxy=False)
    html = html.replace("document.writeln(\"", "").replace("\")", "")
    soup = BeautifulSoup(html, features="lxml")
    # print(soup.prettify())
    brand_list = soup.select("ul li h3 a")
    for b in brand_list:
        data = b.text
        start_index = data.find("(")
        end_index = data.find(")")
        brand = data[0:start_index]
        num = data[start_index + 1:end_index]
        brand_url = base_url + b['href']
        data_list.append(brand + "," + num + "," + brand_url)
    return data_list


def get_series(brand_file):
    data_list = list()
    data_list.append("brand,type,type_url,car_type,series,url")
    with open(brand_file, mode="r") as r:
        for line in r.readlines():
            if "brand,car_count,url" in line:
                continue
            line = line.replace("\n", "")
            lines = line.split(",")
            brand = lines[0]
            brand_url = lines[2]
            html = su.download_requests(brand_url, encoding="gb2312", use_proxy=False)
            # html = html.replace("document.writeln(\"", "").replace("\")", "")
            soup = BeautifulSoup(html, features="lxml")
            # print(soup.prettify())
            series_list = soup.select("div.carbradn-cont.fn-clear dl.list-dl")
            for s in series_list:
                types = s.find("dt").find("a")
                tp = types.text
                type_url = types['href']
                car_type_list = s.select("dd div")
                list_size = len(car_type_list)
                for i in range(int(list_size / 2)):
                    # car_type_ = car_type_list[i].find(name="div", attrs={"class": "list-dl-name"})
                    # car_type_ = car_type_list[i].text
                    i = i * 2
                    car_type = car_type_list[i].text.replace("：", "")
                    i += 1
                    s_list = car_type_list[i].select("div.list-dl-text a")
                    for s in s_list:
                        series = s.text
                        series_url = base_url + s['href']
                        data_list.append(
                            brand + "," + tp + "," + type_url + "," + car_type + "," + series + "," + series_url
                        )
            time.sleep(np.random.rand() * 5)
    return data_list


def start():
    # 获取品牌信息
    data_list = get_brands()
    brand_file = "../../input/car/brand.csv"
    save(data_list, brand_file)
    # 获取品牌下的车系信息
    series_file = "../../input/car/brand_series.csv"
    series_list = get_series(brand_file)
    save(series_list, series_file)


if __name__ == '__main__':
    base_url = "https://car.autohome.com.cn/"
    # start()
    html = su.download_requests("https://car.autohome.com.cn/price/brand-33.html", encoding="gb2312", use_proxy=False)
    html = html.replace("document.writeln(\"", "").replace("\")", "")
    soup = BeautifulSoup(html, features="lxml")
    print(soup.prettify())
