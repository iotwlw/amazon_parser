# coding:utf-8
import contextlib
import os
import random

import chardet
import pymysql
import requests
import time

from requests.exceptions import ProxyError

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

class ProxyControl:
    """
    Magic google search.
    """

    def __init__(self, proxies=None):
        self.proxies = {'https': 'https://218.60.8.98:3129' }

    # 定义上下文管理器，连接后自动关闭连接
    @contextlib.contextmanager
    def mysql(self, host='127.0.0.1', port=3306, user='root', passwd='P@ssw0rd', db='amazon_db', charset='utf8'):
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            yield cursor
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    def detect_proxy(self):
        with self.mysql() as cursor:
            try:
                cursor.execute("SELECT * from proxys where score > 6 and (last_use is null or last_use < date_sub(now(), interval 2 hour)) ORDER by score desc limit 100 ")
                print "---------------------------detect_proxy---------------------------"
                for proxy in cursor.fetchall():
                    ip = proxy['ip']
                    port = proxy['port']
                    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
                    protocol, types, speed = self.amazon_check(proxies)
                    if protocol >= 0:
                        proxy['speed'] = speed
                        if proxy['score'] and proxy['score'] < 10:
                            proxy['score'] = proxy['score'] + 1
                        self.update_proxy(proxy, cursor)
                        self.proxies = proxies
                        return proxies
                    else:
                        proxy['score'] = proxy['score'] - 1
                        self.update_proxy(proxy, cursor)
                raise ProxyError

            except Exception as e:
                # update_listing_google(data_asin)
                print("--------------------------detect_proxy error---------------------------{}".format(e))
                raise Exception

    def amazon_check(self, proxies):
        try:
            start = time.time()
            headers = {'user-agent': self.get_random_user_agent()}
            r = requests.get(url='https://www.amazon.com', headers=headers, proxies=proxies, timeout=30)
            r.encoding = chardet.detect(r.content)['encoding']
            if r.ok and len(r.content) > 500 and ("Robot Check" not in r.content):
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

    def get_random_user_agent(self):
        """
        Get a random user agent string.
        :return: Random user agent string.
        """
        return random.choice(self.get_data('user_agents.txt', USER_AGENT))

    def get_data(self, filename, default=''):
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

    def update_proxy(self, proxy, cursor):
        update_sql = "UPDATE proxys set score = '%(score)s',speed = '%(speed)s'  where ip = '%(ip)s' and port = '%(port)s'" % proxy
        print update_sql
        try:
            row_count = cursor.execute(update_sql)
            print("UPDATE proxy {} success:", row_count)
        except Exception as e:
            print("UPDATE proxy errors:{}".format(e), proxy)



