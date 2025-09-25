# For NewsAPI 
import os
from dotenv import load_dotenv
import json
from rich import print_json
import requests
import urllib.parse

# Load environment variables
load_dotenv("../.env")
API_TOKEN = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

from newsapi import NewsApiClient
api = NewsApiClient(api_key=API_TOKEN)

# headlines =api.get_top_headlines(sources='bbc-news')
# print(headlines)

# Getting /top-headlines
# api.get_top_headlines()
# api.get_top_headlines(q="hurricane")
# api.get_top_headlines(category="sports")
# api.get_top_headlines(sources="abc-news,ars-technica", page_size=50)

# Getting /everything
# api.get_everything("hurricane OR tornado", sort_by="relevancy", language="en")
# print(api.get_everything("(hurricane OR tornado) AND FEMA", sort_by="relevancy"))

# Getting /sources
# api.get_sources()
# api.get_sources(category="technology")

# api.get_sources(country="ru")
# api.get_sources(category="health", country="us")
# api.get_sources(language="en", country="in")

# query = '"heung min son" AND football NOT injury'
# encoded_q = urllib.parse.quote(query)

encoded_q = urllib.parse.quote('h1b AND "f1 visa" AND trump')
print(encoded_q)
params = {
    "apiKey": API_TOKEN,
    "language": "en",
    "q": encoded_q,
    "from": "2025-09-01",
    "to": "2025-09-25",
    "sortBy": "relevancy",
    "pageSize": 1
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])
    print_json(json.dumps(articles))
    if articles:
        print("Title:", articles[0]["title"])
        print("URL:", articles[0]["url"])
    else:
        print("No articles found.")
else:
    print("Error:", response.status_code, response.text)