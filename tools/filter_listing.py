# ! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "TKQ"
import random

import pymysql
import contextlib
import datetime
import product_detail_merge as merge



# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='P@ssw0rd', db='amazon_db', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

# 执行sql
with mysql() as cursor:
    print(cursor)
    row_count = cursor.execute("select * from listing_google where state = 0 limit  1")
    print "----------------------------------------------------------------ALL ASIN:"+str(row_count)
    for row in cursor.fetchall():
        try:
            asin = row["asin"]
            print ("{}:------------".format(datetime.datetime.now()) + asin + "----------------begin")
            listing_info_dict, ranking_list, offering_list = merge.asin_to_listing_info(asin)
            merge.insert_data_to_mysql(listing_info_dict, "merge_product_detail")
            merge.insert_mysql(ranking_list, "merge_product_salesrank")
            merge.insert_mysql(offering_list, "merge_product_offer")
            sleep_time = random.randint(7, 100)
            print ("{}:----------------Sleep:{}".format(datetime.datetime.now(), sleep_time) + "------end")
            time.sleep(sleep_time)
        except Exception as e:
            print("Product_detail Error {}".format(e))

