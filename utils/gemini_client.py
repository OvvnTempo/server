import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure the Gemini client
genai.configure(api_key=api_key)

# Choose the model (Gemini Flash 2.5)
model = genai.GenerativeModel("gemini-2.5-pro")


def refine_query(user_input: str) -> str:
    """
    Uses Gemini to refine user input into a NewsAPI-compatible 'q' query.
    """
    prompt = f"""
    Convert the following user request into a concise query for NewsAPI's 'q' parameter.

    Requirements:
    - Must be 500 characters or fewer.
    - Use only keywords or phrases relevant to the user input.
    - You may use:
        * Quotes " " for exact matches
        * +word for mandatory terms
        * -word for excluded terms
        * AND / OR / NOT for logic
        * Parentheses for grouping
    - Do NOT include explanations, formatting, or extra text.
    - Output only the query string, nothing else.

    User input: {user_input}
    """

    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    user_input = input("Enter your topic: ")
    query = refine_query(user_input)
    print(f"\nRefined NewsAPI query: {query}")

if __name__ == "__main__":
    main()