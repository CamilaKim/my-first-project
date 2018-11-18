# AIM: RETRIEVES THE IMDB DATASET, DOES THE PREPROCESSING AND APPLIES VARIOUS MODELS
import os

import mpld3 as mpld3
import requests
import pandas as pd
from lxml import html
import numpy as np
import matplotlib.pyplot as plt

def WebCrawler(request,asin):
    print("Success")


    reviews_list = []
    reviews_df = pd.DataFrame()

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    XPATH_REVIEWS = '//div[@data-hook1="review"]'
    XPATH_REVIEW_RATING = './/i[@data-hook="review-star-rating"]//text()'
    XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
    XPATH_REVIEW_AUTHOR = './/span[contains(@class,"a-profile-name")]//text()'
    XPATH_REVIEW_DATE = './/span[@data-hook="review-date"]//text()'
    XPATH_REVIEW_BODY = './/span[@data-hook="review-body"]//text()'

    p_num = 1
    r_data = []

    while True:
        print('Scraping review page nr. {}'.format(p_num))
        # amazon_url = 'https://www.amazon.com/product-reviews/' + asin + '?pageNumber=' + str(
        #     p_num) + '&sortBy=recent'
        #
        amazon_url = 'https://www.amazon.com/Halo-Sleepsack-Wearable-Blanket-Heather/product-reviews/' + asin + '?pageNumber=' + str(
    p_num) + '&sortBy=recent'
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
                'page_number': p_num,
                'review_text': raw_review_body,
                'pub_date': raw_review_date,
                'review_header': raw_review_header,
                'review_rating': raw_review_rating,
                'review_author': raw_review_author,
            }
            reviews_list.append(review_dict)
            reviews_df = reviews_df.append(review_dict, ignore_index=True)
            reviews_df.to_csv('test.csv')
            r_data.append(''.join(raw_review_body))
        p_num += 1
        # if p_num > 7:
        #     break
        # data.update({
        #     'reviews': reviews_list,
        # })
        # crawled_data=Review(**data)
        # crawled_data.save()
        # return crawled_data
    result = list(r_data)
    return result

train_path = "aclImdb/train/"  # source data
test_path = "test.csv"  # test data for grade evaluation.
'''
IMDB_DATA_PREPROCESS explores the neg and pos folders from aclImdb/train and creates a output_file in the required format
Inpath - Path of the training samples 
Outpath - Path were the file has to be saved 
Name  - Name with which the file has to be saved 
Mix - Used for shuffling the data 
'''


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    import pandas as pd
    from pandas import DataFrame, read_csv
    import os
    import csv
    import numpy as np

    stopwords = open("stopwords.en.txt", 'r', encoding="ISO-8859-1").read()
    stopwords = stopwords.split("\n")

    indices = []
    text = []
    rating = []

    i = 0

    for filename in os.listdir(inpath + "pos"):
        data = open(inpath + "pos/" + filename, 'r', encoding="ISO-8859-1").read()
        data = remove_stopwords(data, stopwords)
        indices.append(i)
        text.append(data)
        rating.append("1")
        i = i + 1

    for filename in os.listdir(inpath + "neg"):
        data = open(inpath + "neg/" + filename, 'r', encoding="ISO-8859-1").read()
        data = remove_stopwords(data, stopwords)
        indices.append(i)
        text.append(data)
        rating.append("0")
        i = i + 1

    Dataset = list(zip(indices, text, rating))

    if mix:
        np.random.shuffle(Dataset)

    df = pd.DataFrame(data=Dataset, columns=['row_Number', 'text', 'polarity'])
    df.to_csv(outpath + name, index=False, header=True)

    pass


'''
REMOVE_STOPWORDS takes a sentence and the stopwords as inputs and returns the sentence without any stopwords 
Sentence - The input from which the stopwords have to be removed
Stopwords - A list of stopwords  
'''


def remove_stopwords(sentence, stopwords):
    sentencewords = sentence.split()
    resultwords = [word for word in sentencewords if word.lower() not in stopwords]
    result = ' '.join(resultwords)
    return result


'''
UNIGRAM_PROCESS takes the data to be fit as the input and returns a vectorizer of the unigram as output 
Data - The data for which the unigram model has to be fit 
'''


def unigram_process(data):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    vectorizer = vectorizer.fit(data)
    return vectorizer


'''
BIGRAM_PROCESS takes the data to be fit as the input and returns a vectorizer of the bigram as output 
Data - The data for which the bigram model has to be fit 
'''


