from amazon_module import amazon_module
import re
import os
from bs4 import BeautifulSoup
import requests
import csv
import openpyxl

node_dict = {}
node_url_dict = {}

top100_url = "https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_e_0_e_1"
soup = amazon_module.download_soup_by_url(top100_url)

lis = soup.find(id="zg_browseRoot").find("ul").find_all("li")

# for temp_li_index, temp_li in enumerate(lis):
#     print(temp_li_index, temp_li.get_text())

# 0 Amazon Devices & Accessories
# 1 Amazon Launchpad
# 2 Appliances
# 3 Apps & Games
# 4 Arts, Crafts & Sewing
# 5 Automotive
# 6 Baby
# 7 Beauty & Personal Care
# 8 Books
# 9 CDs & Vinyl
# 10 Camera & Photo
# 11 Cell Phones & Accessories
# 12 Clothing, Shoes & Jewelry
# 13 Collectible Coins
# 14 Computers & Accessories
# 15 Digital Music
# 16 Electronics
# 17 Entertainment Collectibles
# 18 Gift Cards
# 19 Grocery & Gourmet Food
# 20 Health & Household
# 21 Home & Kitchen
# 22 Industrial & Scientific
# 23 Kindle Store
# 24 Kitchen & Dining
# 25 Magazine Subscriptions
# 26 Movies & TV
# 27 Musical Instruments
# 28 Office Products
# 29 Patio, Lawn & Garden
# 30 Pet Supplies
# 31 Prime Pantry
# 32 Software
# 33 Sports & Outdoors
# 34 Sports Collectibles
# 35 Tools & Home Improvement
# 36 Toys & Games
# 37 Video Games

# 30 Pet Supplies
start_node = 30

node_num_chain = ""
node_chain = ""

def page_url_to_asin_list(url):
    asin_list = []
    try:
        page_soup = amazon_module.download_soup_by_url(url)
        page_lis = page_soup.find(id="zg-ordered-list").find_all("li", class_="zg-item-immersion")
        for page_li_index, page_li in enumerate(page_lis):
            try:
                link = page_li.find("a")['href']
                asin = re.findall(r"dp/(.*?)/ref", link)[0]
                badge = page_li.find("span", class_="zg-badge-text").get_text()
                print(page_li_index, asin, badge)
                asin_list.append(asin + badge)
            except:
                pass
        return asin_list
    except:
        pass

def url_to_all_asin_list(url):
    all_asin_list = []
    count = 10
    asin_list = []
    for i in range(2):
        try:
            page_url = re.sub(r"ref=zg(.*)", "ref=zg_bs_pg_" + str(i+1) + "?_encoding=UTF8&pg=" + str(i+1), url)
            print(page_url)

            try:
                asin_list = page_url_to_asin_list(page_url)
                print("asin_list:", asin_list)
            except:
                pass

            while count > 0 and asin_list is None:
                asin_list = page_url_to_asin_list(page_url)
                count -= 1
                print("count:", count)

            try:
                if asin_list is not None:
                    all_asin_list.extend(asin_list)
            except:
                pass
        except:
            pass

    print("all_asin_list:", all_asin_list)
    return all_asin_list

def asin_info_save_to_csv_file(asin_info_dict):
    csv_folder = "csv"
    csv_filename = "top10000.csv"
    csv_file_path = csv_folder + "/" + csv_filename

    headers = ["node_chain", "node_num_chain", "asin_info"]

    if not os.path.exists(csv_folder):
        os.mkdir(csv_folder)
        print("success to create folder")

    if not os.path.isfile(csv_file_path):
        try:
            with open(csv_file_path, 'w', encoding='utf8', newline='') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                print("success to write csv header!")
        except:
            print("fail to write csv header!")

    try:
        with open(csv_file_path, 'a+', encoding='utf8', newline='') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writerow(asin_info_dict)
            print("success to write csv content!")
    except:
        print("fail to write csv content!")

# for li in lis[30:31] 相当于获取lis[30]
# for li in lis[30:33] 相当于获取lis[30], lis[31], lis[32]

