# 默认下载best seller列表pet类目的产品信息并添加到mysql数据库，大概2w-3w条数据；
# 要修改第352行mysql数据库的用户名，密码；

import pymysql
import re
from amazon_module import amazon_module
from datetime import datetime

def asin_to_listing_info(asin):
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
        print("brand: ", brand)

        badge = ""
        try:
            if soup.find("a", class_="badge-link"):
               badge = " ".join(soup.find("a", class_="badge-link").get_text().strip().split())
        except:
            pass
        print("badge: ", badge)

        title = ""
        try:
            if soup.find(id="productTitle"):
                title = soup.find(id="productTitle").get_text().strip()
        except:
            pass
        print("title: ", title)

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
                price = soup.find(id="price").find("span").get_text().strip()
            if soup.find(id="priceblock_ourprice"):
                price = soup.find(id="priceblock_ourprice").get_text().strip()
        except:
            pass
        print("price: ", price)

        sold_by = " "
        try:
            if soup.find(id="merchant-info"):
                # print("soup.find(id='merchant-info').get_text().strip(): ", soup.find(id="merchant-info").get_text().strip())
                sold_by = " ".join(soup.find(id="merchant-info").get_text().strip().split())
        except:
            pass
        print("sold_by: ", sold_by)

        how_many_sellers = " "
        try:
            if soup.find(id="olp_feature_div"):
                how_many_sellers = soup.find(id="olp_feature_div").find("a").get_text().strip()
        except:
            pass
        print("how_many_sellers: ", how_many_sellers )

        bullets_list = []
        try:
            if  soup.find("div", id="feature-bullets"):
                bullets_contents = soup.find("div", id="feature-bullets").find_all("span", class_="a-list-item")
                print("bullets: ")
                for bullets_content in bullets_contents:
                    print(bullets_content.get_text().strip())
                    #toys
                    if bullets_content.span:
                        continue
                    bullets_list.append(bullets_content.get_text().strip())
        except:
            pass

        description = " "
        try:
            if soup.find(id="productDescription"):
                description = soup.find(id="productDescription").get_text()
            if soup.find(id="aplus"):
                description = soup.find(id="aplus").get_text()
            description = " ".join(description.split())
        except:
            pass
        print("description: ", description)

        salesrank = " "
        try:
            if soup.find(id="SalesRank"):
                salesrank = soup.find(id="SalesRank")
                salesrank = salesrank.get_text().strip()
                salesrank = re.search('#(\d|,)+', salesrank)
                salesrank = salesrank.group()
                salesrank = salesrank.replace(',', '')
                salesrank = salesrank.replace('#', '')
            #toys
            if soup.find(id="productDetails_detailBullets_sections1"):
                trs = soup.find(id="productDetails_detailBullets_sections1").find_all("tr")
                for tr in trs:
                    if tr.find("th").get_text().strip():
                        if tr.find("th").get_text().strip() == "Best Sellers Rank":
                            salesrank = tr.find("td").get_text().strip()
                            salesrank = re.search('#(\d|,)+', salesrank)
                            salesrank = salesrank.group()
                            salesrank = salesrank.replace(',', '')
                            salesrank = salesrank.replace('#', '')
        except:
            pass
        print("salesrank: ", salesrank)

        review_num = " "
        try:
            if soup.find(id="acrCustomerReviewText"):
                review_num = soup.find(id="acrCustomerReviewText").get_text().split()[0].strip()
        except:
            pass
        print("review_num: ", review_num)

        review_value = " "
        try:
            if soup.find(class_="arp-rating-out-of-text"):
                review_value = soup.find(class_="arp-rating-out-of-text").get_text().strip()
                review_value = re.search('(.*?)\s', review_value)
                review_value = review_value.group()
                review_value = review_value.strip()
        except:
            pass
        print("review_value: ", review_value)

        qa_num = " "
        try:
            if soup.find(id="askATFLink"):
                qa_num = soup.find(id="askATFLink").get_text().split()[0].strip()
        except:
            pass
        print("qa_num: ", qa_num)

        picture_url = " "
        try:
            picture_urls_dict = dict()
            if soup.find("img", id="landingImage"):
                picture_urls = soup.find("img", id="landingImage")["data-a-dynamic-image"]
                picture_urls_dict = eval(picture_urls)
            picture_urls_list = []
            for key in picture_urls_dict.keys():
                picture_urls_list.append(key)
            picture_url = picture_urls_list[0]
        except:
            pass
        print("picture_url: ", picture_url)

        listing_info_dict = {
                             "asin": asin,
                             "url": url,
                             "brand": brand,
                             "badge": badge,
                             "title": title,
                             "variation_name": variation_name,
                             "price": price,
                             "sold_by": sold_by,
                             "how_many_sellers": how_many_sellers,
                             "bullets": bullets_list,
                             "description": description,
                             "salesrank": salesrank,
                             "review_num": review_num,
                             "review_value": review_value,
                             "qa_num": qa_num,
                             "picture_url": picture_url
                             }
        # print(listing_info_dict)
        return listing_info_dict

