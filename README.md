# Movie App 🎬

A terminal-based app to manage your favorite movies, fetch real data from OMDb, and generate a personal movie website.

## Features

- Add movies with title, year, rating, poster
- Fetch data from OMDb API
- Store movies in SQLite
- Generate a movie website (HTML + CSS)
- View stats, search, update, and delete

## Setup

1. Clone the repo  
2. Create `.env` with your OMDb API key:
   ```bash
   OMDB_API_KEY=your_key_here
For OMDB_API_KEY go to the Go to OMDb API website.https://www.omdbapi.com/ 
Scroll down to the “Examples” section and try the API. Input different titles, parts of titles and see what happens. You’re going to use this API from your Python code.
Obtaining API Key
Many services require using a user identifier to access the API - this identifier is called an API key. When you access the API, you should provide the API key along with your request.
This method allows the service to track the usage of the API from different users, and possibly to apply rate limiting, for example, to make sure you don’t overuse the API.
To get an API key for OMDb, click on the “API Key” at the navigation menu. Enter your email, and choose "Free account". Go to your inbox, you should find there an email from the website with your API key. If you don’t see the email, check your Spam. Click on the activation key to activate your API key. Now you can use it in all future requests!

Use It With Python
Read the specification of the API in OMDb API home page. Use the t param to search a single by title, by making a request to:
http://www.omdbapi.com/?apikey=[yourkey]&t=titanic
You can try it in your browser, and via Python code. Verify that you can access the API and get results.


