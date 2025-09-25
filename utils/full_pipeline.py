import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import urllib.parse
import json
from rich import print_json

# Load environment variables
load_dotenv("../.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

BASE_URL = "https://newsapi.org/v2/everything"

def refine_query(user_input: str) -> str:
    """Use Gemini to turn user input into a short NewsAPI query."""
    prompt = f"""
    Convert the following user request into a concise query for NewsAPI's 'q' parameter.

    Requirements:
    - Only keywords or short phrases
    - May use quotes " " for exact matches
    - May use + for mandatory terms, - for exclusion
    - May use AND / OR / NOT and parentheses
    - Maximum 500 characters
    - Output only the query string, nothing else

    User input: {user_input}
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def get_latest_article(user_input: str) -> dict:
    """Refine user input and fetch the most recent NewsAPI article URL."""
    # 1️⃣ Refine query using Gemini
    query = refine_query(user_input)

    # 2️⃣ URL-encode for safe request
    # encoded_query = urllib.parse.quote(query)
    # print(f"Encoded Query: {encoded_query}")

    # 3️⃣ Call NewsAPI
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "q": query,
        "from": "2025-09-24",
        "to": "2025-09-25",
        "sortBy": "relevancy",
        "pageSize": 1
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise RuntimeError(f"NewsAPI error {response.status_code}: {response.text}")

    data = response.json()
    articles = data.get("articles", [])
    if not articles:
        return {"query": query, "url": None, "message": "No articles found"}

    return {"query": query, "url": articles[0]["url"], "title": articles[0]["title"]}

# Example usage
if __name__ == "__main__":
    user_input = input("Enter your topic: ")
    result = get_latest_article(user_input)
    print_json(json.dumps(result))