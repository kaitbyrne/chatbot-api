import unittest
import requests
from skills.news import news_helper


class TestNews(unittest.TestCase):

    def test_api_call(self):

        url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=aab38de72c3a43f09663d59405f99b8b')
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

    def news_test(self):

        news = news_helper()
        self.assertTrue(news)
