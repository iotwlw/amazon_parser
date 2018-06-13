# coding: utf-8

import re
from amazon_module import amazon_module
import requests
import os
import csv

class Storefront_to_listing():

    def __init__(self):

        # change to yours
        self.storefront_url = "https://www.amazon.com/s?marketplaceID=ATVPDKIKX0DER&me=A3I7K5MJPCIZH9&merchant=A3I7K5MJPCIZH9&redirect=true"
        self.store_name = "Sprtjoy"
        self.max_page = 5

        # don't change
        self.csv_folder = ""
        self.csv_file_name = ""
        self.picture_folder = ""
        self.picture_url = ""
        self.asin = ""
        self.asin_list = []
        self.listing_info_dict = dict()
        self.best_seller_badge = " "

    def store_url_to_asin_list(self, store_url):
        soup = amazon_module.download_soup_by_url(store_url)
        # lis = soup.find(id="s-results-list-atf").find_all("li")
        lis = soup.find_all("li", class_="celwidget")
        asin_list = []
        for index, li in enumerate(lis):
            self.asin = li["data-asin"]
            # self.listing_info_dict = self.asin_to_listing_info()
            # self.listing_info_dict_to_csv_file()
            asin_list.append(self.asin)
            self.asin_list.append(self.asin)
            print (self.asin)
            # best seller badge
            self.best_seller_badge = ""
            try:
                best_seller_badge_id = "BESTSELLER_" + self.asin
                best_seller_badge = li.find(id=best_seller_badge_id).get_text()
                best_seller_badge = " ".join(best_seller_badge.split())
                self.best_seller_badge = best_seller_badge.replace("Best Seller", "Best Seller ", 1)
                print("best_seller_badge:", self.best_seller_badge)
            except:
                pass
        return asin_list

    def storefront_url_to_store_url_list(self):
        store_url_list = []
        store_url_list.append(self.storefront_url)
        page = self.max_page
        if page == 1:
            return store_url_list
        while page > 1:
            soup = amazon_module.download_soup_by_url(store_url_list[-1])
            try:
                if soup.find(id="pagnNextLink")['href']:
                    next_page_url_part2 = soup.find(id="pagnNextLink")['href']
                    next_page_url = "https://www.amazon.com" + next_page_url_part2
                    store_url_list.append(next_page_url)
            except:
                return store_url_list
            page = page - 1
        return store_url_list

    def listing_info_dict_to_csv_file(self):
        try:
            headers = []
            for i in self.listing_info_dict:
                headers.append(i)
        except:
            print("fail to find csv header tags")

        csv_file_path = self.csv_folder + self.csv_file_name

        if not os.path.exists(self.csv_folder):
            os.mkdir(self.csv_folder)
            print("success to create folder")

        if not os.path.isfile(csv_file_path):
            try:
                with open(csv_file_path, 'w') as f:
                    f_csv = csv.DictWriter(f, headers)
                    f_csv.writeheader()
                    print("success to write csv header!")
            except:
                print("fail to write csv header!")

        try:
            with open(csv_file_path, 'a+') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writerow(self.listing_info_dict)
                print("success to write csv content!")
        except:
            print("fail to write csv content!")

    def download_picture_by_url(self):
        try:
            if not os.path.exists(self.picture_folder):
                os.makedirs(self.picture_folder)
                print("success to create picture folder")
        except:
            print("fail to create picture folder")

        try:
            pic = requests.get(self.picture_url, timeout=10)
            picture_name = self.picture_folder + str(self.asin) + '.jpg'
            with open(picture_name, 'wb') as fp:
                fp.write(pic.content)
            print("success to download picture!")
        except requests.exceptions.ConnectionError:
            print("fail to download picture!")

    def asin_to_listing_info(self):
            print("asin: ", self.asin)
            url = "https://www.amazon.com/dp/" + self.asin
            soup = amazon_module.download_soup_by_url(url)

            brand = " "
            try:
                if soup.find(id="bylineInfo"):
                    brand = soup.find(id="bylineInfo").get_text().strip()
                if soup.find(id="brand"):
                    brand = soup.find(id="brand").get_text().strip()
            except:
                pass
            print("brand:", brand)

            badge = " "
            try:
                if soup.find(id="acBadge_feature_div").find("div", class_="ac-badge-wrapper"):
                    badge = " ".join(soup.find(id="acBadge_feature_div").find("div", class_="ac-badge-wrapper").get_text().strip().split())
                    badge = badge.replace("Amazon's Choice recommends highly rated, well-priced products available to ship immediately. ", "", 1)
            except:
                pass
            print("badge:", badge)

            title = " "
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
                variation_name = " ".join(variation_name.split())
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
                    for bullets_content in bullets_contents:
                        print(bullets_content.get_text().strip())
                        #toys
                        if bullets_content.span:
                            continue
                        bullets_list.append(bullets_content.get_text().strip())
                        bullets = bullets_list

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
                            except:
                                pass
                            try:
                                bullet_2 = bullets[1]
                            except:
                                pass
                            try:
                                bullet_3 = bullets[2]
                            except:
                                pass
                            try:
                                bullet_4 = bullets[3]
                            except:
                                pass
                            try:
                                bullet_5 = bullets[4]
                            except:
                                pass
                            try:
                                bullet_6 = bullets[5]
                            except:
                                pass
                            try:
                                bullet_7 = bullets[6]
                            except:
                                pass
                            try:
                                bullet_8 = bullets[7]
                            except:
                                pass
                            try:
                                bullet_9 = bullets[8]
                            except:
                                pass
                            try:
                                bullet_10 = bullets[9]
                            except:
                                pass
            except:
                pass
            print("bullets_list:", bullets_list)

            a_plus_page = " "
            try:
                if soup.find(id="aplus"):
                    a_plus_page = soup.find(id="aplus").get_text()
                a_plus_page = " ".join(a_plus_page.split())
            except:
                pass
            a_plus_page = re.sub(r"(Product Description.*; } )", "", a_plus_page)
            a_plus_page = re.sub(r"(From the manufacturer.*; } )", "", a_plus_page)
            a_plus_page = a_plus_page.replace("View larger ", "")
            a_plus_page = a_plus_page.replace("Read more ", "")
            print("a_plus_page:", a_plus_page)

            description = " "
            try:
                if soup.find(id="productDescription"):
                    description = soup.find(id="productDescription").get_text()
                description = " ".join(description.split())
            except:
                pass
            description = re.sub(r"(Product Description.*; } )", "", description)
            description = re.sub(r"(From the manufacturer.*; } )", "", description)
            description = description.replace("View larger ", "")
            description = description.replace("Read more ", "")
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
            self.picture_url = picture_url
            self.download_picture_by_url()

            self.listing_info_dict = {
                "asin": self.asin,
                "url": url,
                "brand": brand,
                "best_seller_badge": self.best_seller_badge,
                "badge": badge,
                "title": title,
                "variation_name": variation_name,
                "price": price,
                "sold_by": sold_by,
                "how_many_sellers": how_many_sellers,
                "bullet_1": bullet_1,
                "bullet_2": bullet_2,
                "bullet_3": bullet_3,
                "bullet_4": bullet_4,
                "bullet_5": bullet_5,
                "bullet_6": bullet_6,
                "bullet_7": bullet_7,
                "bullet_8": bullet_8,
                "bullet_9": bullet_9,
                "bullet_10": bullet_10,
                "a_plus_page": a_plus_page,
                "description": description,
                "salesrank": salesrank,
                "review_num": review_num,
                "review_value": review_value,
                "qa_num": qa_num,
                "picture_url": picture_url
                                 }

            return self.listing_info_dict

    def export_asin_of_store(self):
        store_ids = open('./config/STORE', 'r')
        for store_id in store_ids:
            self.start(store_id)

        fileObject = open('./store/asin_of_store.txt', 'w')
        for ip in self.asin_list:
            fileObject.write(ip)
            fileObject.write('\n')
        fileObject.close()

    def start(self, store_url):
        try:
            # get storefront_id
            storefront_url_temp = store_url
            storefront_id = ""
            try:
                storefront_id = re.search(r"seller=(.*?)&", storefront_url_temp).group(1)
            except:
                pass
            try:
                storefront_id = re.search(r"merchant=(.*?)&", storefront_url_temp).group(1)
            except:
                pass
            print("storefront_id:", storefront_id)
            self.storefront_url = "https://www.amazon.com/shops/" + storefront_id + "?ref_=v_sp_storefront"


            # main
            store_url_list = self.storefront_url_to_store_url_list()
            all_asin = []
            for index, store_url in enumerate(store_url_list):
                print("store_url:", store_url)
                self.store_url_to_asin_list(store_url)
        except:
            print("fail")

#main function
storefront_to_listing = Storefront_to_listing()
storefront_to_listing.export_asin_of_store()