# for li in lis[30:31] 与 for li in lis[30] 意思是不一样的
# for li in lis[30:31] 相当于获取lis[30]
# for li in lis[30] 相当于获取lis[30]其中的元素（如果lis[30]可以迭代的话）
for li_index_step, li in enumerate(lis[start_node:start_node+1]):
    li_index = start_node + li_index_step
    li_title = li.get_text().strip()
    li_url = li.a['href']
    print("li_index:", li_index)
    print("li_title:", li_title)
    print("li_url:", li_url)

    node_num_chain = str(li_index)
    node_chain = li_title
    print("node_num_chain:", node_num_chain)
    print("node_chain:", node_chain)

    try:
        li_all_asin_list = url_to_all_asin_list(li_url)
        for li_asin in li_all_asin_list:
            asin_info_dict = {
                "node_chain": node_chain,
                "node_num_chain": node_num_chain,
                "asin_info": li_asin
            }
            asin_info_save_to_csv_file(asin_info_dict)
    except:
        pass

    soup_1 = amazon_module.download_soup_by_url(li_url)
    lis_1 = soup_1.find(id="zg_browseRoot").find("ul").find("ul").find_all("li")
    for li_1_index, li_1 in enumerate(lis_1):
        li_1_title = li_1.get_text().strip()
        li_1_url = li_1.a['href']
        print("  li_1_index:", li_1_index)
        print("  li_1_title:", li_1_title)
        print("  li_1_url:", li_1_url)

        node_num_chain = str(li_index) + "_" + str(li_1_index)
        node_chain = li_title + " => " + li_1_title
        print("  node_num_chain:", node_num_chain)
        print("  node_chain:", node_chain)

        try:
            li_1_all_asin_list = url_to_all_asin_list(li_1_url)
            for li_1_asin in li_1_all_asin_list:
                asin_info_dict = {
                    "node_chain": node_chain,
                    "node_num_chain": node_num_chain,
                    "asin_info": li_1_asin
                }
                asin_info_save_to_csv_file(asin_info_dict)
        except:
            pass

        try:
            soup_2 = amazon_module.download_soup_by_url(li_1.a['href'])
            lis_2 = soup_2.find(id="zg_browseRoot").find("ul").find("ul").find("ul").find_all("li")
            try:
                for li_2_index, li_2 in enumerate(lis_2):
                    li_2_title = li_2.get_text().strip()
                    li_2_url = li_2.a['href']
                    print("    li_2_index:", li_2_index)
                    print("    li_2_title:", li_2_title)
                    print("    li_2_url:", li_2_url)

                    node_num_chain = str(li_index) + "_" + str(li_1_index) + "_" + str(li_2_index)
                    node_chain = li_title + " => " + li_1_title + " => " + li_2_title
                    print("    node_num_chain:", node_num_chain)
                    print("    node_chain:", node_chain)

                    try:
                        li_2_all_asin_list = url_to_all_asin_list(li_2_url)
                        for li_2_asin in li_2_all_asin_list:
                            asin_info_dict = {
                                "node_chain": node_chain,
                                "node_num_chain": node_num_chain,
                                "asin_info": li_2_asin
                            }
                            asin_info_save_to_csv_file(asin_info_dict)
                    except:
                        pass

                    try:
                        soup_3 = amazon_module.download_soup_by_url(li_2.a['href'])
                        lis_3 = soup_3.find(id="zg_browseRoot").find("ul").find("ul").find("ul").find("ul").find_all("li")
                        for li_3_index, li_3 in enumerate(lis_3):
                            li_3_title = li_3.get_text().strip()
                            li_3_url = li_3.a['href']
                            print("      li_3_index:", li_3_index)
                            print("      li_3_title:", li_3_title)
                            print("      li_3_url:", li_3_url)

                            node_num_chain = str(li_index) + "_" + str(li_1_index) + "_" + str(li_2_index) + "_" + str(li_3_index)
                            node_chain = li_title + " => " + li_1_title + " => " + li_2_title + " => " + li_3_title
                            print("      node_num_chain:", node_num_chain)
                            print("      node_chain:", node_chain)

                            try:
                                li_3_all_asin_list = url_to_all_asin_list(li_3_url)
                                for li_3_asin in li_3_all_asin_list:
                                    asin_info_dict = {
                                        "node_chain": node_chain,
                                        "node_num_chain": node_num_chain,
                                        "asin_info": li_3_asin
                                    }
                                    asin_info_save_to_csv_file(asin_info_dict)
                            except:
                                pass
                    except:
                        pass
            except:
                pass

        except:
            pass




