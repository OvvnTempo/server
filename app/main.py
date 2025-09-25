# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from datetime import datetime, timedelta


# Load environment variables
# load_dotenv("../.env")
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not GEMINI_API_KEY or not NEWS_API_KEY:
    raise ValueError("API keys not found in .env")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

BASE_URL = "https://newsapi.org/v2/everything"

# Pydantic model for POST request
class QueryRequest(BaseModel):
    user_input: str

# Initialize FastAPI app
app = FastAPI(title="NewsURL Finder API")

def refine_query(user_input: str) -> str:
    """Uses Gemini to convert natural language into a NewsAPI query string."""
    prompt = f"""
    Convert the following user request into a concise and effective query for the NewsAPI 'q' parameter.

    Follow these requirements strictly:
    - The output must ONLY be the query string. Do not include any other text, labels, or explanations.
    - Use keywords and short phrases.
    - Use quotes " " for exact phrase matches (e.g., "artificial intelligence").
    - Use the '+' prefix for mandatory terms.
    - Use the '-' prefix to exclude terms.
    - Use boolean operators like AND, OR, NOT and parentheses for complex logic.
    - The final query must not exceed 500 characters.

    User input: {user_input}"""
    try:
        response = model.generate_content(prompt)
        # It's good practice to add validation or error handling here
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise HTTPException(status_code=500, detail="Failed to refine query with AI model.")

def get_latest_article(query: str) -> dict:
    """Fetches the most relevant article from NewsAPI based on the query."""
    # --- FIX: Use a dynamic date range (e.g., the last 2 days) ---
    # This makes the search more robust than a fixed future date.

    to_date = datetime.now()
    from_date = to_date - timedelta(days=2)
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "q": query,
        "from": from_date.strftime('%Y-%m-%d'), # Format date as YYYY-MM-DD
        "to": to_date.strftime('%Y-%m-%d'),
        "sortBy": "relevancy", # 'relevancy' is a good default
        "pageSize": 1 # We only want the top article
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    articles = data.get("articles", [])
    if not articles:
        return {"query": query, "url": None, "message": "No articles found"}

    return {"query": query, "url": articles[0]["url"], "title": articles[0]["title"]}


# POST endpoint to search for an article
@app.post("/search")
def search_article(request: QueryRequest):
    """
    This endpoint takes a user's natural language query, refines it using
    an AI model, and fetches the most relevant news article URL.
    """
    if not request.user_input:
        raise HTTPException(status_code=400, detail="user_input cannot be empty.")
        
    # 1. Refine the user's input into a search query using Gemini
    refined_query = refine_query(request.user_input)
    
    # 2. Fetch the latest article from NewsAPI using the refined query
    result = get_latest_article(refined_query)
    
    return result

# GET endpoint for health check or simple testing
@app.get("/")
def root():
    return {"message": "NewsURL Finder API is running! Use the /docs endpoint to test the POST /search route."}

