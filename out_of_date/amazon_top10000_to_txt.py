from amazon_module import amazon_module
import re
import os
from bs4 import BeautifulSoup
import requests
import csv

node_dict = {}
node_url_dict = {}

top100_url = "https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_e_0_e_1"
soup = amazon_module.download_soup_by_url(top100_url)

lis = soup.find(id="zg_browseRoot").find("ul").find_all("li")
for li in lis[25:26]:
    print("li: ", li.get_text().strip())
    # print(li.a['href'])
    node_dict[li.get_text().strip()] = "none"
    node_url_dict[li.get_text().strip()] = li.a['href']

    soup_1 = amazon_module.download_soup_by_url(li.a['href'])
    lis_1 = soup_1.find(id="zg_browseRoot").find("ul").find("ul").find_all("li")
    temp_dict_1 = {}
    for li_1 in lis_1:
        print("  li_1: ", li_1.get_text().strip())
        # print("li_1.url: ", li_1.a['href'])
        temp_dict_1[li_1.get_text().strip()] = "none"
        node_url_dict[li.get_text().strip() + " " + li_1.get_text().strip()] = li_1.a['href']

        try:
            soup_2 = amazon_module.download_soup_by_url(li_1.a['href'])
            lis_2 = soup_2.find(id="zg_browseRoot").find("ul").find("ul").find("ul").find_all("li")
            temp_dict_2 = {}
            try:
                for li_2 in lis_2:
                    print("    li_2: ", li_2.get_text().strip())
                    # print("li_2.url: ", li_2.a['href'])
                    temp_dict_2[li_2.get_text().strip()] = "none"
                    node_url_dict[li_1.get_text().strip() + " " + li_2.get_text().strip()] = li_2.a['href']

                    try:
                        soup_3 = amazon_module.download_soup_by_url(li_2.a['href'])
                        lis_3 = soup_3.find(id="zg_browseRoot").find("ul").find("ul").find("ul").find("ul").find_all("li")
                        temp_dict_3 = {}
                        try:
                            for li_3 in lis_3:
                                print("      li_3: ", li_3.get_text().strip())
                                # print("li_3.url: ", li_3.a['href'])
                                temp_dict_3[li_3.get_text().strip()] = "none"
                                node_url_dict[li_1.get_text().strip() + " " + li_2.get_text().strip() + " " + li_3.get_text().strip()] = li_3.a['href']

                        except:
                            pass
                        try:
                            temp_dict_2[li_2.get_text().strip()] = temp_dict_3
                        except:
                            pass
                    except:
                        pass
            except:
                pass
            try:
                temp_dict_1[li_1.get_text().strip()] = temp_dict_2
            except:
                pass

        except:
            pass

    node_dict[li.get_text().strip()] = temp_dict_1
    node_url_dict[li_1.get_text().strip()] = li_1.a['href']

print("node_dict: ", node_dict)
print("node_url_dict: ", node_url_dict)

print("len of node_dict: ", len(node_dict))
print("len of node_url_dict: ", len(node_url_dict))
#
# start_url = "https://www.amazon.com/Best-Sellers-Pet-Supplies-Dry-Dog-Food/zgbs/pet-supplies/2975360011/ref=zg_bs_nav_petsupplies_3_2975359011"
# new_url_list = []
# new_url_list.append(start_url)
#
# asin_set = set()
# new_url_list = node_url_dict.values()
# old_url_set = set()
# for url in new_url_list:
#     if url not in old_url_set:
#         old_url_set.add(url)
#         for i in range(5):
#             try:
#                 page_url = re.sub(r"ref=zg(.*)", "ref=zg_bs_pg_" + str(i+1) + "?_encoding=UTF8&pg=" + str(i+1), url)
#                 print(page_url)
#                 page_soup = amazon_module.download_soup_by_url(page_url)
#                 page_lis = page_soup.find(id="zg_centerListWrapper").find_all("div", class_="zg_itemImmersion")
#                 for page_li in page_lis:
#                     try:
#                         link = page_li.find("a")['href']
#                         asin = re.findall(r"dp/(.*?)/ref", link)[0]
#                         # print(asin)
#                         asin_set.add(asin)
#                     except:
#                         pass
#             except:
#                 pass
# print(asin_set)
# print(len(asin_set))
#
# with open("pet.txt", "w") as f:
#     for asin in asin_set:
#         f.write(asin + "\n")

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
            if  soup.find("div", id="feature-bullets"):
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
