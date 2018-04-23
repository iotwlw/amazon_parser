# ! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "Quan"
import contextlib
import datetime
import pymysql
import random

from amazon_module import amazon_module
import re
import time


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


def asin_to_listing_info(asin):
    now = int(time.time())
    print("asin: ", asin)
    url = "https://www.amazon.com/dp/" + asin
    soup = amazon_module.download_soup_by_url(url)
    print(len(soup))

    brand = " "
    try:
        if soup.find(id="bylineInfo"):
            brand = soup.find(id="bylineInfo").get_text().strip()
        if soup.find(id="brand"):
            brand = soup.find(id="brand").get_text().strip()
    except:
        pass
    print("brand:", brand)

    title = ""
    try:
        if soup.find(id="productTitle"):
            title = soup.find(id="productTitle").get_text().strip()
    except:
        pass
    print("title:", title)

    variation_name = " "
    try:
        if soup.find(id="variation_pattern_name"):
            variation_name = soup.find(id="variation_pattern_name").find("span").get_text().strip()
            print("variation_pattern_name: ", variation_name)
        elif soup.find(id="variation_color_name"):
            variation_name = soup.find(id="variation_color_name").find("span").get_text().strip()
            print("variation_color_name: ", variation_name)
        elif soup.find(id="variation_size_name"):
            variation_name = soup.find(id="variation_size_name").find("span").get_text().strip()
            print("variation_size_name: ", variation_name)
        else:
            print("variation_name: ", variation_name)
    except:
        pass

    price = " "
    try:
        if soup.find(id="price"):
            price = soup.find(id="price").find("span").get_text().replace('$', '').strip()
        if soup.find(id="priceblock_ourprice"):
            price = soup.find(id="priceblock_ourprice").get_text().replace('$', '').strip()
    except:
        pass
    print("price:", price)

    sold_by = " "
    try:
        if soup.find(id="merchant-info"):
            sold_by = " ".join(soup.find(id="merchant-info").get_text().strip().split())
    except:
        pass
    print("sold_by:", sold_by)

    availability = ""
    try:
        if soup.find(id="availability"):
            availability = soup.find(id="availability").find("span").get_text().strip()
    except:
        pass
    print("availability:", availability)

    aplus = ""
    try:
        if soup.find(id="aplus"):
            aplus = soup.find(id="aplus").find("h2").get_text().strip()
    except:
        pass
    print("availability:", aplus)

    ranking_list = []
    offering_list = []
    spans_text = ""

    review_dict_list = []
    review_last_time = ""

    # Salesrank
    try:
        trs = soup.find(id="productDetails_detailBullets_sections1").find_all("tr")
        for tr in trs:
            try:
                th = tr.find("th").get_text().strip()
                if th == "Best Sellers Rank":
                    spans = tr.find("span").find_all("span")
                    num = 0
                    for span in spans:
                        try:
                            span_text = span.get_text()
                            spans_text = spans_text + span_text + "\n"
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
                                "detail_id": now,
                                "rank_num": num,
                                "rank_asin": asin,
                                "rank_order": ranking,
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

    review_num = " "
    try:
        if soup.find(id="acrCustomerReviewText"):
            review_num = soup.find(id="acrCustomerReviewText").get_text().split()[0].strip()
    except:
        pass
    print("review_num:", review_num)

    review_value = " "
    try:
        if soup.find(class_="arp-rating-out-of-text"):
            review_value = soup.find(class_="arp-rating-out-of-text").get_text().strip()
            review_value = re.search('(.*?)\s', review_value)
            review_value = review_value.group()
            review_value = review_value.strip()
    except:
        pass
    print("review_value:", review_value)

    qa_num = " "
    try:
        if soup.find(id="askATFLink"):
            qa_num = soup.find(id="askATFLink").get_text().split()[0].strip()
    except:
        pass
    print("qa_num:", qa_num)


    try:
        review_list = soup.find(id="most-recent-reviews-content").find_all("div", {"data-hook": "recent-review"})

        for review_index, review in enumerate(review_list):
            review_title = review.find("span", {"data-hook": "review-title-recent"}).get_text()
            review_star_rating = review.find("i", {"data-hook": "review-star-rating-recent"}).get_text()
            review_author_url = review.find("a", {"class": "a-profile"})["href"]
            review_author = review.find("span", {"class": "a-profile-name"}).get_text()
            review_date = review.find("span", {"data-hook": "review-author-timestamp"}).get_text()
            if review_index == 0:
                review_last_time = review_date
            review_body = review.find("span", {"data-hook": "review-body-recent"}).get_text()
            review_dict = {
                           "review_asin": asin,
                           "review_title": review_title,
                           "review_star": review_star_rating.rstrip(" out of 5 stars"),
                           "review_author": review_author,
                           "review_author_url": review_author_url,
                           "review_date": review_date,
                           "review_body": review_body,
                           }
            print(review_dict)
            review_dict_list.append(review_dict)
    except Exception as e:
        print "analyze review error:{}".format(e)
        pass

    # follow_sell
    how_many_sellers = ""
    follow_type = ""
    follow_num = 0
    buy_money = ""

    try:
        if soup.find(id="olp_feature_div"):
            how_many_sellers = soup.find(id="olp_feature_div").find("a").get_text().strip()
            follow_sell = how_many_sellers.split('(')
            follow_type = follow_sell[0].strip()
            follow_num = follow_sell[1].split(')')
            buy_money = follow_num[1].split('$')
            buy_money = buy_money[1].strip()
            follow_num = follow_num[0].strip()

    except Exception as e:
        print("Handling follow_sell errors !: {}".format(e))
        pass

    except Exception as e:
        print("Handling follow_sell errors !: {}".format(e))
        pass

    listing_info_dict = {
        "id": now,
        "asin": asin,
        "url": url,
        "brand": brand,
        "title": title,
        "variation_name": variation_name,
        "price": price,
        "sold_by": sold_by,
        "how_many_sellers": how_many_sellers,
        "follow_type": follow_type,
        "follow_num": follow_num,
        "buy_money": buy_money,
        "review_num": review_num,
        "review_value": review_value,
        "review_last_time": review_last_time,
        "spans_text": spans_text,
        "qa_num": qa_num,
    }

    return listing_info_dict, ranking_list, offering_list

