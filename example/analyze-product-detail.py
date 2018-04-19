#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from amazon_module import amazon_module
import re
import random
import time
from datetime import datetime
import csv
import os

import requests

# proxy
# SOCKS5 proxy for HTTP/HTTPS
proxies = {
    'http': 'http://192.168.1.103:48850',
    'https': 'https://192.168.1.103:48850',
}

# headers
headers = {
}

url = 'https://www.amazon.com/dp/B07B8CMX26'
soup = amazon_module.download_soup_by_url(url)
# results = open('./product-detail-page-one.html', 'r')
# r = results.read()

# soup = BeautifulSoup(r, 'html.parser')
try:
    # Variations
    try:
        lis = soup.find("ul", role="radiogroup").find_all("li")
        variation_list = []
        for li in lis:
            variation_list.append(li['data-defaultasin'])
    except Exception as e:
        print("Analyze Variations Failed!: {}".format(e))
        pass

    # Salesrank
    try:
        trs = soup.find(id="productDetails_detailBullets_sections1").find_all("tr")
        for tr in trs:
            try:
                th = tr.find("th").get_text().strip()
                if th == "Best Sellers Rank":
                    spans = tr.find("span").find_all("span")
                    ranking_list = []
                    num = 0
                    for span in spans:
                        try:
                            span_text = span.get_text()
                            ranking = re.search('#(\d|,)+', span_text)
                            ranking = ranking.group()
                            ranking = ranking.replace(',', '')
                            ranking = ranking.replace('#', '')

                            rank_text_arr = span_text.split(' in ')
                            rank_text = rank_text_arr[1]
                            rank_text_arr = rank_text.split('(')
                            rank_text = rank_text_arr[0]

                            num = num + 1
                            rank_dict = {
                                "num": num,
                                "ranking": ranking,
                                "rank_text": rank_text,
                            }
                            print rank_dict
                            ranking_list.append(rank_dict)
                        except Exception as e:
                            print("Handling Salesrank string errors !: {}".format(e))
                            pass

            except Exception as e:
                print("Analyze Salesrank th Failed!: {}".format(e))
                pass
    except Exception as e:
        print("Analyze Salesrank Failed!: {}".format(e))
        pass

    # Review
    review_num = "0"
    try:
        review_num = soup.find(id="acrCustomerReviewText").get_text().split()[0].strip()
    except Exception as e:
        print("Handling review_num errors !: {}".format(e))
        pass


    review_value = "0"
    try:
        review_value = soup.find(class_="arp-rating-out-of-text").get_text().strip()
        review_value = re.search('(.*?)\s', review_value)
        review_value = review_value.group()
        review_value = review_value.strip()
        print("review_value: ", type(review_value))
    except:
        pass

    review_value_and_star = review_num + "/" + review_value
    print(review_value_and_star)

    # re.compile来匹配需要抓取的href地址
    try:
        follow = soup.find_all(href=re.compile("/gp/offer-listing"))
        follow_sell = follow[0].get_text()
        follow_sell = follow_sell.split('(')
        follow_type = follow_sell[0].strip()
        follow_num = follow_sell[1].split(')')
        buy_money = follow_num[1].split('$')
        buy_money = buy_money[1].strip()
        follow_num = follow_num[0].strip()

    except Exception as e:
        print("Handling follow_sell errors !: {}".format(e))
        pass

    store_salesrank_and_review_star_dict = {
        "asin": "B079LDM5XM",
        "review_value_and_star": review_value_and_star,
    }

except Exception as e:
    print("fail to convert!: {}".format(e))
