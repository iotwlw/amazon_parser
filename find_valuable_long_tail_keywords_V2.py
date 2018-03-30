from amazon_module import amazon_module

keyword_list = [
    "*necklace",
]

long_tail_keyword_dict_list = []

print("根据给定的关键词，获取亚马逊搜索框的提示词做为长尾词；")
print("根据获取的长尾词，获取亚马逊搜索框的提示词作为更长的长尾词；")
print("")

for keyword in keyword_list:

    long_tail_keyword_list = amazon_module.keyword_to_long_tail_keyword_list(keyword)

    for long_tail_keyword in long_tail_keyword_list:
        long_tail_keyword = "*" + long_tail_keyword
        amazon_module.keyword_to_long_tail_keyword_list(long_tail_keyword)
