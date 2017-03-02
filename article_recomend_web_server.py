from flask import Flask
from article_recommend import find_similar
from article_recommend import fetch_text
import json
import requests

app = Flask(__name__)


@app.route('/<user_id>/<text_id>/similar_by_text')
def similar_by_text(user_id, text_id):
    # http://188.166.174.189:28103/article{?page,size,sort}
    request = requests.get('http://188.166.174.189:28103/article/byUserId/' + user_id + '/unread?page=0&size=20')
    # request = requests.get('http://pocket_square_articles:8080/articles/' + user_id )
    response = request.json()

    article_texts = []
    article_metadata = []
    target_index = None
    for i, elem in enumerate(response):
        try:
            if 'content' not in elem:
                continue
            article_metadata.append(elem)
            article_texts.append(fetch_text(elem['content']))
            del elem['content']
            if elem['id'] == text_id:
                target_index = i
            print 'one articles fetched'
        except Exception:
            print 'something went wrong'

    indices = find_similar(article_texts, target_index, 10)
    recommended_articles = []
    for ind in reversed(indices):
        recommended_articles.append(article_metadata[ind])

    return json.dumps(recommended_articles)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
