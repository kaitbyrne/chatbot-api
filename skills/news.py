import requests
import json


def get_news():
    """
    Get a news update from News API
    :return: news json
    """
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=aab38de72c3a43f09663d59405f99b8b')
    response = requests.get(url)
    return response.json()


def news_helper():
    """
    Parse news result
    :return: String with top headline
    """

    news = get_news()
    update = "Latest headline: " + news['articles'][0]['title'] + "\n" + news['articles'][0]['description']
    return update


if __name__ == "__main__":

    print(news_helper())
