import requests
from bs4 import BeautifulSoup
import re
import random
from datetime import datetime
import csv
import os
# from amazon_module import amazon_module

def download_soup_by_url(url):
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
    proxies = random.choice(usa_proxies_list)
    # proxies = random.choice(china_proxies_list)
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
    # soup = BeautifulSoup(r.content, 'html5lib')
    return soup

def first_store_url_to_store_urls(store_frontpage_url, pages=1):
    pages_urls_list = []
    pages_urls_list.append(store_frontpage_url)
    if pages == 1:
        return pages_urls_list
    while pages > 1:
        # seed_url = pages_urls_list[-1]
        soup = download_soup_by_url(pages_urls_list[-1])
        try:
            if soup.find(id="pagnNextLink")["href"]:
                next_page_url_part2 = soup.find(id="pagnNextLink")["href"]
                next_page_url = "https://www.amazon.com" + next_page_url_part2
                print(next_page_url_part2)
                pages_urls_list.append(next_page_url)
        except:
            return pages_urls_list

        pages = pages - 1

    return pages_urls_list

def store_url_to_asins(store_url):
    soup = download_soup_by_url(store_url)

    # lis = soup.find(id="s-results-list-atf").find_all("li")
    # for li in lis:
    #     print(li["id"])


    lis = soup.find_all("li", class_="celwidget")

    # for index, li in enumerate(lis):
        # print(index + 1, li['id'])

    asin_list = []
    for index, li in enumerate(lis):
        asin = li["data-asin"]
        # print(asin)
        # asin = amazon_module.url_to_asin(url)
        asin_list.append(asin)
    return asin_list

def store_frontpage_url_to_asins(store_frontpage_url, pages=1):
    asins_list = []
    store_urls = first_store_url_to_store_urls(store_frontpage_url, pages)
    for page_index, store_url in enumerate(store_urls):
        asin_list = store_url_to_asins(store_url)
        for asin_index, asin in enumerate(asin_list):
            asins_list.append(asin)
            num = "page" + str(page_index + 1) + "-" + str(asin_index + 1)
            print(num, asin)

            # try:
            #     download_picture_by_asin(asin)
            #     print("download picture successfully!")
            # except:
            #     print("fail to download picture......")

    return asins_list

