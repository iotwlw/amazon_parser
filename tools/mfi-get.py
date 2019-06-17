# ! /usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import contextlib
import requests
import json
url1 = 'https://mfi.apple.com/MFiWeb/getAPS.action'
url2 = 'https://mfi.apple.com/MFiWeb/getApprovedProducts.action'


import product_detail_merge as merge

# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='P@ssw0rd', db='mfi', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


# 执行sql
def split_company_name():
    with mysql() as cursor:
        row_count = cursor.execute("SELECT id, company_name from mfi_company  where country = 'china';")
        print "---------------------------ALL Company URL :"+str(row_count)+"---------------------------"
        inxxxx = 0
        for row in cursor.fetchall():
            try:
                inxxxx = inxxxx + 1
                id = row["id"]
                company_name = row["company_name"]
                print (str(inxxxx)+':'+company_name)
                key_list = company_name.split( )
                five_key_list = []

                for item in key_list:
                    if item:
                        five_key = {
                            "mfi_id": id,
                            "company_name": company_name,
                            "company_key": item,
                            "state": '0'
                        }
                    five_key_list.append(five_key)
                insert_mysql(five_key_list, "mfi_company_key")
            except Exception as e:
                print("{}".format(e))


def serch_mfi_from_apple():
    with mysql() as cursor:
        row_count = cursor.execute("SELECT company_key from (SELECT company_key,count(company_key) as num  from mfi_company_key  where company_key not like '%有限公司%' GROUP BY company_key) b where b.num = 1;")
        print "---------------------------ALL company_key :" + str(row_count) + "---------------------------"
        r = requests.post(url1)
        cookies = r.cookies.get_dict()
        headers = {'Content-Type': 'application/json'}
        for row in cursor.fetchall():
            company_key = row["company_key"]
            mydata = {'brand': company_key}
            r2 = requests.post(url2, headers=headers, data=json.dumps(mydata), cookies=cookies)
            data = r2.content
            j = json.loads(data)
            result_list = j['resultList']
            if result_list:
                result_list3 = result_list[0]
                result_list2 = result_list3['returnList']
                insert_mysql(result_list2, "mfi_company_record")



def insert_mysql(offer_dict_list, table_name):
    insert_into_sql = "INSERT INTO " + table_name + "("
    insert_into_sql_s = ""
    datas = []
    try:
        if offer_dict_list and offer_dict_list[0]:
            keys = offer_dict_list[0].keys()
            for j in keys:
                insert_into_sql = insert_into_sql + j + ","
                insert_into_sql_s = insert_into_sql_s + "%s,"
            insert_into_sql = insert_into_sql.rstrip(",") + ") VALUES (" + insert_into_sql_s.rstrip(',') + ")"
            # print insert_into_sql
        else:
            return
    except Exception as e:
        print("Splicing insert_into_" + table_name + "_sql errors:{}".format(e))

    try:
        for i in offer_dict_list:
            data = tuple(i.values())
            datas.append(data)
    except Exception as e:
        print("Splicing insert_into_" + table_name + "_data errors:{}".format(e))

    try:
        with mysql() as cursor:
            cursor.executemany(insert_into_sql, datas)
    except Exception as e:
        print("INSERT " + table_name + " errors:{}".format(e), datas)


serch_mfi_from_apple()
