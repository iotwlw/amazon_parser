# coding: utf-8
# 用于通过品牌搜索

import re
from amazon_module import amazon_module
import os
import csv
import random
import time


class Keyword_to_listing():
    def __init__(self):

        self.csv_folder = "brand/"
        self.csv_file_name = "brand_huaqiangbei.csv"
        self.listing_info_dict = dict()

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
                with open(csv_file_path, 'wb') as f:
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

    def keyword_to_asin_list(self):
        print("brand_to_asin_list is running...")
        brands = open('./brands', 'r')
        brand_list = []
        for brand in brands:
            try:
                base_url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
                keyword_with_plus = "+".join(brand.split())
                first_page_url = base_url + keyword_with_plus
                get_url_sleep_time = random.randint(0, 5)
                soup = amazon_module.download_soup_by_url(first_page_url)
                tag_content = soup.get_text().encode("utf-8")
                if re.search(r"No results for", tag_content):
                    self.listing_info_dict["brand"] = brand
                    self.listing_info_dict["serch_url"] = first_page_url
                    self.listing_info_dict["state"] = 'no results'
                else:
                    self.listing_info_dict["brand"] = brand
                    self.listing_info_dict["serch_url"] = first_page_url
                    self.listing_info_dict["state"] = 'yes'
                try:
                    self.listing_info_dict_to_csv_file()
                except:
                    pass
                time.sleep(get_url_sleep_time)

            except Exception as e:
                print("{}".format(e))


# main function
keyword_to_listing = Keyword_to_listing()
keyword_to_listing.keyword_to_asin_list()
