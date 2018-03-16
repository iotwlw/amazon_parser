# 根据产品长，宽，高（单位inch），重量（单位lb），计算FBA配送费（单位$）；（亚马逊即将调整FBA运费，该计算器马上作废）
# 修改第83行尺寸，重量信息；

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
