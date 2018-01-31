# 根据asin爬取前几页的review信息（review标题，内容，作者，星星数，profile链接，留review时间等等）；
# 根据profile链接爬取客户信息，如简评，facebook，youtube等等（如果客户有信息的话）；
# profile里的邮箱暂时获取不到，需要登录亚马逊买家账号才可以看到邮箱（如果客户有添加邮箱的话）；

import requests
from bs4 import BeautifulSoup
import re
import random
import os
import csv
import time
from datetime import datetime
import json

class Asin_to_reviews():

    def __init__(self):
        # 这里填你要爬取得ASIN，注意英文引号，英文逗号，每行必须左对齐！
        self.asin_list = [
            "B071GBGVSQ",
        ]
        # 这里填每个ASIN里review最大爬取页数
        self.max_page = 30
        # recent表示爬取最近时间的review，top表示爬取默认排名高的review
        self.top_or_recent = "recent"
        # all代表所有星级，positive代表好评，critical代表差评
        self.all_or_positive_or_critical = "all"
        # 防止爬取太频繁导致亚马逊买家页面不能访问，每爬取一个页面，休息的时间秒数
        self.sleep_time = 0
        # 下面的不用更改
        self.reviews_dict_list = []
        self.csv_file_name = ""

    def download_soup_by_url(self, url):
        # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        headers_list = [
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0)'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
            {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
            {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}
        ]
        headers = random.choice(headers_list)
        # print("headers: ", headers)
        china_proxies_list = [
            {'http:': 'http://123.56.169.22:3128'},
            {'http:': 'http://121.196.226.246:84'},
            {'http:': 'http://122.49.35.168:33128'},
            {'http:': 'http://124.238.235.135:81'},
            {'http:': 'http://121.40.199.105:80'},
            {'http:': 'http://202.99.99.123:80'},
            {'http:': 'http://61.153.67.110:9999'},
            {'http:': 'http://121.40.213.161:80'},
            {'http:': 'http://121.42.163.161:80'},
            {'http:': 'http://111.13.7.42:81'},
            {'http:': 'http://114.215.103.121:8081'},
            {'http:': 'http://175.11.157.195:80'}
        ]
        usa_proxies_list = [
            {'http:': 'http://40.140.245.109:8080'},
            {'http:': 'http://50.116.12.78:8118'},
            {'http:': 'http://69.85.70.37:53281'},
            {'http:': 'http://35.195.160.37:1244'},
            {'http:': 'http://104.131.122.164:8118'},
            {'http:': 'http://32.115.161.78:53281'},
            {'http:': 'http://165.227.7.51:80'},
            {'http:': 'http://72.169.78.49:87'},
            {'http:': 'http://52.24.67.217:80'},
            {'http:': 'http://209.159.156.199:80'},
            {'http:': 'http://198.35.55.147:443'},
            {'http:': 'http://97.72.129.36:87'},
            {'http:': 'http://152.160.35.171:80'},
            {'http:': 'http://191.96.51.224:8080'},
            {'http:': 'http://45.55.157.204:80'}
        ]
        # proxies = random.choice(usa_proxies_list)
        proxies = random.choice(china_proxies_list)
        # print("proxies: ", proxies)
        # r = requests.get(url, headers=headers)
        r = requests.get(url, headers=headers, proxies=proxies)
        # print("Downloading: r.status_code=", r.status_code)
        # print("url: ", url)
        if r.status_code != 200:
            headers = random.choice(headers_list)
            proxies = random.choice(china_proxies_list)
            r = requests.get(url, headers=headers, proxies=proxies)
            # print("Downloading: r.status_code=", r.status_code)

        soup = BeautifulSoup(r.content, 'html.parser')
        # soup = BeautifulSoup(r.read(), 'html.parser')
        # soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
        # soup = BeautifulSoup(r.content, 'html5lib')
        time.sleep(self.sleep_time)
        return soup

    def dict_list_to_csv_file(self):
        print("***********************************")
        print("start to write csv file...")
        headers = []
        for i in self.reviews_dict_list[0]:
            headers.append(i)

        csv_folder = "review and profile"
        csv_file_path = csv_folder + "/" + str(self.csv_file_name) + ".csv"

        if not os.path.exists(csv_folder):
            print("***********************************")
            print("reviews folder not exist, create the folder now...")
            os.mkdir(csv_folder)
            print("success to create reviews folder")

        try:
            with open(csv_file_path, 'w', encoding='utf8', newline='') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                f_csv.writerows(self.reviews_dict_list)
                print("success to write csv file...")
        except:
            print("fail to write csv!")

    # def get_profile_info(self, url):
    #     profile_author = ""
    #     profile_occupation_location = ""
    #     profile_description = ""
    #     profile_website = ""
    #     profile_facebook = ""
    #     profile_twitter = ""
    #     profile_pinterest = ""
    #     profile_instagram = ""
    #     profile_youtube = ""
    #
    #     profile_soup = self.download_soup_by_url(url)
    #     try:
    #         for i in profile_soup.find_all("script"):
    #             if re.search("window.CustomerProfileRootProps", i.get_text()):
    #                 i = i.get_text().lstrip().splitlines()[0]
    #                 i = i.rstrip().replace("window.CustomerProfileRootProps = ", "")[:-1]
    #                 i = json.loads(i)
    #                 profile_author = i['nameHeaderData']['name'].strip()
    #                 print("profile_author: ", profile_author)
    #                 profile_occupation_location = i['bioData']['occupationLocationList'][0].strip()
    #                 print("profile_occupation_location: ", profile_occupation_location)
    #                 profile_description = i['bioData']['personalDescription'].strip()
    #                 print("profile_description: ", profile_description)
    #                 profile_website = i['bioData']['website']['normalized'].strip()
    #                 print("profile_website: ", profile_website)
    #                 for social_link in i['bioData']['social']['socialLinks']:
    #                     if social_link['type'] == 'facebook':
    #                         profile_facebook = social_link['url']
    #                     if social_link['type'] == 'twitter':
    #                         profile_twitter = social_link['url']
    #                     if social_link['type'] == 'pinterest':
    #                         profile_pinterest = social_link['url']
    #                     if social_link['type'] == 'instagram':
    #                         profile_instagram = social_link['url']
    #                     if social_link['type'] == 'youtube':
    #                         profile_youtube = social_link['url']
    #     except:
    #         pass

    def first_review_url_to_review_info(self, url, asin):
        location = re.search("ref=", url)
        span = location.span()[0]
        first_review_url_part1 = url[:span]

        review_base_url = first_review_url_part1 + "ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&filterByStar=" + self.all_or_positive_or_critical + "&reviewerType=avp_only_reviews&sortBy=" + self.top_or_recent + "&pageNumber="
        first_review_url = review_base_url + str(1)
        first_review_url_soup = self.download_soup_by_url(first_review_url)

        last_page = 1
        try:
            last_page = first_review_url_soup.find(id="cm_cr-pagination_bar").find_all("li", class_="page-button")[-1].get_text()
        except:
            pass
        last_page = int(last_page)
        min_page = min(last_page, self.max_page)

        for page in range(1, min_page+1):
            review_url = review_base_url + str(page)
            try:
                soup = self.download_soup_by_url(review_url)
                review_list = soup.find(id="cm_cr-review_list").find_all("div", {"data-hook":"review"})

                for review_index, review in enumerate(review_list):
                    review_title = review.find("a", {"data-hook":"review-title"}).get_text()
                    review_star_rating = review.find("i", {"data-hook": "review-star-rating"}).get_text()
                    review_author = review.find("a", {"data-hook": "review-author"}).get_text()
                    review_date = review.find("span", {"data-hook": "review-date"}).get_text()
                    review_body = review.find("span", {"data-hook": "review-body"}).get_text()
                    page_rank = "page" + str(page) + "-" + str(review_index + 1)
                    # print("page_rank: ", page_rank)
                    # print("review_title: ", review_title)
                    # get_profile_info(profile_url)

                    profile_author = " "
                    profile_occupation_location = " "
                    profile_description = " "
                    profile_website = " "
                    profile_facebook = " "
                    profile_twitter = " "
                    profile_pinterest = " "
                    profile_instagram = " "
                    profile_youtube = " "
                    profile_rank= " "
                    profile_url_part = review.find("a", {"data-hook": "review-author"})['href']
                    profile_url = "https://www.amazon.com" + profile_url_part
                    # print("profile_url: ", profile_url)
                    profile_soup = self.download_soup_by_url(profile_url)
                    try:
                        for i in profile_soup.find_all("script"):
                            if re.search("window.CustomerProfileRootProps", i.get_text()):
                                i = i.get_text().lstrip().splitlines()[0]
                                i = i.rstrip().replace("window.CustomerProfileRootProps = ", "")[:-1]
                                i = json.loads(i)
                                profile_author = i['nameHeaderData']['name'].strip()
                                print("profile_author: ", profile_author)
                                try:
                                    profile_occupation_location = i['bioData']['occupationLocationList'][0].strip()
                                    print("profile_occupation_location: ", profile_occupation_location)
                                except:
                                    pass
                                try:
                                    profile_description = i['bioData']['personalDescription'].strip()
                                    print("profile_description: ", profile_description)
                                except:
                                    pass
                                try:
                                    profile_website = i['bioData']['website']['normalized'].get_text()
                                    if profile_website == "http://":
                                        profile_website = " "
                                    print("profile_website: ", profile_website)
                                except:
                                    pass
                                try:
                                    for social_link in i['bioData']['social']['socialLinks']:
                                        if social_link['type'] == 'facebook':
                                            profile_facebook = social_link['url']
                                        if social_link['type'] == 'twitter':
                                            profile_twitter = social_link['url']
                                        if social_link['type'] == 'pinterest':
                                            profile_pinterest = social_link['url']
                                        if social_link['type'] == 'instagram':
                                            profile_instagram = social_link['url']
                                        if social_link['type'] == 'youtube':
                                            profile_youtube = social_link['url']
                                except:
                                    pass
                                try:
                                    profile_rank = i['bioData']['topReviewerInfo']['decoratedRank'].strip()
                                    print("profile_rank: ", profile_rank)
                                except:
                                    pass
                    except:
                        pass

                    review_dict = { "page_rank": page_rank,
                                    "asin": asin,
                                    "review_title": review_title,
                                    "review_star_rating": review_star_rating,
                                    "review_author": review_author,
                                    "review_date": review_date,
                                    "review_body": review_body,
                                    "profile_author": profile_author,
                                    "profile_occupation_location": profile_occupation_location,
                                    "profile_description": profile_description,
                                    "profile_website": profile_website,
                                    "profile_facebook": profile_facebook,
                                    "profile_twitter": profile_twitter,
                                    "profile_pinterest": profile_pinterest,
                                    "profile_instagram": profile_instagram,
                                    "profile_youtube": profile_youtube,
                                    "profile_rank": profile_rank,
                                    "profile_url": profile_url
                                   }
                    # print(review_dict)
                    self.reviews_dict_list.append(review_dict)
            except:
                pass

    def asin_to_first_review_url(self, asin):
        listing_url = "https://www.amazon.com/dp/" + asin
        soup = self.download_soup_by_url(listing_url)
        first_review_url_part2 = soup.find(id="dp-summary-see-all-reviews")["href"]
        first_review_url = "https://www.amazon.com" + first_review_url_part2
        return first_review_url

    def get_reviews_by_asin(self, asin):
        try:
            first_review_url = self.asin_to_first_review_url(asin)
            self.first_review_url_to_review_info(first_review_url, asin)
        except:
            pass

    def get_reviews(self):
        self.csv_file_name = str(datetime.now()).replace(":", ";").strip().split(".")[0]
        start_time = datetime.now()

        for asin in self.asin_list:
            self.get_reviews_by_asin(asin)
        self.dict_list_to_csv_file()

        end_time = datetime.now()
        how_many_seconds = end_time - start_time
        print(start_time)
        print(end_time)
        how_many_seconds = str(how_many_seconds.total_seconds()).split(".")[0]
        print(how_many_seconds + " seconds")

#main function
asin_to_reviews = Asin_to_reviews()
asin_to_reviews.get_reviews()