def asin_to_listing_info(asin, index):

        print("asin: ", asin)

        url = "https://www.amazon.com/dp/" + asin
        print("url: ", url)

        soup = amazon_module.download_soup_by_url(url)

        brand = " "
        try:
            if soup.find(id="bylineInfo"):
                brand = soup.find(id="bylineInfo").get_text().strip()
            if soup.find(id="brand"):
                brand = soup.find(id="brand").get_text().strip()
        except:
            pass
        print("brand: ", brand)

        badge = " "
        try:
            if soup.find("a", class_="badge-link"):
               badge = " ".join(soup.find("a", class_="badge-link").get_text().strip().split())
        except:
            pass
        print("badge: ", badge)

        title = " "
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
        sale_price = " "
        try:
            if soup.find(id="price"):
                price = soup.find(id="price").find("span").get_text().strip()
            if soup.find(id="priceblock_ourprice"):
                price = soup.find(id="priceblock_ourprice").get_text().strip()
            if soup.find(id="priceblock_saleprice"):
                sale_price = soup.find(id="priceblock_saleprice").get_text().strip()
        except:
            pass
        print("price: ", price)
        print("sale_price: ", sale_price)

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
        bullet_1 = " "
        bullet_2 = " "
        bullet_3 = " "
        bullet_4 = " "
        bullet_5 = " "
        try:
            if soup.find("div", id="feature-bullets"):
                bullets_contents = soup.find("div", id="feature-bullets").find_all("span", class_="a-list-item")
                # print("bullets: ")
                for bullets_content in bullets_contents:
                    # print(bullets_content.get_text().strip())
                    #toys
                    if bullets_content.span:
                        continue
                    bullets_list.append(bullets_content.get_text().strip())
        except:
            pass
        try:
            bullet_1 = bullets_list[0]
            bullet_2 = bullets_list[1]
            bullet_3 = bullets_list[2]
            bullet_4 = bullets_list[3]
            bullet_5 = bullets_list[4]
        except:
            pass
        print("bullet_1: ", bullet_1)
        print("bullet_2: ", bullet_2)
        print("bullet_3: ", bullet_3)
        print("bullet_4: ", bullet_4)
        print("bullet_5: ", bullet_5)


        description = " "
        try:
            if soup.find(id="productDescription"):
                description = soup.find(id="productDescription").get_text()
            if soup.find(id="aplus"):
                description = soup.find(id="aplus").find("div").find_all("div").get_text()
                description = re.search(r".aplus-v2(.*)\}(.*)", description)
                description = description.group(1)
                description = description.strip()
            description = " ".join(description.split())
        except:
            pass
        print("description: ", description)

        salesrank = " "
        # try:
        #     if soup.find(id="SalesRank"):
        #         salesrank = soup.find(id="SalesRank")
        #         salesrank = salesrank.get_text().strip()
        #         salesrank = re.search('#(\d|,)+', salesrank)
        #         salesrank = salesrank.group()
        #         salesrank = salesrank.replace(',', '')
        #         salesrank = salesrank.replace('#', '')
        #     #toys
        #     if soup.find(id="productDetails_detailBullets_sections1"):
        #         trs = soup.find(id="productDetails_detailBullets_sections1").find_all("tr")
        #         for tr in trs:
        #             if tr.find("th").get_text().strip():
        #                 if tr.find("th").get_text().strip() == "Best Sellers Rank":
        #                     salesrank = tr.find("td").get_text().strip()
        #                     salesrank = re.search('#(\d|,)+', salesrank)
        #                     salesrank = salesrank.group()
        #                     salesrank = salesrank.replace(',', '')
        #                     salesrank = salesrank.replace('#', '')
        # except:
        #     pass
        # print("salesrank: ", salesrank)

        salesrank_1 = " "
        salesrank_2 = " "
        salesrank_3 = " "
        salesrank_node_1 = " "
        salesrank_node_2 = " "
        salesrank_node_3 = " "
        try:
            salesrank_1 = soup.find(id="SalesRank")
            salesrank_1 = salesrank_1.get_text().strip()
            salesrank_1 = re.search('#(\d|,)+', salesrank_1)
            salesrank_1 = salesrank_1.group()
            salesrank_1 = salesrank_1.replace(',', '')
            salesrank_1 = salesrank_1.replace('#', '')
            # print(salesrank_1)
            salesrank_node_1 = soup.find(id="SalesRank")
            salesrank_node_1 = salesrank_node_1.get_text().strip()
            salesrank_node_1 = re.search(r"in(.*?)\(", salesrank_node_1)
            salesrank_node_1 = salesrank_node_1.group()
            salesrank_node_1 = salesrank_node_1.replace("in ", "")
            salesrank_node_1 = salesrank_node_1.replace(" (", "")
            salesrank_node_1 = salesrank_node_1.strip()
            # print(salesrank_node_1)

            try:
                lis = soup.find(id="SalesRank").find("ul", class_="zg_hrsr").find_all("li")
                node_salesrank_list = []
                node_name_list = []
                for li in lis:
                    node_salesrank = li.get_text().strip()
                    node_salesrank = re.search('#(\d|,)+', node_salesrank)
                    node_salesrank = node_salesrank.group()
                    node_salesrank = node_salesrank.replace(',', '')
                    node_salesrank = node_salesrank.replace('#', '')
                    node_salesrank_list.append(node_salesrank)

                    node_name = li.get_text().strip()
                    node_name = re.search(r"in(.*)", node_name)
                    node_name = node_name.group()
                    node_name = node_name.replace("in\xa0", "")
                    node_name = node_name.strip()
                    node_name_list.append(node_name)
                # print(node_salesrank_list)
                # print(node_name_list)

                if len(node_salesrank_list) == 1:
                    salesrank_2 = node_salesrank_list[0]
                if len(node_salesrank_list) == 2:
                    salesrank_2 = node_salesrank_list[0]
                    salesrank_3 = node_salesrank_list[1]

                if len(node_salesrank_list) == 1:
                    salesrank_node_2 = node_name_list[0]
                if len(node_salesrank_list) == 2:
                    salesrank_node_2 = node_name_list[0]
                    salesrank_node_3 = node_name_list[1]
            except:
                pass
        except:
            pass
        print("salesrank_1: ", salesrank_1, " ", "salesrank_node_1: ", salesrank_node_1)
        print("salesrank_2: ", salesrank_2, " ", "salesrank_node_2: ", salesrank_node_2)
        print("salesrank_3: ", salesrank_3, " ", "salesrank_node_3: ", salesrank_node_3)



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
                             "sale_price": sale_price,
                             "sold_by": sold_by,
                             "how_many_sellers": how_many_sellers,
                             # "bullets": bullets_list,
                             "bullet_1": bullet_1,
                             "bullet_2": bullet_2,
                             "bullet_3": bullet_3,
                             "bullet_4": bullet_4,
                             "bullet_5": bullet_5,
                             "description": description,
                             # "salesrank": salesrank,
                             "salesrank_1": salesrank_1,
                             "salesrank_node_1": salesrank_node_1,
                             "salesrank_2": salesrank_2,
                             "salesrank_node_2": salesrank_node_2,
                             "salesrank_3": salesrank_3,
                             "salesrank_node_3": salesrank_node_3,
                             "review_num": review_num,
                             "review_value": review_value,
                             "qa_num": qa_num,
                             "picture_url": picture_url
                             }

        # return listing_info_dict
        dict_list_to_csv_file(listing_info_dict, index)

        try:
            download_picture_by_url(asin, picture_url)
        except:
            pass


