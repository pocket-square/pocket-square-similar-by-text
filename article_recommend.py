import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
import urllib2
import re


def find_similar(article_texts, post, count):
    tfidf = TfidfVectorizer().fit_transform(article_texts)
    # print type(tfidf)
    # pairwise_similarity = tfidf * tfidf.T
    cosine_similarities = linear_kernel(tfidf[post:post+1], tfidf).flatten()
    # print pairwise_similarity.A
    related_docs_indices = cosine_similarities.argsort()[-count:]
    return related_docs_indices

# article_indices = find_similar(article_texts, 0, 10)
#
# for ind in reversed(article_indices):
#     print article_titles[ind]


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
