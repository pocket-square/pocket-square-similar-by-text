from flask import Flask
from article_recommend import find_similar
from article_recommend import fetch_text
import json
import requests

app = Flask(__name__)


@app.route('/<user_id>/<text_id>/similar_by_text')
def similar_by_text(user_id, text_id):
    request = requests.get('http://188.166.174.189:28103/articles/' + user_id + '/unread')
    # request = requests.get('http://pocket_square_articles:8080/articles/' + user_id )
    response = request.json()

    article_texts = []
    article_metadata = []
    for elem in response[:100]:
        try:
            article_metadata.append(elem)
            article_texts.append(fetch_text(elem['url']))
            print 'one articles fetched'
        except Exception:
            print 'something went wrong'

    indices = find_similar(article_texts, 0, 10)
    recommended_articles = []
    for ind in reversed(indices):
        recommended_articles.append(article_metadata[ind])

    return json.dumps(recommended_articles)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
