import requests


class Retriever:
    def __init__(self, url):
        self.url = url

    def get_page_source(self):
        return requests.get(self.url).text
