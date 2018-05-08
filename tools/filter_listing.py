# ! /usr/bin/env python
# -*- coding:utf-8 -*-
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
def filter_listing():
    with mysql() as cursor:
        try:
            row_count = cursor.execute("select DISTINCT asin from listing_google_us where state = 0 and review_num >= 30 and  review_value >= 3.6 and asin not in (SELECT asin from merge_product_detail)")
            print "---------------------------ALL ASIN:"+str(row_count)+"---------------------------"
            data_asin = []
            for row in cursor.fetchall():
                    asin = row["asin"]
                    print ("{}:------------".format(datetime.datetime.now()) + asin + "----------------begin")
                    listing_info_dict, ranking_list, offering_list, review_dict_list = merge.asin_to_listing_info(asin)
                    merge.insert_data_to_mysql(listing_info_dict, "merge_product_detail")
                    merge.insert_mysql(ranking_list, "merge_product_salesrank")
                    merge.insert_mysql(offering_list, "merge_product_offer")
                    merge.insert_mysql(review_dict_list, "merge_product_review")
                    data_asin.append(asin)
            merge.update_listing_google(data_asin)
        except Exception as e:
            # os.system('start G:\911S5\ProxyTool\AutoProxyTool.exe  -changeproxy/US')
            merge.update_listing_google(data_asin)
            print("{}".format(e))

filter_listing()
