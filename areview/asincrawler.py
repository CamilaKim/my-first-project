import os
import re
import requests
from bs4 import BeautifulSoup

def asinCrawler(request):
    print("Success")
    keyword = request.POST.get('keywords')
    p_num = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    asin_list = []

    while True:
        print('Scraping product page nr. {}'.format(p_num))
        url = 'https://www.amazon.com/s/ref=nb_sb_noss_?url=search-alias%3Daps&field-keywords='+ keyword + '&page=' + str(p_num)
        # url = "https://www.amazon.com/s/ref=nb_sb_noss_?url=search-alias%3Daps&field-keywords=teapot&page=1"

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml', exclude_encodings='utf-8')

        asin = soup.find_all('li', {"class": "s-result-item"})

        for p_asin in asin:
            pp_asin = p_asin.get('data-asin')
            if pp_asin == None:
                pass
            else:
                asin_list.append(pp_asin)

        print(asin_list)
        p_num += 1
        if p_num > 1:
            break

    return asin_list
