# 📰 NewsURL Finder API

This is the backend server for our news finder application. Its main job is to take a simple text query from a user, figure out what they're looking for, and find the most relevant recent news article in real time.

This guide will show you how to connect to it and use it.

## Live API Base URL
The API is deployed on Render and is publicly accessible at the following URL:

`https://ovvntempo-server.onrender.com/`

First check if the api works by going to the above url and you should see a message that says:

`"NewsURL Finder API is running! Use the /docs endpoint to test the POST /search route."`

If not, then let me know.

## How to Use the API
There is one **main endpoint** you will need to use to get an article.

### Find an Article (/search)
This is the core feature of the API. You send it a user's search query, and it returns the details of the best matching article.

- **Endpoint:** `/search`  
- **Method:** `POST`  
- **Full URL:**  `https://ovvntempo-server.onrender.com/search`

### Request Body
You must send a **JSON object** in the body of your POST request. It needs to have one key: user_input.

#### Example Input
`
{
  "user_input": "tylenol autism trump"
}
`

#### Success Response
If an article is found, the server will respond with a 200 OK status and a JSON object containing the article's details.

- **query:** The refined search query that was used to find the article.

- **title:** The headline of the article.

- **url:** A direct link to the full article.
- 
- **urlToImage:** A link to the article's thumbnail/header image. You can use this to display an image in the app. This might be null if the article has no image.

#### Example Success Response:

`
{
  "query": "(+tylenol OR +acetaminophen) AND +autism AND +trump",
  "url": "https://gizmodo.com/how-the-world-is-reacting-to-trumps-tylenol-autism-scare-2000663086",
  "urlToImage": "https://gizmodo.com/app/uploads/2025/07/donald-trump-july-16-2025-1200x675.jpg",
  "title": "How the World Is Reacting to Trump’s Tylenol Autism Scare"
}
`

#### "Not Found" Response
If no relevant articles are found for the query, the server will respond with a JSON object like this:

`
{
  "query": "asdfghjkl",
  "url": null,
  "urlToImage": null,
  "message": "No articles found"
}
`

### Testing the API
#### 1. curl Command
You can quickly test the API from your command line using a tool like curl. This is a great way to make sure it's working before you write any mobile app code.

`
curl -X POST "[https://ovvntempo-server.onrender.com/search](https://ovvntempo-server.onrender.com/search)" \
-H "Content-Type: application/json" \
-d '{"user_input": "latest news on trump tylenol autism"}'
`

#### 2. FastAPI's built-in Swagger UI
🔗 **[API Docs](https://ovvntempo-server.onrender.com/docs)** 

1. Open the docs link in your browser.  
2. Scroll down to **POST /search**.  
3. Click the **“Try it out”** button.  
4. Enter your desired query in the **`user_input`** field.  
5. Click **Execute**.  
6. Wait a few seconds for the response (the first request may take longer if the server was asleep).  

### Important Note for Developers
The API is hosted on Render's free tier. If it doesn't receive any requests for 15 minutes, it will go to "sleep". The first request after it has been asleep will be slow (it might take 20-30 seconds). If your first request times out, just try it again immediately, and it will be fast. This is normal behavior for the free hosting plan.

Let me know if you have any questions!
