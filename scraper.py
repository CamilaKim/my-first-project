from lxml import html
import requests
import pandas as pd

from time import sleep

import json

def ParsingReviews(asin):
    reviews_list = []
    reviews_df = pd.DataFrame()

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    XPATH_REVIEWS = '//div[@data-hook1="review"]'
    XPATH_REVIEW_RATING = './/i[@data-hook="review-star-rating"]//text()'
    XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
    XPATH_REVIEW_AUTHOR = './/span[contains(@class,"a-profile-name")]//text()'
    XPATH_REVIEW_DATE = './/span[@data-hook="review-date"]//text()'
    XPATH_REVIEW_BODY = './/span[@data-hook="review-body"]//text()'

    p_num = 0
    data={}

    for p in range(5):
        while True:
            print('Scraping review page nr. {}'.format(p_num))
            amazon_url = 'https://www.amazon.com/product-reviews/' + asin + '?pageNumber=' + str(p_num) + '&sortBy=recent'
            page = requests.get(amazon_url, headers=headers)
            page_response = page.text.encode('utf-8')
            parser = html.fromstring(page.content)

            xpath_reviews = '//div[@data-hook="review"]'
            reviews = parser.xpath(xpath_reviews)

            if not len(reviews) > 0:
                break
            for review in reviews:
                raw_review_author = review.xpath(XPATH_REVIEW_AUTHOR)
                raw_review_rating = review.xpath(XPATH_REVIEW_RATING)
                raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
                raw_review_date = review.xpath(XPATH_REVIEW_DATE)
                raw_review_body = review.xpath(XPATH_REVIEW_BODY)

                review_dict = {
                                'asin': asin,
                                'page-number': p_num,
                                'review_text': raw_review_body,
                                'review_posted_date': raw_review_date,
                                'review_header': raw_review_header,
                                'review_rating': raw_review_rating,
                                'review_author': raw_review_author,
                               }
                reviews_list.append(review_dict)
                reviews_df = reviews_df.append(review_dict, ignore_index=True)
            p_num += 1
            if p_num > 7:
                break
        data.update({
            'reviews': reviews_list,
        })
        return data

def ReadAsin():
	AsinList = ['B01ETPUQ6E','B017HW9DEW',"B00U8KSIOM"]
	extracted_data = []
	for asin in AsinList:
		print("Downloading and processing page http://www.amazon.com/dp/"+asin)
		extracted_data.append(ParsingReviews(asin))
		sleep(5)
	f = open('a.json','w', encoding='UTF-8', newline='')
	json.dump(extracted_data,f,indent=4,ensure_ascii=False)

if __name__ == '__main__':
	ReadAsin()