def insert_data_to_mysql(asin_dict):
    try:
        try:
            asin = asin_dict["asin"]
            print(asin)
        except:
            pass
        try:
            url = asin_dict["url"]
            print(url)
        except:
            pass
        try:
            brand = asin_dict["brand"]
            brand = pymysql.escape_string(brand)
            print(brand)
        except:
            pass
        try:
            badge = asin_dict["badge"]
            badge = pymysql.escape_string(badge)
            print("bage: ", badge)
        except:
            pass
        try:
            title = asin_dict["title"]
            title = pymysql.escape_string(title)
            print("title: ", title)
        except:
            pass
        try:
            variation_name = asin_dict["variation_name"]
            variation_name = pymysql.escape_string(variation_name)
            print(variation_name)
        except:
            pass
        try:
            price = asin_dict["price"]
            print(price)
        except:
            pass
        try:
            sold_by = asin_dict["sold_by"]
            sold_by = pymysql.escape_string(sold_by)
            print(sold_by)
        except:
            pass
        try:
            how_many_sellers = asin_dict["how_many_sellers"]
            how_many_sellers = pymysql.escape_string(how_many_sellers)
        except:
            pass
        try:
            bullets = asin_dict["bullets"]
            # print(bullets)

            bullet_1 = " "
            bullet_2 = " "
            bullet_3 = " "
            bullet_4 = " "
            bullet_5 = " "
            if bullets:
                try:
                    bullet_1 = bullets[0]
                    bullet_1 = pymysql.escape_string(bullet_1)
                except:
                    pass
                try:
                    bullet_2 = bullets[1]
                    bullet_2 = pymysql.escape_string(bullet_2)
                except:
                    pass
                try:
                    bullet_3 = bullets[2]
                    bullet_3 = pymysql.escape_string(bullet_3)
                except:
                    pass
                try:
                    bullet_4 = bullets[3]
                    bullet_4 = pymysql.escape_string(bullet_4)
                except:
                    pass
                try:
                    bullet_5 = bullets[4]
                    bullet_5 = pymysql.escape_string(bullet_5)
                except:
                    pass
        except:
            pass

        print("bullet_1: ", bullet_1)
        print("bullet_2: ", bullet_2)
        print("bullet_3: ", bullet_3)
        print("bullet_4: ", bullet_4)
        print("bullet_5: ", bullet_5)
        try:
            description = asin_dict["description"]
            description = pymysql.escape_string(description)
            print(description)
        except:
            pass
        try:
            salesrank = asin_dict["salesrank"]
            print(salesrank)
        except:
            pass
        try:
            review_num = asin_dict["review_num"]
            print(review_num)
        except:
            pass
        try:
            review_value =asin_dict["review_value"]
            print(review_value)
        except:
            pass
        try:
            qa_num = asin_dict["qa_num"]
            print(qa_num)
        except:
            pass
        try:
            picture_url = asin_dict["picture_url"]
            print(picture_url)
        except:
            pass
        try:
            insert_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("insert_datetime: ", insert_datetime)

            insert_into_sql = "INSERT INTO " + table_name + \
            " (asin, insert_datetime, url, brand, badge, title, variation_name, price, sold_by, how_many_sellers, bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, description, salesrank, review_num, review_value, qa_num, picture_url ) \
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ) " % \
            (asin, insert_datetime, url, brand, badge, title, variation_name, price, sold_by, how_many_sellers, bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, description, salesrank, review_num, review_value, qa_num, picture_url )

            cursor.execute(insert_into_sql)
            print(cursor)
            conn.commit()
            print("success to insert asin_dict to mysql")
        except:
            pass
    except:
        print("fail to insert asin_dict to mysql!")


## 需要修改成大类目名字
node_name = "pet"
txt_name = "pet_asin.txt"

asin_list = []
with open(txt_name, 'r') as f:
    asins = f.readlines()
    for asin in asins:
        asin_list.append(asin.strip())
print(len(asin_list))
print(asin_list)

conn = pymysql.connect("localhost", "root", "password",)
cursor = conn.cursor()

db_name = node_name + "_db"
try:
    create_db_sql = "create database " + db_name
    print(create_db_sql)
    cursor.execute(create_db_sql)
except:
    print("fail to create database " + db_name)

try:
    use_db_sql = "use " + db_name
    print(use_db_sql)
    cursor.execute(use_db_sql)
except:
    print("fail to use database: ", db_name)

table_name = node_name + "_table"
print(table_name)

try:
    create_table_sql = "create table " + table_name + " (asin char(10), insert_datetime varchar(30), url char(50), brand char(50), badge char(50), title char(250), variation_name char(250), price char(10), sold_by char(100), how_many_sellers char(100), bullet_1 varchar(3000), bullet_2 varchar(3000), bullet_3 varchar(3000), bullet_4 varchar(3000), bullet_5 varchar(3000), description varchar(3000), salesrank char(10), review_num char(10), review_value char(10), qa_num char(10), picture_url char(100) )"
    print(create_table_sql)
    cursor.execute(create_table_sql)
    print(cursor)
except:
    print("fail to create table: ", table_name)





for index, asin in enumerate(asin_list):

    try:
        asin_dict = asin_to_listing_info(asin)
        print("index: ", index + 1 )
        print(asin_dict)
        insert_data_to_mysql(asin_dict)
    except:
        print("fail")

conn.close()
