# coding: utf-8

import pymysql
import re
from amazon_module import amazon_module
from datetime import datetime
import requests
import os

# 记得先安装pymysql， pip3 install pymysql
# 默认会新建图片文件夹，文件名默认是关键词（关键词内空格换成下划线）
# 记得修改mysql用户名，密码
# mysql里默认下载到amazon_db数据库，表名是关键词（关键词内空格换成下划线） + "_table"

# change them to yours
keyword = "men shoes"
max_page = 3

db_config = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': 'P@ssw0rd',
    'database': 'amazon_db',
    'charset': 'utf8'
}

mysql_table = "_".join(keyword.split()) + "_table"

def download_picture_by_url(picture_url, picture_folder, asin):
    print("start to download picture...")

    try:
        pic = requests.get(picture_url, timeout=10)
        picture_name = picture_folder + "/"+ str(asin) + '.jpg'
        with open(picture_name, 'wb') as fp:
            fp.write(pic.content)
        print("success to download picture")
    except requests.exceptions.ConnectionError:
        print("download picture failed!")

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
        print("brand:", brand)

        badge = ""
        try:
            if soup.find("a", class_="badge-link"):
               badge = " ".join(soup.find("a", class_="badge-link").get_text().strip().split())
        except:
            pass
        print("badge:", badge)

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
                price = soup.find(id="price").find("span").get_text().strip()
            if soup.find(id="priceblock_ourprice"):
                price = soup.find(id="priceblock_ourprice").get_text().strip()
        except:
            pass
        print("price:", price)

        sold_by = " "
        try:
            if soup.find(id="merchant-info"):
                # print("soup.find(id='merchant-info').get_text().strip(): ", soup.find(id="merchant-info").get_text().strip())
                sold_by = " ".join(soup.find(id="merchant-info").get_text().strip().split())
        except:
            pass
        print("sold_by:", sold_by)

        how_many_sellers = " "
        try:
            if soup.find(id="olp_feature_div"):
                how_many_sellers = soup.find(id="olp_feature_div").find("a").get_text().strip()
        except:
            pass
        print("how_many_sellers:", how_many_sellers )

        bullets_list = []
        try:
            if  soup.find("div", id="feature-bullets"):
                bullets_contents = soup.find("div", id="feature-bullets").find_all("span", class_="a-list-item")
                print("bullets:")
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
        print("description:", description)

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
        print("salesrank:", salesrank)

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
        print("picture_url:", picture_url)

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

        return listing_info_dict

def insert_data_to_mysql(asin_dict, table_name, conn):
    print("insert_data_to_mysql")
    try:
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
            badge = asin_dict["badge"]
            badge = pymysql.escape_string(badge)
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

        price = " "
        try:
            price = asin_dict["price"]
            price = str(price)
            price = pymysql.escape_string(price)
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
            bullets = asin_dict["bullets"]

            bullet_1 = " "
            bullet_2 = " "
            bullet_3 = " "
            bullet_4 = " "
            bullet_5 = " "
            bullet_6 = " "
            bullet_7 = " "
            bullet_8 = " "
            bullet_9 = " "
            bullet_10 = " "
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
                try:
                    bullet_6 = bullets[5]
                    bullet_6 = pymysql.escape_string(bullet_6)
                except:
                    pass
                try:
                    bullet_7 = bullets[6]
                    bullet_7 = pymysql.escape_string(bullet_7)
                except:
                    pass
                try:
                    bullet_8 = bullets[7]
                    bullet_8 = pymysql.escape_string(bullet_8)
                except:
                    pass
                try:
                    bullet_9 = bullets[8]
                    bullet_9 = pymysql.escape_string(bullet_9)
                except:
                    pass
                try:
                    bullet_10 = bullets[9]
                    bullet_10 = pymysql.escape_string(bullet_10)
                except:
                    pass
        except:
            pass

        try:
            description = asin_dict["description"]
            description = " ".join(description.split())
            description = pymysql.escape_string(description)
        except:
            pass
        try:
            salesrank = asin_dict["salesrank"]
            salesrank = pymysql.escape_string(salesrank)
        except:
            pass
        try:
            review_num = asin_dict["review_num"]
            review_num = pymysql.escape_string(review_num)
        except:
            pass
        try:
            review_value =asin_dict["review_value"]
            review_value = pymysql.escape_string(review_value)
        except:
            pass
        try:
            qa_num = asin_dict["qa_num"]
        except:
            pass
        try:
            picture_url = asin_dict["picture_url"]
        except:
            pass
        try:
            insert_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_datetime = str(insert_datetime)
            print("insert_datetime: ", insert_datetime)

            with conn.cursor() as cursor:
                insert_into_sql = "INSERT INTO " + table_name + " (asin, insert_datetime, url, brand, badge, title, variation_name, price, sold_by, how_many_sellers, bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, bullet_6, bullet_7, bullet_8, bullet_9, bullet_10, description, salesrank, review_num, review_value, qa_num, picture_url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') "
                data = (asin, insert_datetime, url, brand, badge, title, variation_name, price, sold_by, how_many_sellers, bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, bullet_6, bullet_7, bullet_8, bullet_9, bullet_10, description, salesrank, review_num, review_value, qa_num, picture_url)
                cursor.execute(insert_into_sql % data )
                conn.commit()
                print("success to insert asin_dict to mysql")
        except:
            print("fail to insert asin_dict to mysql!")
    except:
        print("fail to insert asin_dict to mysql!!")

