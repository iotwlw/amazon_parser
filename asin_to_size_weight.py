from amazon_module import amazon_module
import json

def asin_to_size_weight(asin):
    # asin = "B075YV1BT8"
    url_head = "https://sellercentral.amazon.com/fba/profitabilitycalculator/productmatches?searchKey="
    url_tail = "&language=en_US&profitcalcToken=p9FcdMuSse7SGDBTzP9EgOn9nuQj3D"
    url = url_head + asin + url_tail

    soup = amazon_module.download_soup_by_url(url)
    soup_text = soup.get_text()
    soup_dict = json.loads(soup_text)
    item_info_dict = soup_dict['data'][0]
    # for k, v in item_info.items():
    #     print(k, ":", v)
    return item_info_dict

asin = "B075YV1BT8"
item_info = asin_to_size_weight(asin)
print("asin:", item_info.get("asin"))
# print("length:", item_info.get("length"))
# print("width:", item_info.get("width"))
# print("height:", item_info.get("height"))
# print("dimensionUnit:", item_info.get("dimensionUnit"))
# print("weight:", item_info.get("weight"))
# print("weightUnit:", item_info.get("weightUnit"))
# print("size:", str(item_info.get("length")) + " * " + str(item_info.get("width")) + " * " + str(item_info.get("height")) + " " + item_info.get("dimensionUnit"))
# print("weight:", str(item_info.get("weight")) + " " + item_info.get("weightUnit"))

length = str(item_info.get("length"))
width = str(item_info.get("width"))
height = str(item_info.get("height"))
print("size:", length + " * " + width + " * " + height + " " + item_info.get("dimensionUnit"))


# asin : B075YV1BT8
# binding : miscellaneous
# dimensionUnit : inches
# dimensionUnitString : inches
# encryptedMarketplaceId :
# gl : gl_pet_products
# height : 4.53
# imageUrl : https://images-na.ssl-images-amazon.com/images/I/614By7g28lL._SCLZZZZZZZ__SL120_.jpg
# isAsinLimits : True
# isWhiteGloveRequired : False
# length : 13.35
# link : http://www.amazon.com/gp/product/B075YV1BT8/ref=silver_xx_cont_revecalc
# originalUrl :
# productGroup :
# subCategory :
# thumbStringUrl : https://images-na.ssl-images-amazon.com/images/I/614By7g28lL._SCLZZZZZZZ__SL80_.jpg
# title : Dog Toys Set Pet Rope Toys Value Pack Puppy Christmas Gift Dog Cotton Chew Toy Assortment 12 Pcs For Small Medium Large Dogs
# weight : 2.05
# weightUnit : pounds
# weightUnitString : pounds
# width : 11.57

# {
#     "data":
#         [
#             {
#                 "asin":"B075YV1BT8",
#                 "binding":"miscellaneous",
#                 "dimensionUnit":"inches",
#                 "dimensionUnitString":"inches",
#                 "encryptedMarketplaceId":"",
#                 "gl":"gl_pet_products",
#                 "height":4.53,
#                 "imageUrl":"https://images-na.ssl-images-amazon.com/images/I/614By7g28lL._SCLZZZZZZZ__SL120_.jpg",
#                 "isAsinLimits":true,
#                 "isWhiteGloveRequired":false,
#                 "length":13.35,
#                 "link":"http://www.amazon.com/gp/product/B075YV1BT8/ref=silver_xx_cont_revecalc",
#                 "originalUrl":"",
#                 "productGroup":"",
#                 "subCategory":"",
#                 "thumbStringUrl":"https://images-na.ssl-images-amazon.com/images/I/614By7g28lL._SCLZZZZZZZ__SL80_.jpg",
#                 "title":"Dog Toys Set Pet Rope Toys Value Pack Puppy Christmas Gift Dog Cotton Chew Toy Assortment 12 Pcs For Small Medium Large Dogs",
#                 "weight":2.05,
#                 "weightUnit":"pounds",
#                 "weightUnitString":"pounds",
#                 "width":11.57}],
#                 "processedDate":"Mon Dec 18 03:55:37 UTC 2017",
#                 "succeed":"true"}


