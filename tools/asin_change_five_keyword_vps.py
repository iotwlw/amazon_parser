# ! /usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import contextlib
import time
import datetime

import re

import product_detail_merge as merge


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='P@ssw0rd', db='amazon_db2', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


# 执行sql
def filter_listing():
    with mysql() as cursor:
        row_count = cursor.execute("SELECT DISTINCT  url from listing_google_us where url is not null and review_num >= 100 and  review_value >= 4 and insert_datetime < '2018-09-16'")
        print "---------------------------ALL ASIN URL :"+str(row_count)+"---------------------------"
        inxxxx = 0
        for row in cursor.fetchall():
                inxxxx = inxxxx + 1
                url = row["url"]
                print (str(inxxxx)+':'+url)
                five_key_list = []
                try:
                    names = re.findall(r'/(\w*)(?=-)|-(\w*)\b', url)
                    if names:
                        for group in names:
                            key_word = ''.join(group)
                            five_key = {
                                "key_big": "ASIN",
                                "key_word": key_word
                            }
                            five_key_list.append(five_key)
                    merge.insert_mysql(five_key_list, "key_word_us")
                    # update_change_over(asin)
                except Exception as e:
                    print("{}".format(e))


filter_listing()
