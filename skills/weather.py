import configparser
import requests


def get_api_key():
    config = configparser.ConfigParser()
    configFile = "/Users/kaitbyrne/Documents/Projects/chatbot-api/config/config.ini"
    config.read(configFile)
    return config['openweathermap']['api']


def get_weather(location):
    """
    Get weather for location
    :return: weather json
    """
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}".format(location, get_api_key())
    r = requests.get(url)
    return r.json()


def weather_helper():
    """
    Gets the current weather and parses the json result
    :return: a formatted weather string
    """

    weather = get_weather('Chicago')
    conditions = weather['weather'][0]['description']
    temperature = weather['main']['temp']
    location = weather['name']

    curr_weather = 'It is currently %s degrees with %s in %s' % (temperature, conditions, location)
    return curr_weather


if __name__ == "__main__":
    weather_helper()
