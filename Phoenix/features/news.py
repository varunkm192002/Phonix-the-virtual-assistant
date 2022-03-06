import requests
import json



def get_news():
    url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=0de948f7d3294ea7b4166cb4820e9fe3'
    news = requests.get(url).text
    news_dict = json.loads(news)
    articles = news_dict['articles']
    try:

        return articles
    except:
        return False


def getNewsUrl():
    return 'https://newsapi.org/v2/top-headlines?country=in&apiKey=0de948f7d3294ea7b4166cb4820e9fe3'
