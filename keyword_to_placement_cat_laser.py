import requests
from bs4 import BeautifulSoup
import re
import random
import os
import csv
import time
from datetime import datetime

class Keyword_placement():

    def __init__(self):
        # 这里填你要查排名的ASIN，注意英文引号，英文逗号，每行必须左对齐！
        self.asin_list = [
            "B077TKHYPB",
            "B0752DDFMJ",
            "B0753FD7N9",
            "B076RKZ2JL",
        ]
        # 这里填你要查排名的关键词，注意英文引号，英文逗号，每行必须左对齐！
        self.keyword_list = [
            "cat toy light",
            "cat toy interactive",
            "cat toys interactive",
            "cat laser pointer",
            "cat toy interactive laser",
            "cat toys interactive laser",
            "cat chasing toy",
            "cat chase toy",
            "cat chaser",
            "cat light pointer",
            "cat toy laser",
            "cat laser toy",
            "laser pointer for cats",
            "laser pointer for dogs",
            "laser pointer cat toy",
            "cat light toy",

            "cat laser",
            "cat light",
            "cat toy",
            "cat toys",

            # B0752DDFMJ
            "Cat Chaser Toys",
            "Interactive LED Light",
            "Chase Laser Cat Toys",
            "interactive exercise cat toy",

            # B0753FD7N9
            "Cats Teaser Wand",
            "laser presenter",
            "interactive LED light pointer",
            "led light teaser",
            "red focused light",
            # B076RKZ2JL
            "Cat Teaser Wand",
            "Interactive Cat Chaser Toys",
            "Red Light Pointer",
            "red laser pointer",

        ]
        # 选填，不填也可以的，这里填ASIN和SKU对应关系，注意英文引号，英文冒号，英文逗号，每行必须左对齐！
        self.asin_sku_dict = {
            "B077TKHYPB": "PE020-1USF3",
            "B0752DDFMJ": "Myguru",
            "B0753FD7N9": "B Bascolor",
            "B076RKZ2JL": "Quality Star store",
        }
        # 这里填每个关键词搜索的最大页数
        self.max_page = 10
        # 防止爬取太频繁导致亚马逊买家页面不能访问，每爬取一个页面，休息的时间秒数
        self.sleep_time = 1
        # 保存到这个文件夹下
        self.csv_folder = "page rank/cat laser"
        # 下面的不用更改
        self.rank_dict_list = []

        self.csv_file_name = ""

    def download_soup_by_url(self, url):
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
        # r = requests.get(url, headers=headers)
        r = requests.get(url, headers=headers, proxies=proxies)
        # print("Downloading: r.status_code=", r.status_code)
        # print("url: ", url)
        if r.status_code != 200:
            headers = random.choice(headers_list)
            proxies = random.choice(china_proxies_list)
            r = requests.get(url, headers=headers, proxies=proxies)

        soup = BeautifulSoup(r.content, 'html.parser')
        # soup = BeautifulSoup(r.read(), 'html.parser')
        # soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')
        # soup = BeautifulSoup(r.content, 'html5lib')
        time.sleep(self.sleep_time)
        return soup

    def find_the_rank(self, soup, page, keyword):
        if soup:
            lis = soup.find_all("li", class_="s-result-item")
            print("page: ", page)
            for li_index, li in enumerate(lis):
                try:
                    asin = li["data-asin"].strip()
                    for given_asin in self.asin_list:
                        if given_asin.strip() == asin:
                            rank = li_index + 1
                            page_rank = str(page) + "P" + str(rank)
                            sponsored_or_natural_rank = "natural rank"
                            try:
                                if li.find("h5").get_text().strip().split()[0]:
                                    if li.find("h5").get_text().strip().split()[0] == "Sponsored":
                                        sponsored_or_natural_rank = "AD"
                            except:
                                pass
                            sku = "no sku"
                            try:
                                if self.asin_sku_dict[asin]:
                                    sku = self.asin_sku_dict[asin]
                            except:
                                pass
                            print(keyword + ": " + page_rank + ": " + asin + ": " + sku + ": " + sponsored_or_natural_rank)
                            rank_dict = {
                                "asin": asin,
                                "keyword": keyword,
                                "page_rank": page_rank,
                                "sku": sku,
                                "sponsored_or_natural_rank": sponsored_or_natural_rank,
                            }
                            self.rank_dict_list.append(rank_dict)
                except:
                    pass

    def dict_list_to_csv_file(self):
        try:
            print("***********************************")
            print("start to write csv file...")
            headers = []
            for i in self.rank_dict_list[0]:
                headers.append(i)


            csv_file_path = self.csv_folder + "/" + str(self.csv_file_name) + ".csv"

            if not os.path.exists(self.csv_folder):
                print("***********************************")
                print("picture folder not exist, create the folder now...")
                os.mkdir(self.csv_folder)
                print("success to create picture folder")

            try:
                with open(csv_file_path, 'w', encoding='utf8', newline='') as f:
                    f_csv = csv.DictWriter(f, headers)
                    f_csv.writeheader()
                    f_csv.writerows(self.rank_dict_list)
                    print("success to write csv file...")
            except:
                print("fail to write csv!")
        except:
            print("fail to write csv!")

    def keyword_to_something(self, keyword):
        how_many_pages = self.max_page
        base_url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
        first_page_url = base_url + keyword

        page = 1
        # print(page)
        soup = self.download_soup_by_url(first_page_url)
        # print(soup)
        self.find_the_rank(soup, page, keyword)

        while how_many_pages > 1:
            try:
                if soup.find(id="pagnNextLink")["href"]:
                    next_page_url_part2 = soup.find(id="pagnNextLink")["href"]
                    next_page_url = "https://www.amazon.com" + next_page_url_part2
                    page = page + 1

                    soup = self.download_soup_by_url(next_page_url)
                    # print(soup)

                    self.find_the_rank(soup, page, keyword)
            except:
                pass

            how_many_pages = how_many_pages - 1

    def get_keyword_placement(self):
        self.csv_file_name = str(datetime.now()).replace(":", ";").strip().split(".")[0]
        start_time = datetime.now()
        for keyword in self.keyword_list:
            print("keyword:", keyword)
            self.keyword_to_something(keyword)
        self.dict_list_to_csv_file()

        end_time = datetime.now()
        how_many_seconds = end_time - start_time
        print(start_time)
        print(end_time)
        print(str(how_many_seconds.total_seconds()) + "seconds")

#main function
print("获取给定ASIN在给定关键词下的排名（格式：第几页+P+第几名），包含自然排名和广告位排名；")
print("")

keyword_placement = Keyword_placement()
keyword_placement.get_keyword_placement()
