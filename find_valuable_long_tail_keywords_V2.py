from amazon_module import amazon_module

keyword_list = [
    "*necklace",
]

long_tail_keyword_dict_list = []

print("根据给定的关键词，获取亚马逊搜索框的提示词做为长尾词；")
print("获取长尾词的merchantwords搜索量，亚马逊搜索框下显示的产品数，以及两者的比值；")
print("")

for keyword in keyword_list:

    long_tail_keyword_list = amazon_module.keyword_to_long_tail_keyword_list(keyword)

    for long_tail_keyword in long_tail_keyword_list:
        long_tail_keyword = "*" + long_tail_keyword
        amazon_module.keyword_to_long_tail_keyword_list(long_tail_keyword)

#     for long_tail_keyword in long_tail_keyword_list:
#         print("    long tail keyword:", long_tail_keyword)
#         try:
#             merchantwords_rank = amazon_module.keyword_to_merchantwords_search_rank(long_tail_keyword)
#             merchantwords_rank = merchantwords_rank.replace("<", "").strip()
#         except:
#             pass
#         print("   merchantwords rank:", merchantwords_rank)
#         amazon_search_results = amazon_module.keyword_to_search_results_num(long_tail_keyword)
#         print("amazon search results:", amazon_search_results)
#
#         ratio = ""
#         try:
#             ratio = int(merchantwords_rank)/int(amazon_search_results)
#             ratio = (ratio*100)
#             ratio = str(ratio).split(".")[0]
#             ratio = str(int(ratio)/100)
#             print("                ratio:", ratio)
#         except:
#             pass
#
#         long_tail_keyword_dict = {
#             "long_tail_keyword": long_tail_keyword,
#             "merchantwords_rank": merchantwords_rank,
#             "amazon_search_results": amazon_search_results,
#             "ratio": ratio,
#         }
#         long_tail_keyword_dict_list.append(long_tail_keyword_dict)
#
# print(long_tail_keyword_dict_list)
#
# try:
#     amazon_module.dict_list_to_csv_file(long_tail_keyword_dict_list, "long_tail_keyword_file.csv", "long_tail_keyword_folder")
# except:
#     pass


