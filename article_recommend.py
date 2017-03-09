import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import urllib2
import re


def find_similar(articles, post_ind, count):
    tfidf = TfidfVectorizer(stop_words='english').fit_transform(articles)
    cosine_dist = cosine_similarity(tfidf[post_ind], tfidf).flatten()
    ind_dist_arr = sorted(enumerate(cosine_dist), reverse=True, key=lambda x: x[1])[:count]
    return ind_dist_arr


def fetch_text(text):
    text = BeautifulSoup(text)
    to_extract = text.findAll('script')
    for item in to_extract:
        item.extract()
    to_extract = text.findAll('style')
    for item in to_extract:
        item.extract()

    text = text.get_text()
    text = re.sub('(\n)+', '\n', text)

    re.sub("\n(\n)*", "\n", text)
    return text.encode('utf-8')
