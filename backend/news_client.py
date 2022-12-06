""" This class implements the client method to read articles from news API platforms """
from news_auth import NewsApiAuth, NewsDataAuth
import requests
import constants


class NewsClient(object):
    """
    Accept all API keys and do initialization
    """

    def __init__(self, newsapi_key, gnews_key, newsdata_key):
        self.newsApiAuth = NewsApiAuth(api_key=newsapi_key)
        self.newsDataAuth = NewsDataAuth(api_key=newsdata_key)
        self.gnewsAuth = gnews_key
        self.request_method = requests

    def getNewsArticles(self, date: object) -> object:
        """
        Returns
        """

        payload = [self.getNewsFromNewsApi(date), self.getNewsFromGnews(date), self.getNewsFromNewsData(date)]

        return payload

    def getNewsFromNewsApi(self, date):
        """ Restrict the articles only to english and USA. """
        req = {
            "from": date,
            "to": date,
            "sources": "bloomberg,business-insider,financial-post,fortune,the-wall-street-journal",
        }

        resp = self.request_method.get(constants.NEWS_API_BASE_URL + "/everything", auth=self.newsApiAuth, timeout=30,
                                       params=req)
        # Check Status of Request, if no response then return empty response. This is to avoid any issues with other
        # two.
        print(resp.content)
        if resp.status_code != requests.codes.ok:
            return []

        matchingArticles = []
        count = 0
        responseJson = resp.json()

        for article in responseJson["articles"]:
            formatted = {"id": count}
            count += 1
            formatted["title"] = article["title"]
            formatted["content"] = article["content"]
            formatted["url"] = article["url"]
            formatted["description"] = article["description"]

            matchingArticles.append(formatted)

        return matchingArticles

    def getNewsFromGnews(self, date):
        # Restrict the articles only to english and USA.
        req = {
            "q": "market OR business OR stocks OR invest",
            "from": date,
            "to": date,
            "country": "us",
            "language": "en",
            "token": self.gnewsAuth
        }

        resp = self.request_method.get(constants.GNEWS_BASE_URL + "/search", timeout=30,
                                       params=req)
        # Check Status of Request, if no response then return empty response. This is to avoid any issues with other
        # two.
        # print(resp.content)
        if resp.status_code != requests.codes.ok:
            return []

        matchingArticles = []
        count = 0
        responseJson = resp.json()
        for article in responseJson["articles"]:
            formatted = {"id": count}
            count += 1
            formatted["title"] = article["title"]
            formatted["content"] = article["content"]
            formatted["description"] = article["description"]
            formatted["url"] = article["url"]

            matchingArticles.append(formatted)

        return matchingArticles

    def getNewsAllNews(self, date):
        """
        This Method returns data for all news in all three sources
        """
        articles = []
        newsdata = self.getNewsFromNewsData(date)
        articles += newsdata
        newsapi = self.getNewsFromNewsApi(date)
        articles += newsapi
        newsgnews = self.getNewsFromGnews(date)
        articles += newsgnews
        return articles

    """
    Request to get news articles from archive and respond structure which has a headline and main content
    """

    def getNewsFromNewsData(self, date):
        # Restrict the articles only to english and USA.
        req = {
            "from_date": date,
            "to_date": date,
            "country": "us",
            "language": "en",
            "category": "business,top"
        }

        resp = self.request_method.get(constants.NEWS_DATA_BASE_URL + "/archive", auth=self.newsDataAuth, timeout=30,
                                       params=req)
        # Check Status of Request, if no response then return empty response. This is to avoid any issues with other
        # two.
        print(resp.content)
        if resp.status_code != requests.codes.ok:
            return []

        matchingArticles = []
        count = 0
        responseJson = resp.json()
        for article in responseJson.results:
            formatted = {"id": count}
            count += 1
            formatted["title"] = article["title"]
            formatted["content"] = article["content"]
            formatted["url"] = article["url"]

            matchingArticles.append(formatted)

        return matchingArticles
