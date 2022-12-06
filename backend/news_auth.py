"""
This file contains authentication header population classes. For GNews.io we need to provide the apiKey in query param so
the class is not implemented
 """

from requests.auth import AuthBase


class NewsApiAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        request.headers.update(get_auth_headers(self.api_key))
        return request


class NewsDataAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        request.headers.update({"Content-Type": "Application/JSON", "X-ACCESS-KEY": self.api_key})
        return request


def get_auth_headers(api_key):
    return {"Content-Type": "Application/JSON", "Authorization": api_key}
