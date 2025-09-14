from fastapi import FastAPI

app = FastAPI(title="Newsletter Recommender")

@app.get("/")
def root():
    return {"message": "Hello, this is the newsletter backend!"}

@app.post("/newsletter")
def get_newsletter(prompt: dict):
    user_prompt = prompt.get("prompt", "")
    # Placeholder logic - later call Gemini / News API
    return {"newsletter": f"Best newsletter for: {user_prompt}"}