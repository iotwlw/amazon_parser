from amazon_module import amazon_module

# 小类目top100的网址
url = "https://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Squeak-Toys/zgbs/pet-supplies/2975419011/ref=zg_bs_nav_petsupplies_3_2975413011"

# 文件名（不需要填后缀名，默认是.csv结尾）
file_name = "dog squeak toys new releases"

# 下面的不用改
folder = "top100_folder/" + file_name + "/"
asin_list = []
asin_list = amazon_module.top100_node_url_to_asin_list(url)
# print(asin_list)
print("*****************************************")
print("共找到" + str(len(asin_list)) + "个产品ASIN")


listing_info_list = []
try:
    for asin in asin_list:
        try:
            listing_info_list.append(amazon_module.asin_to_listing_info(asin))
            amazon_module.download_picture_by_asin(asin, folder)
            print(listing_info_list)
        except:
            pass

    file_name += ".csv"
    amazon_module.dict_list_to_csv_file(listing_info_list, file_name, folder)
except:
    pass
