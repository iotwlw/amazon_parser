# ! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "Quan"
import contextlib
import datetime
import pymysql

from amazon_module import amazon_module
import re
import time


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


def asin_to_listing_info(asin, country=None):
    now = int(time.time())
    # print("asin: ", asin)
    url = "https://www.amazon.com/dp/" + asin
    if country:
        url = "https://www.amazon.co.uk/dp/" + asin
    soup = amazon_module.download_soup_by_url(url)

    brand = " "
    brand_url = ""
    try:
        if soup.find(id="bylineInfo"):
            brand = soup.find(id="bylineInfo").get_text().strip()
            brand_url = soup.find(id="bylineInfo")["href"]
        if soup.find(id="brand"):
            brand = soup.find(id="brand").get_text().strip()
    except:
        pass

    title = ""
    try:
        if soup.find(id="productTitle"):
            title = soup.find(id="productTitle").get_text().strip()
    except:
        pass

    variation_name = " "
    try:
        if soup.find(id="variation_pattern_name"):
            variation_name = soup.find(id="variation_pattern_name").find("span").get_text().strip()
        elif soup.find(id="variation_color_name"):
            variation_name = soup.find(id="variation_color_name").find("span").get_text().strip()
        elif soup.find(id="variation_size_name"):
            variation_name = soup.find(id="variation_size_name").find("span").get_text().strip()
    except:
        pass

    price = 0.0
    try:
        if soup.find(id="price"):
            price = soup.find(id="price").find("span").get_text()
            price = re.search('(\d*\.\d*)', price)
            price = price.group()
        if soup.find(id="priceblock_ourprice"):
            price = soup.find(id="priceblock_ourprice").get_text()
            price = re.search('(\d*\.\d*)', price)
            price = price.group()
    except:
        pass

    sold_by = " "
    try:
        if soup.find(id="merchant-info"):
            sold_by = " ".join(soup.find(id="merchant-info").get_text().strip().split())
    except:
        pass

    availability = ""
    try:
        if soup.find(id="availability"):
            availability = soup.find(id="availability").find("span").get_text().strip()
    except:
        pass

    aplus = ""
    try:
        if soup.find(id="aplus"):
            aplus = soup.find(id="aplus").find("h2").get_text().strip()
    except:
        pass

    ranking_list = []
    offering_list = []
    spans_text = ""

    review_dict_list = []
    review_last_desc = ""
    review_last_time = 0
    review_last_unit = ""

    # Salesrank
    try:
        trs = soup.find(id="productDetails_detailBullets_sections1")
        if trs:
            trs = trs.find_all("tr")
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
                                ranking_list.append(rank_dict)
                            except Exception as e:
                                print("Handling Salesrank string errors !: {}".format(e))
                                pass

                except Exception as e:
                    print("Analyze Salesrank th errors!: {}".format(e))
                    pass
    except Exception as e:
        print("Analyze Salesrank errors!: {}".format(e))
        pass

    review_num = 0
    try:
        if soup.find(id="acrCustomerReviewText"):
            review_num = soup.find(id="acrCustomerReviewText").get_text().split()[0].strip(",").strip().replace(',', '')
    except:
        pass

    review_value = 0.0
    try:
        if soup.find(class_="arp-rating-out-of-text"):
            review_value = soup.find(class_="arp-rating-out-of-text").get_text().strip()
            review_value = re.search('(.*?)\s', review_value)
            review_value = review_value.group()
            review_value = review_value.strip()
    except:
        pass

    qa_num = 0
    try:
        if soup.find(id="askATFLink"):
            qa_num = soup.find(id="askATFLink").get_text().split()[0].strip()
    except:
        pass

    try:
        review_list = soup.find(id="most-recent-reviews-content")
        if review_list and review_list.find_all("div", {"data-hook": "recent-review"}):
            review_list = review_list.find_all("div", {"data-hook": "recent-review"})
            for review_index, review in enumerate(review_list):
                review_title = review.find("span", {"data-hook": "review-title-recent"}).get_text()
                review_star_rating = review.find("i", {"data-hook": "review-star-rating-recent"}).get_text()
                review_author_url = review.find("a", {"class": "a-profile"})["href"]
                review_author = review.find("span", {"class": "a-profile-name"}).get_text()
                review_date_desc = review.find("span", {"data-hook": "review-author-timestamp"}).get_text()
                review_body = review.find("span", {"data-hook": "review-body-recent"}).get_text()
                review_date_desc_temp = review_date_desc.lstrip('Published ').rstrip(' ago')
                if 'on ' in review_date_desc_temp:
                    review_date = '2'
                    review_date_unit = 'year'
                else:
                    review_date_desc_arr = review_date_desc_temp.split(' ')
                    review_date = review_date_desc_arr[0]
                    review_date_unit = review_date_desc_arr[1].rstrip('s')
                #TODO:
                if review_index == 0:
                    review_last_desc = review_date_desc
                    review_last_time = review_date
                    review_last_unit = review_date_unit
                review_dict = {
                    "review_asin": asin,
                    "review_title": review_title,
                    "review_star": review_star_rating.rstrip(" out of 5 stars"),
                    "review_author": review_author,
                    "review_author_url": review_author_url,
                    "review_date": review_date,
                    "review_date_unit": review_date_unit,
                    "review_date_desc": review_date_desc,
                    "review_body": review_body,
                }
                review_dict_list.append(review_dict)
    except Exception as e:
        print "analyze review errors:{}".format(e)
        pass

    # follow_sell
    how_many_sellers = ""
    follow_type = ""
    follow_num = 0
    buy_money = 0.0

    try:
        olp_feature_div = soup.find(id="olp_feature_div")
        if olp_feature_div and olp_feature_div.find("a"):
            how_many_sellers = olp_feature_div.find("a").get_text().strip()
            if country:
                follow_sell = how_many_sellers.split()
                follow_num = follow_sell[0].strip()
                follow_type = follow_sell[1].strip()
            else:
                follow_sell = how_many_sellers.split('(')
                follow_type = follow_sell[0].strip()
                follow_num = follow_sell[1].split(')')
                buy_money = follow_num[1].split('$')
                buy_money = buy_money[1].strip().replace(',', '').rstrip(' +')
                follow_num = follow_num[0].strip()

    except Exception as e:
        print("Handling follow_sell errors !: {}".format(e))
        pass

    listing_info_dict = {
        "id": now,
        "asin": asin,
        "url": url,
        "brand": brand,
        "brand_url": brand_url,
        "title": title,
        "variation_name": variation_name,
        "availability": availability,
        "price": price,
        "sold_by": sold_by,
        "how_many_sellers": how_many_sellers,
        "follow_type": follow_type,
        "follow_num": follow_num,
        "buy_money": buy_money,
        "review_num": review_num,
        "review_value": review_value,
        "review_last_time": review_last_time,
        "review_last_unit": review_last_unit,
        "review_last_desc": review_last_desc,
        "spans_text": spans_text,
        "qa_num": qa_num,
        "aplus": aplus,
    }

    return listing_info_dict, ranking_list, offering_list, review_dict_list


