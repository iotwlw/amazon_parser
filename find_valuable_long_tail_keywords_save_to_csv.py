from amazon_module import amazon_module
import os
import copy

# change to yours
# Note: you can input keyword starts with '*' to match more results
keyword_list = [
    "dog collars",
]

def save_list_to_csv(csv_folder, csv_file_name):
    csv_file_path = csv_folder + csv_file_name
    try:
        if not os.path.exists(csv_folder):
            os.mkdir(csv_folder)
            print("success to create folder")
    except:
        pass

    with open(csv_file_path, 'w', encoding='utf8', newline='') as f:
        for item in all_long_tail_keyword_list:
            f.write(item + "\n")
        print("success to write csv content")



print("根据给定的关键词，获取亚马逊搜索框的提示词做为长尾词；")
print("根据获取的长尾词，获取亚马逊搜索框的提示词作为更长的长尾词；")
print("")

for keyword in keyword_list:

    all_long_tail_keyword_list = []
    csv_folder = "long_tail_keyword/"
    keyword_underline = keyword.replace(" ", "_").replace("*", "[star]")
    csv_file_name = keyword_underline + ".csv"

    long_tail_keyword_list_1 = amazon_module.keyword_to_long_tail_keyword_list(keyword)
    all_long_tail_keyword_list.extend(copy.deepcopy(long_tail_keyword_list_1))

    for long_tail_keyword in long_tail_keyword_list_1:
        long_tail_keyword_list_2 = amazon_module.keyword_to_long_tail_keyword_list("*" + long_tail_keyword)
        all_long_tail_keyword_list.extend(copy.deepcopy(long_tail_keyword_list_2))

    save_list_to_csv(csv_folder, csv_file_name)



