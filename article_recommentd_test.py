import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup

from sklearn.datasets import fetch_20newsgroups

import urllib2


def find_similar(articles, post_ind, count):
    tfidf = TfidfVectorizer(stop_words='english').fit_transform(articles)
    cosine_dist = cosine_similarity(tfidf[post_ind], tfidf).flatten()
    ind_dist_arr = sorted(enumerate(cosine_dist), reverse=True, key=lambda x: x[1])[:count]
    return ind_dist_arr

article_file = open('../pocket-square-ingest/articles.json', 'r')
article_map = json.loads(article_file.read())
article_texts = []
article_titles = []
for l in article_map.keys():
    try:
        f = open('../pocket-square-ingest/articles/' + l + '.txt', 'r')
        article_texts.append(f.read())
        article_titles.append(article_map[l]['resolved_title'])
        f.close()
    except Exception:
        pass

article_file.close()


ind_dist_arr = find_similar(article_texts, 64, 50)

for ind, dist in ind_dist_arr:
    print article_titles[ind], dist, ind
