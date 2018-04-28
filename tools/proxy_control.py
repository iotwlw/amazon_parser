# coding:utf-8
import contextlib
import os
import random

import chardet
import pymysql
import requests
import time

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'


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


def detect_proxy():
    with mysql() as cursor:
        try:
            cursor.execute("SELECT * from proxys where score > 7 and last_use < date_sub(now(), interval 1 hour)")
            print "---------------------------detect_proxy---------------------------"
            for proxy in cursor.fetchall():
                ip = proxy['ip']
                port = proxy['port']
                proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
                protocol, types, speed = amazon_check(proxies)
                if protocol >= 0:
                    proxy['speed'] = speed
                    if proxy['score'] and proxy['score'] < 10:
                        proxy['score'] = proxy['score'] + 1
                    return proxy
                else:
                    proxy['score'] = proxy['score'] - 1
                    return None

        except Exception as e:
            # os.system('start G:\911S5\ProxyTool\AutoProxyTool.exe  -changeproxy/US')
            # update_listing_google(data_asin)
            print("--------------------------detect_proxy error---------------------------{}".format(e))
            return None


def amazon_check(proxies):
    try:
        start = time.time()
        headers = {'user-agent': get_random_user_agent()}
        r = requests.get(url='https://www.amazon.co.uk', headers=headers, proxies=proxies)
        r.encoding = chardet.detect(r.content)['encoding']
        if r.ok and len(r.content) > 500:
            speed = round(time.time() - start, 2)
            protocol = 3
            types = 0

        else:
            speed = -1
            protocol = -1
            types = -1
    except Exception as e:
        print ("------------check to amazon error {}".format(e))
        speed = -1
        protocol = -1
        types = -1
    return protocol, types, speed


def get_random_user_agent():
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    return random.choice(get_data('user_agents.txt', USER_AGENT))


def get_data(filename, default=''):
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(
        os.path.join(root_folder, '../res'), filename)
    try:
        with open(user_agents_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except Exception as e:
        print ("----------choice user agent error {}".format(e))
        data = [default]
    return data


def update_listing_google(data_asins):
    # state: 0  insert data
    #        -1 error data
    #        2  handled by Amazon program
    #        11 first filter by under 30 review_num and under 4.0 review_value
    update_sql = "UPDATE listing_google set state = 2 where asin = %s"

    try:
        with mysql() as cursor:
            row_count = cursor.executemany(update_sql, data_asins)
            print("UPDATE listing_google {}/{} success:", row_count, len(data_asins))
    except Exception as e:
        print("UPDATE listing_google errors:{}".format(e), data_asins)


if __name__ == '__main__':
    aaa = get_random_user_agent()
    print aaa
