# abc_list = [chr(i) for i in range(0, 256)]
# print(abc_list)

# def is_prime(num):
#     if num <= 1:
#         return False
#     for i in range(2, int(num**0.5)+1):
#         if not num%i:
#             return False
#     return True
#
# # is_prime(10)
# for j in range(1000000):
#     if is_prime(j):
#         print(j)


# color_list = ['black', 'white', 'black', 'white', 'white', 'black']
# # color_filter = "black"
# # color_filter = "white"
# color_filter = "black or white"
# for index, color in enumerate(color_list):
#     if color in color_filter:
#         print(index+1, color)

import math

def cut_unwanted_tail(num):
    return int(num*100)/100

def fba_fee_calc(length, width, height, weight):

    if not length and not width and not height and not weight:
        return None
    if length<=0 or width<=0 or height<=0 or weight<=0:
        return None

    len1 = cut_unwanted_tail(max(length, width, height))
    len3 = cut_unwanted_tail(min(length, width, height))
    len2 = cut_unwanted_tail((length + width + height) - len1 - len3)
    girth = (len2 + len3) * 2

    print(len1, "in")
    print(len2, "in")
    print(len3, "in")
    print(weight, "lb")


    unit_weight = weight
    dimensional_weight = math.ceil(len1*len2*len3/166)
    packaging_weight_1 = 0.25
    packaging_weight_2 = 1
    final_weight_1 = math.ceil((max(unit_weight, dimensional_weight) + packaging_weight_1))
    final_weight_2 = math.ceil((max(unit_weight, dimensional_weight) + packaging_weight_2))

    if len1<15 and len2<12 and len3<0.75 and weight<(12/16):
        size_tier = "small_standard_size"
    elif len1<18 and len2<14 and len3<8 and final_weight_1<(20-4/16):
        size_tier = "large_standard_size"
    elif len1<60 and len2<30 and (len1+girth)<130 and final_weight_2<(70-1):
        size_tier = "small_oversize"
    elif len1<108 and (len1+girth)<130 and final_weight_2<(150-1):
        size_tier = "medium_oversize"
    elif len1<108 and (len1+girth)<165 and final_weight_2<(150-1):
        size_tier = "large_oversize"
    else:
        size_tier = "special_oversize"
    print(size_tier)


    if size_tier == "small_standard_size":
        fba_fee = 2.39
    elif size_tier == "large_standard_size":
        if final_weight_2 <= 1:
            fba_fee = 2.88
        elif final_weight_2 <=2:
            fba_fee = 3.96
        else:
            fba_fee = 3.96 + 0.35 * (final_weight_2 - 2)
    elif size_tier == "small_oversize":
        if final_weight_2 <= 2:
            fba_fee = 6.85
        else:
            fba_fee = 6.69 + 0.35 * (final_weight_2 - 2)
    elif size_tier == "medium_oversize":
        if final_weight_2 <= 2:
            fba_fee = 8.73
        else:
            fba_fee = 8.73 + 0.35 * (final_weight_2 - 2)
    elif size_tier == "large_oversize":
        if final_weight_2 <= 2:
            fba_fee = 69.5
        else:
            fba_fee = 69.5 + 0.76 * (final_weight_2 - 2)
    elif size_tier == "special_oversize":
        if final_weight_2 <= 2:
            fba_fee = 131.44
        else:
            fba_fee = 131.44 + 0.88 * (final_weight_2 - 2)


    return fba_fee


length = 10
width = 20
height = 5.9
weight = 1
fba_fee = fba_fee_calc(length, width, height, weight)
print("FBA fee: $" + str(fba_fee))


{
    "orderId":"114-8985947-6381866",
    "legacyOrderItemId":"66310165735482",
    "orderItemId":"17442876240361",
    "asin":"B076JBM7C6",
    "title":"Personalized Dog Collar, Custom Engraving with Pet Name and Phone Number, Adjustable Tough Nylon ID Collar, Matching Leash Available Separately (Peafowl)",
    "merchantId":"A8E7LT0GUPMN2",
    "quantity":1,
    "version3.0":{
        "customizationInfo":{
            "surfaces":[
                {
                    "name":"Surface 1",
                    "areas":[
                        {
                            "colorName":"111","fontFamily":"timesbd","Position":{"x":278,"y":284},"name":"Customization 2","Dimensions":{"width":106,"height":11},"label":"Line 1","fill":"#111","customizationType":"TextPrinting","text":"Cash"},{"colorName":"111","fontFamily":"timesbd","Position":{"x":272,"y":319},"name":"Customization 3","Dimensions":{"width":110,"height":13},"label":"Line 2","fill":"#111","customizationType":"TextPrinting","text":"615-516-1432"},{"colorName":"111","fontFamily":"timesbd","Position":{"x":273,"y":353},"name":"Customization 4","Dimensions":{"width":106,"height":13},"label":"Line 3（X-S is not suitable for this line）","fill":"#111","customizationType":"TextPrinting","text":"615-879-1120"},{"optionValue":"L","name":"定制 5","priceDelta":{"currency":"USD","value":0},"optionId":"1-3-3","label":"Pls Choose Size","customizationType":"Options","optionImage":"https://m.media-amazon.com/images/S/pc-vendor-gallery-prod/A8E7LT0GUPMN2/options/2017-12-12/f78d6cf4-9613-4c7d-9db9-8c4ac266e0c9.png"}]}]}},"customizationInfo":{"aspects":[{"title":"Line 1","text":{"value":"Cash"},"font":{"value":"timesbd"},"color":{"value":"#111"}},{"title":"Line 2","text":{"value":"615-516-1432"},"font":{"value":"timesbd"},"color":{"value":"#111"}},{"title":"Line 3（X-S is not suitable for this line）","text":{"value":"615-879-1120"},"font":{"value":"timesbd"},"color":{"value":"#111"}},{"title":"Pls Choose Size","text":{},"font":{},"color":{}}]},"version":"2.0"}