def dict_list_to_csv_file(listing_info_dict, index):
        print("start to write csv file...")
        headers = []
        for i in listing_info_dict:
            headers.append(i)

        csv_folder = "amazon_top_100"
        csv_file_name = "pet_asin"
        csv_file_path = csv_folder + "/" + csv_file_name + ".csv"
        print("csv_file_path: ", csv_file_path)
        try:
            with open(csv_file_path, 'a+', encoding='utf8', newline='') as f:
                f_csv = csv.DictWriter(f, headers)
                if index == 0:
                    f_csv.writeheader()
                # f_csv.writeheader()
                f_csv.writerow(listing_info_dict)
                print("success to write csv file...")
        except:
            print("fail to write csv!")

        print("***********************************")

def download_picture_by_url(asin, picture_url):
        print("start to download picture...")

        try:
            pic = requests.get(picture_url, timeout=10)
            picture_folder = "amazon_top_100"
            picture_name = picture_folder + "/"+ asin + '.jpg'
            with open(picture_name, 'wb') as fp:
                fp.write(pic.content)
            print("success to download picture")
        except requests.exceptions.ConnectionError:
            print("download picture failed!")
        print("***********************************")

# unparsed_asin_list = []
# unparsed_asin_set = set()
# parsed_asin_set = set()
#
#
# with open("pet_28772_asin.txt", "r") as f:
#     for line in f.readlines():
#         unparsed_asin_list.append(line.strip())
#
# unparsed_asin_set = set(unparsed_asin_list)
# for index, asin in enumerate(unparsed_asin_list):
#     if asin not in parsed_asin_set:
#
#         print("index: ", index)
#         # print("asin: ", asin)
#         asin_to_listing_info(asin, index)
#
#         unparsed_asin_set.remove(asin)
#         parsed_asin_set.add(asin)
#
# print(len(unparsed_asin_set))
# print(len(parsed_asin_set))