def insert_data_to_mysql(asin_dict, table_name, conn):
    print("insert_data_to_mysql")
    try:
        try:
            id = asin_dict["id"]
            id = pymysql.escape_string(id)
        except:
            pass
        try:
            asin = asin_dict["asin"]
            asin = pymysql.escape_string(asin)
        except:
            pass
        try:
            url = asin_dict["url"]
            url = pymysql.escape_string(url)
        except:
            pass
        try:
            brand = asin_dict["brand"]
            brand = pymysql.escape_string(brand)
        except:
            pass
        try:
            title = asin_dict["title"]
            title = pymysql.escape_string(title)
        except:
            pass
        try:
            variation_name = asin_dict["variation_name"]
            variation_name = " ".join(variation_name.split())
            variation_name = pymysql.escape_string(variation_name)
            print(variation_name)
        except:
            pass
        try:
            price = asin_dict["price"]
            price = pymysql.escape_float(price)
        except:
            pass
        try:
            sold_by = asin_dict["sold_by"]
            sold_by = pymysql.escape_string(sold_by)
        except:
            pass
        try:
            how_many_sellers = asin_dict["how_many_sellers"]
            how_many_sellers = pymysql.escape_string(how_many_sellers)
        except:
            pass
        try:
            follow_type = asin_dict["follow_type"]
            follow_type = pymysql.escape_string(follow_type)
        except:
            pass
        try:
            follow_num = asin_dict["follow_num"]
            follow_num = pymysql.escape_int(follow_num)
        except:
            pass
        try:
            buy_money = asin_dict["buy_money"]
            buy_money = pymysql.escape_float(buy_money)
        except:
            pass

        try:
            review_num = asin_dict["review_num"]
            review_num = pymysql.escape_string(review_num)
        except:
            pass
        try:
            review_value =asin_dict["review_value"]
            review_value = pymysql.escape_float(review_value)
        except:
            pass
        try:
            spans_text = asin_dict["spans_text"]
            spans_text = pymysql.escape_string(spans_text)
        except:
            pass
        try:
            qa_num = asin_dict["qa_num"]
        except:
            pass

        try:
            insert_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_datetime = str(insert_datetime)
            print("insert_datetime: ", insert_datetime)

            with mysql() as cursor:
                insert_into_sql = "INSERT INTO " + table_name + " (id, asin, insert_datetime, url, brand, title, variation_name, price, sold_by, how_many_sellers, review_num, review_value, qa_num,follow_type,follow_num,buy_money,spans_text) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') "
                data = (id, asin, insert_datetime, url, brand, title, variation_name, price, sold_by, how_many_sellers, review_num, review_value, qa_num,follow_type,follow_num,buy_money,spans_text)
                cursor.execute(insert_into_sql % data )
                print("success to insert asin_dict to mysql")
        except:
            print("fail to insert asin_dict to mysql!")
    except:
        print("fail to insert asin_dict to mysql!!")


def insert_mysql(offer_dict_list, table_name, conn):
    insert_into_sql = "INSERT INTO " + table_name + "("
    insert_into_sql_s = ""
    datas = []
    try:
        if offer_dict_list[0]:
            keys = offer_dict_list[0].keys()
            for j in keys:
                insert_into_sql = insert_into_sql + j+","
                insert_into_sql_s = insert_into_sql_s + "%s,"
            insert_into_sql = insert_into_sql.rstrip(",") + ") VALUES (" + insert_into_sql_s.rstrip(',') + ")"
            print insert_into_sql

    except Exception as e:
        print("FAIL to insert_into_sql {}".format(e))

    try:
        for i in offer_dict_list:
            data = tuple(i.values())
            datas.append(data)
            print datas
    except Exception as e:
        print("FAIL to insert_into_data {}".format(e))

    try:
        with mysql() as cursor:
            cursor.executemany(insert_into_sql, datas)
            print("success to insert asin_dict to mysql")
    except Exception as e:
        print("fail to insert asin_dict to mysql!{}".format(e))
