import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
import urllib2

article_file = open('articles.json', 'r')
article_map = json.loads(article_file.read())
article_texts = []
article_titles = []
for l in article_map.keys():
    try:
        f = open('articles/' + l + '.txt', 'r')
        article_texts.append(f.read())
        article_titles.append(article_map[l]['resolved_title'])
        f.close()
    except Exception:
        print 'something went wrong'

article_file.close()


def find_similar(article_texts, post, count):
    tfidf = TfidfVectorizer().fit_transform(article_texts)
    # print type(tfidf)
    # pairwise_similarity = tfidf * tfidf.T
    cosine_similarities = linear_kernel(tfidf[post:post+1], tfidf).flatten()
    # print pairwise_similarity.A
    related_docs_indices = cosine_similarities.argsort()[-count:]
    return related_docs_indices

article_indices = find_similar(article_texts, 0, 10)

for ind in reversed(article_indices):
    print article_titles[ind]
