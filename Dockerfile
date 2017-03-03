FROM python:2-onbuild

EXPOSE 5000
CMD [ "python", "article_recommend_web_server.py" ]
