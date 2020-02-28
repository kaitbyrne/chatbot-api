import unittest
import urllib
import requests
from skills.weather import weather_helper


class TestWeather(unittest.TestCase):

    def test_api_call(self):

        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select item.condition from weather.forecast where woeid=2377942"
        yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
        response = requests.get(yql_url)

        self.assertEqual(response.status_code, 200)

    def degrees_test(self):

        weather = weather_helper()
        self.assertIn('degrees', weather)

    def conditions_test(self):

        weather = weather_helper()
        self.assertIn('It is currently', weather)
