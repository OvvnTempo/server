NewsURL Finder API
Hey! This is the backend server for our news finder application. Its main job is to take a simple text query from a user, figure out what they're looking for, and find the most relevant recent news article.

This guide will show you how to connect to it and use it in the mobile app.

Live API Base URL
The API is deployed on Render and is publicly accessible at the following URL:

https://ovvntempo-server.onrender.com/

How to Use the API
There is one main endpoint you will need to use to get an article.

Find an Article (/search)
This is the core feature of the API. You send it a user's search query, and it returns the details of the best matching article.

Endpoint: /search

Method: POST

Full URL: https://ovvntempo-server.onrender.com/search

Request Body
You must send a JSON object in the body of your POST request. It needs to have one key: user_input.

{
  "user_input": "latest news about electric vehicle batteries"
}

Success Response
If an article is found, the server will respond with a 200 OK status and a JSON object containing the article's details.

query: The refined search query that was used to find the article.

title: The headline of the article.

url: A direct link to the full article.

urlToImage: A link to the article's thumbnail/header image. You can use this to display an image in the app. This might be null if the article has no image.

Example Success Response:

{
  "query": "\"electric vehicle batteries\" latest news",
  "url": "[https://www.some-tech-website.com/article/12345](https://www.some-tech-website.com/article/12345)",
  "urlToImage": "[https://www.some-tech-website.com/images/ev-battery.jpg](https://www.some-tech-website.com/images/ev-battery.jpg)",
  "title": "New Breakthrough Promises to Double EV Battery Life"
}

"Not Found" Response
If no relevant articles are found for the query, the server will respond with a JSON object like this:

{
  "query": "asdfghjkl",
  "url": null,
  "urlToImage": null,
  "message": "No articles found"
}

Testing the API
You can quickly test the API from your command line using a tool like curl. This is a great way to make sure it's working before you write any mobile app code.

curl -X POST "[https://ovvntempo-server.onrender.com/search](https://ovvntempo-server.onrender.com/search)" \
-H "Content-Type: application/json" \
-d '{"user_input": "What are the latest developments on Mars rovers?"}'

Important Note for Developers
The API is hosted on Render's free tier. If it doesn't receive any requests for 15 minutes, it will go to "sleep". The first request after it has been asleep will be slow (it might take 20-30 seconds). If your first request times out, just try it again immediately, and it will be fast. This is normal behavior for the free hosting plan.

Let me know if you have any questions!