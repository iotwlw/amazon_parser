from amazon_module import amazon_module

keyword_list = [
    "cat toy",
    "cat toy ",
    "cat laser",
    "cat light",
    "shock collar",
    "training collar",
    "dog collar",
    "cat collar",
    "Dog Shock Collar",
    "shock collar",
    "dog training collar",
    "shock collar for dogs",
    "cat toys",
    "laser pointer",
]

def keyword_to_long_tail_keyword_list(keyword):
    try:
        print("keyword:", keyword)
        print("-" * (len("keyword: ") + len(keyword)))
        url_head = "https://completion.amazon.com/search/complete?method=completion&mkt=1&r=Y5KKREBZPVVDRZT19HX9&s=133-8959284-8300960&c=&p=Gateway&l=en_US&b2b=0&fresh=0&sv=desktop&client=amazon-search-ui&x=String&search-alias=aps&q="
        url_tail = "&qs=&cf=1&fb=1&sc=1&"
        try:
            keyword = keyword.replace(" ", "%20")
            keyword = keyword.replace("'", "%27")
            url = url_head + keyword + url_tail

            soup = amazon_module.download_soup_by_url(url)

            soup_string = soup.get_text()
            soup_string = soup_string[13:-11]
            soup_list = eval(soup_string)

            long_tail_keyword_list = []
            for long_tail_keyword in soup_list[1]:
                print(long_tail_keyword)
                long_tail_keyword_list.append(long_tail_keyword)

            print("")
            return(long_tail_keyword_list)
        except:
            print("can't find long tail words")
    except:
        print("can't find long tail words")



print("根据给定的词，获取亚马逊搜索框提示词；")
print("")

abc_list = [chr(i) for i in range(97,123)]
abc_with_blank_list = [chr(i) for i in range(97,123)]
abc_with_blank_list.insert(0, "")
abc_with_blank_list.insert(1, " ")
# print(abc_list)
# print(abc_with_blank_list)

for keyword in keyword_list:
    keyword_to_long_tail_keyword_list(keyword)

# for keyword in abc_list:
#     keyword_to_long_tail_keywords(keyword)

# for i in range(0,26):
#     for j in range(0,27):
#         keyword = abc_list[i] + abc_with_blank_list[j]
#         keyword_to_long_tail_keywords(keyword)