def insert_data_to_mysql(asin_dict, table_name):
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
        except:
            pass

        try:
            availability = asin_dict["availability"]
            availability = pymysql.escape_string(availability)
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
            review_num = pymysql.escape_int(review_num)
        except:
            pass
        try:
            review_value = asin_dict["review_value"]
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
            review_last_time = asin_dict["review_last_time"]
            review_last_time = pymysql.escape_int(review_last_time)
        except:
            pass
        try:
            review_last_unit = asin_dict["review_last_unit"]
            review_last_unit = pymysql.escape_string(review_last_unit)
        except:
            pass
        try:
            review_last_desc = asin_dict["review_last_desc"]
            review_last_desc = pymysql.escape_string(review_last_desc)
        except:
            pass
        try:
            aplus = asin_dict["aplus"]
            aplus = pymysql.escape_string(aplus)
        except:
            pass
        try:
            brand_url = asin_dict["brand_url"]
            brand_url = pymysql.escape_string(brand_url)
        except:
            pass

        data = ()
        try:
            insert_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_datetime = str(insert_datetime)

            with mysql() as cursor:
                insert_into_sql = "INSERT INTO " + table_name + "(id, asin, insert_datetime, url, brand, title, " \
                                                                "variation_name, price, sold_by, how_many_sellers, " \
                                                                "review_num, review_value, qa_num,follow_type," \
                                                                "follow_num,buy_money,spans_text,review_last_time," \
                                                                "availability,aplus,review_last_unit," \
                                                                "review_last_desc,brand_url) VALUES ('%s', '%s', '%s', '%s', " \
                                                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                                                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                                                                "'%s', '%s', '%s') "
                data = (id, asin, insert_datetime, url, brand, title, variation_name, price, sold_by, how_many_sellers,
                        review_num, review_value, qa_num, follow_type, follow_num, buy_money, spans_text,
                        review_last_time, availability, aplus, review_last_unit, review_last_desc, brand_url)
                # print("{}:".format(insert_datetime), insert_into_sql)
                cursor.execute(insert_into_sql % data)
        except Exception as e:
            print(insert_into_sql + " errors:{}".format(e), data)
    except Exception as e:
        print("INSERT " + table_name + " errors!!{}".format(e))


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


def update_listing_google(data_asins):
    # state: 0  insert data
    #        -1 error data
    #        2  handled by Amazon program
    #        11 first filter by under 30 review_num and under 4.0 review_value
    update_sql = "UPDATE listing_google_us set state = 2 where asin = %s"

    try:
        with mysql() as cursor:
            row_count = cursor.executemany(update_sql, data_asins)
            # print("UPDATE listing_google {}/{} success:", row_count, len(data_asins))
    except Exception as e:
        print("UPDATE listing_google errors:{}".format(e), data_asins)