def asin_to_simple_listing_info(asin):
    print("asin: ", asin)
    url = "https://www.amazon.com/dp/" + asin
    soup = download_soup_by_url(url)
    salesrank_1 = " "
    salesrank_2 = " "
    salesrank_3 = " "
    try:
        salesrank_1 = soup.find(id="SalesRank")
        salesrank_1 = salesrank_1.get_text().strip()
        salesrank_1 = re.search('#(\d|,)+', salesrank_1)
        salesrank_1 = salesrank_1.group()
        salesrank_1 = salesrank_1.replace(',', '')
        salesrank_1 = salesrank_1.replace('#', '')
        # print(salesrank_1)
        try:
            lis = soup.find(id="SalesRank").find("ul", class_="zg_hrsr").find_all("li")
            node_salesrank_list = []
            for li in lis:
                node_salesrank = li.get_text().strip()
                node_salesrank = re.search('#(\d|,)+', node_salesrank)
                node_salesrank = node_salesrank.group()
                node_salesrank = node_salesrank.replace(',', '')
                node_salesrank = node_salesrank.replace('#', '')
                node_salesrank_list.append(node_salesrank)
            # print(node_salesrank_list)

            if len(node_salesrank_list) == 1:
                salesrank_2 = node_salesrank_list[0]
            if len(node_salesrank_list) == 2:
                salesrank_2 = node_salesrank_list[0]
                salesrank_3 = node_salesrank_list[1]
        except:
            pass
    except:
        pass

    #kitchen
    try:
        trs = soup.find(id="productDetails_detailBullets_sections1").find_all("tr")
        for tr in trs:
            try:
                th = tr.find("th").get_text().strip()
                if th == "Best Sellers Rank":
                    spans = tr.find("span").find_all("span")
                    span_text_list = []
                    for span in spans:
                        try:
                            span_text = span.get_text()
                            # print("span_text: ", span_text)
                            span_text = re.search('#(\d|,)+', span_text)
                            span_text = span_text.group()
                            span_text = span_text.replace(',', '')
                            span_text = span_text.replace('#', '')
                            span_text_list.append(span_text)
                        except:
                            pass
                    # print("span_text_list: ", span_text_list)
                    if len(span_text_list) == 1:
                        salesrank_1 = span_text_list[0]
                    if len(span_text_list) == 2:
                        salesrank_1 = span_text_list[0]
                        salesrank_2 = span_text_list[1]
                    if len(span_text_list) == 3:
                        salesrank_1 = span_text_list[0]
                        salesrank_2 = span_text_list[1]
                        salesrank_3 = span_text_list[2]


            except:
                pass
    except:
        pass

    print("salesrank_1: ", salesrank_1)
    print("salesrank_2: ", salesrank_2)
    print("salesrank_3: ", salesrank_3)


    review_num = "0"
    try:
        review_num = soup.find(id="acrCustomerReviewText").get_text().split()[0].strip()
        # print("review_num: ", type(review_num))
    except:
        pass

    review_value = "0"
    try:
        review_value = soup.find(class_="arp-rating-out-of-text").get_text().strip()
        review_value = re.search('(.*?)\s', review_value)
        review_value = review_value.group()
        review_value = review_value.strip()
        # print("review_value: ", type(review_value))
    except:
        pass

    review_value_and_star = review_num + "/" + review_value
    print(review_value_and_star)

    store_salesrank_and_review_star_dict = {
                                            "asin" : asin,
                                            "salesrank_1" : salesrank_1,
                                            "salesrank_2" : salesrank_2,
                                            "salesrank_3" : salesrank_3,
                                            "review_value_and_star" : review_value_and_star,
                                            }
    return store_salesrank_and_review_star_dict

def dict_list_to_csv_file(csv_file_name, dict_list):
    print("***********************************")
    print("start to write csv file...")
    headers = []
    for i in dict_list[0]:
        headers.append(i)

    csv_folder = "store_salesrank_reviewstar"
    csv_file_path = csv_folder + "/" + str(csv_file_name) + ".csv"

    if not os.path.exists(csv_folder):
        print("***********************************")
        print("picture folder not exist, create the folder now...")
        os.mkdir(csv_folder)
        print("success to create picture folder")

    try:
        with open(csv_file_path, 'w', encoding='utf8', newline='') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(dict_list)
            print("success to write csv file...")
    except:
        print("fail to write csv!")

csv_file_name = str(datetime.now()).replace(":", ";").strip().split(".")[0]
start_time = datetime.now()

print("根据亚马逊店铺storefront的链接，获取该店铺产品的review数量星星，salesrank；")
print("")

# store front url
# 修改成你想要的店铺首页网址
store_url = "https://www.amazon.com/s?marketplaceID=ATVPDKIKX0DER&me=A2FQ5GG01HBOZ1&merchant=A2FQ5GG01HBOZ1&redirect=true"
print("store_url:", store_url)

pages = 1
asin_list = store_frontpage_url_to_asins(store_url, pages)

all_asin_list = []
for asin in asin_list:
    url = "https://www.amazon.com/dp/" + asin
    soup = download_soup_by_url(url)
    try:
        lis = soup.find("ul", role="radiogroup").find_all("li")
        for li in lis:
            print(li['data-defaultasin'])
            all_asin_list.append(li['data-defaultasin'])
    except:
        print(asin)
        all_asin_list.append(asin)

print("total ", len(all_asin_list), " asin.")

dict_list = []
for asin in all_asin_list:
    dict_list.append(asin_to_simple_listing_info(asin))
    try:
        pass
    except:
        pass
print(dict_list)

dict_list_to_csv_file(csv_file_name, dict_list)

end_time = datetime.now()
how_many_seconds = end_time - start_time
print(start_time)
print(end_time)
print(str(how_many_seconds.total_seconds()) + "seconds")