def keyword_to_asin_list(keyword, max_page, table_name, conn):
    print("keyword_to_asin_list is running...")
    base_url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
    keyword_with_underline = "_".join(keyword.split())
    keyword_with_plus = "+".join(keyword.split())
    first_page_url = base_url + keyword_with_plus

    pages_urls_list = []
    pages_urls_list.append(first_page_url)
    page = 1
    while page <= max_page:
        # soup = self.download_soup_by_url(pages_urls_list[-1])
        soup = amazon_module.download_soup_by_url(pages_urls_list[-1])
        try:
            if soup.find(id="pagnNextLink")["href"]:
                next_page_url_part2 = soup.find(id="pagnNextLink")["href"]
                next_page_url = "https://www.amazon.com" + next_page_url_part2
                pages_urls_list.append(next_page_url)
            page = page + 1
        except:
            pass

        try:
            lis = soup.find_all("li", class_="s-result-item")
            for index, li in enumerate(lis):
                try:
                    asin = li["data-asin"]

                    page_rank = "page" + str(page - 1) + "-" + str(index + 1)
                    print("page_rank: ", page_rank)

                    sponsored_or_natural_rank = "natural_rank"
                    try:
                        if li.find("h5").get_text().strip().split()[0]:
                            if li.find("h5").get_text().strip().split()[0] == "Sponsored":
                                sponsored_or_natural_rank = "sponsored"
                            else:
                                sponsored_or_natural_rank = "natural_rank"
                    except:
                        pass
                    print("sponsored_or_natural_rank: ", sponsored_or_natural_rank)

                    is_prime = ""
                    try:
                        if li.find("i", class_="a-icon-prime"):
                            is_prime  = "prime"
                    except:
                        pass
                    print("is_prime: ", is_prime)

                    listing_info_dict = asin_to_listing_info(asin)
                    listing_info_dict["page_rank"] = page_rank
                    listing_info_dict["sponsored_or_natural_rank"] = sponsored_or_natural_rank
                    listing_info_dict["is_prime"] = is_prime

                    try:
                        insert_data_to_mysql(listing_info_dict, table_name, conn)
                    except:
                        pass

                    try:
                        picture_url = listing_info_dict['picture_url']
                        picture_folder = keyword_with_underline
                        download_picture_by_url(picture_url, picture_folder, asin)
                    except:
                        print("fail to download picture")
                except:
                    pass
        except:
            pass


# do not change
keyword_with_underline = "_".join(keyword.split())

# create picture folder
picture_folder = keyword_with_underline
try:
    if not os.path.exists(picture_folder):
        print("picture folder does not exist, creating the folder...")
        os.mkdir(picture_folder)
        print("success to create picture folder")
except:
    print("fail to create picture folder")

# change "root", "password"
conn = pymysql.connect(db_config['host'], db_config['username'], db_config['password'],)
cursor = conn.cursor()

# create datebase
db_name = db_config['database']
try:
    create_db_sql = "create database " + db_name
    print(create_db_sql)
    cursor.execute(create_db_sql)
except:
    print("fail to create database " + db_name)

# use database
try:
    use_db_sql = "use " + db_name
    print(use_db_sql)
    cursor.execute(use_db_sql)
except:
    print("fail to use database:", db_name)

# create table
table_name = mysql_table
print(table_name)
try:
    create_table_sql = "create table " + table_name + " (asin char(10), insert_datetime char(30), url char(100), brand char(50), badge char(50), title varchar(500), variation_name varchar(250), price char(50), sold_by char(100), how_many_sellers char(100), bullet_1 varchar(3000), bullet_2 varchar(3000), bullet_3 varchar(3000), bullet_4 varchar(3000), bullet_5 varchar(3000), bullet_6 varchar(3000), bullet_7 varchar(3000), bullet_8 varchar(3000), bullet_9 varchar(3000), bullet_10 varchar(3000), description varchar(9000), salesrank char(10), review_num char(10), review_value char(10), qa_num char(10), picture_url char(100) )"
    print(create_table_sql)
    cursor.execute(create_table_sql)
    print(cursor)
except:
    print("fail to create table:", table_name)

# keyword_to_asin_list
try:
    keyword_to_asin_list(keyword, max_page, table_name, conn)
except:
    print("fail")

conn.close()