def bigram_process(data):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    vectorizer = vectorizer.fit(data)
    return vectorizer


'''
TFIDF_PROCESS takes the data to be fit as the input and returns a vectorizer of the tfidf as output 
Data - The data for which the bigram model has to be fit 
'''


def tfidf_process(data):
    from sklearn.feature_extraction.text import TfidfTransformer
    transformer = TfidfTransformer()
    transformer = transformer.fit(data)
    return transformer


'''
RETRIEVE_DATA takes a CSV file as the input and returns the corresponding arrays of labels and data as output. 
Name - Name of the csv file 
Train - If train is True, both the data and labels are returned. Else only the data is returned 
'''


def retrieve_data(name="imdb_tr.csv", train=True):
    import pandas as pd
    data = pd.read_csv(name, header=0, encoding='ISO-8859-1')
    X = data['text']

    if train:
        Y = data['polarity']
        return X, Y

    return X


'''
STOCHASTIC_DESCENT applies Stochastic on the training data and returns the predicted labels 
Xtrain - Training Data
Ytrain - Training Labels
Xtest - Test Data 
'''


def stochastic_descent(Xtrain, Ytrain, Xtest):
    from sklearn.linear_model import SGDClassifier
    clf = SGDClassifier(loss="hinge", penalty="l1", n_iter=20)
    print("SGD Fitting")
    clf.fit(Xtrain, Ytrain)
    print("SGD Predicting")
    Ytest = clf.predict(Xtest)
    return Ytest


'''
ACCURACY finds the accuracy in percentage given the training and test labels 
Ytrain - One set of labels 
Ytest - Other set of labels 
'''


def accuracy(Ytrain, Ytest):
    assert (len(Ytrain) == len(Ytest))
    num = sum([1 for i, word in enumerate(Ytrain) if Ytest[i] == word])
    n = len(Ytrain)
    return (num * 100) / n


'''
WRITE_TXT writes the given data to a text file 
Data - Data to be written to the text file 
Name - Name of the file 
'''


def write_txt(data, name):
    save_path = 'C:/Users/soldesk/aproject/areview/data/'
    completeName= os.path.join(save_path, name)
    data = ','.join(str(word) for word in data)
    file = open(completeName, 'w')
    file.write(data)
    file.close()
    pass


# if __name__ == "__main__":
def SentimentAnalysis(data):
    import time

    start = time.time()
    print("Preprocessing the training_data--")
    print("Done with preprocessing. Now, will retreieve the training data in the required format")
    [Xtrain_text, Ytrain] = retrieve_data("imdb_tr.csv",)
    print("Retrieved the training data. Now will retrieve the test data in the required format")
    Xtest_text = data
    print("Retrieved the test data. Now will initialize the model \n\n")

    print("-----------------------ANALYSIS ON THE INSAMPLE DATA (TRAINING DATA)---------------------------")
    uni_vectorizer = unigram_process(Xtrain_text)
    print("Fitting the unigram model")
    Xtrain_uni = uni_vectorizer.transform(Xtrain_text)
    print("After fitting ")
    print("\n")

    print("-----------------------ANALYSIS ON THE TEST DATA ---------------------------")
    print("Unigram Model on the Test Data--")
    Xtest_uni = uni_vectorizer.transform(Xtest_text)
    print("Applying the stochastic descent")
    Ytest_uni = stochastic_descent(Xtrain_uni, Ytrain, Xtest_uni)
    print(Ytest_uni)
    size_p = len(Ytest_uni)
    unique, count = np.unique(Ytest_uni, return_counts=True)
    result_dict = dict(zip(unique, count))
    result_dict_1= {}
    result_dict_1["a"]=result_dict
    result_dict_1['b']=size_p
    return result_dict_1

    print("Total time taken is ", time.time() - start, " seconds")
    pass

def drawpiechart(val1, val2):
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(aspect="equal"))

    data = [val1, val2]
    categories = ['pos', 'neg']

    def func(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    fig.set_facecolor('xkcd:salmon')
    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data), textprops=dict(color="white"))

    ax.legend(wedges, categories,
              title="categories",
              loc="center left",
              bbox_to_anchor=(0.7, 0.3, 1, 1))

    plt.setp(autotexts, size=20, weight="bold")
    ax.set_title("Analysis of Amazon reviews")
    # plt.show()
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig
