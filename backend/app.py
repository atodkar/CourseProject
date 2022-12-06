"""
This is the main app class which also acts as a web API server.
All configurations are done here.
"""

from flask import Flask, render_template, request, Response
import os
import json
import constants
from news_client import NewsClient
from topic_extractor import TopicExtractor

# Set the template and static folder to the client build
app = Flask(__name__, template_folder="../frontend/build", static_folder="../frontend/build/static")

app.config['SECRET_KEY'] = '12345'
app.config['SITE'] = "http://0.0.0.0:5000/"
app.config['DEBUG'] = True

# Initialize news client with keys
news_client = NewsClient(constants.NEWSAPI_KEY, constants.GNEWS_KEY,
                         constants.NEWSDATA_KEY)
# Initialize topic extractor
topic_extractor = TopicExtractor()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """
    This is a react-router catch all route
    """
    return render_template('index.html')


@app.route('/news', methods=['GET'])
def getNews():
    """
    Main API which accepts date and returns the major topics along with the news on that day.
    """
    if request.method == 'GET':
        if request.args["date"] == '':
            res = [{"id": 1, "content": "Please provide input date"}]
            return Response(json.dumps(res))
        date = request.args["date"]
        print('date: ', date)

        matching_articles = news_client.getNewsAllNews(date)

        content = ""
        for article in matching_articles:
            content += article["title"] + article["content"] + article["description"]

        if content != "":
            top_topics = topic_extractor.getTopTopicsForTheArticle(content)
        else:
            top_topics = ""

        returned_data = {
            'articles': matching_articles,
            'topics': top_topics
        }

        return Response(json.dumps(returned_data))


@app.route('/relevance', methods=["POST"])
def submitRelevance():
    """
    Post the relevance feedback
    """
    if request.method == 'POST':
        # We are simply printing the relevance at this time.
        # The relevant feedback can be used for further optimizing the job. Its not in the scope of this project.
        print(request.json)
        return_data = {
            "status": "SUCCESS"
        }
        return Response(json.dumps(return_data))


if __name__ == '__main__':
    """
    Main method which takes care of web container
    """
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
