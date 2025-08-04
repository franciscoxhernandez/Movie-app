from sqlalchemy import create_engine, text
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Define the database URL
DB_URL = "sqlite:///movies.db"


# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT 
        )
    """))
    connection.commit()

def fetch_movie_from_omdb(title):
    """Search and add the movie to the database"""

    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()


        if data["Response"] == "False":
            print(f"\033[91mMovie '{title}' not found on OMDb.\033[0m")
            return None
        try:
            match = re.search(r"\d{4}", data["Year"])
            year = int(match.group()) if match else None
        except (ValueError, TypeError):
            print(f"\033[91mCould not parse year from '{data['Year']}'. Try a different movie.\033[0m")
            return None

            # Extract rating safely (handle N/A)
        try:
            rating = float(data["imdbRating"]) if data["imdbRating"] != "N/A" else 0.0
        except (ValueError, TypeError):
            rating = 0.0

        poster_url = data.get("Poster", "")

        return {
            "title": data["Title"],
            "year": year,
            "rating": rating,
            "poster_url": poster_url
        }

    except requests.RequestException as e:
        print(f"\033[91mConnection error: {e}\033[0m")
        return None

def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]} for row in movies}

def add_movie(title, year, rating, poster_url):
    """Add a new movie to the database using OMDB."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM movies WHERE title = :title"),
                                    {"title": title})
        if result.scalar() > 0:
            print(f"\033[91mMovie '{title}' already exists in the database.\033[0m")
            return
        connection.execute(
            text("INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"),
            {"title": title, "year": year, "rating": rating, "poster_url": poster_url})
        connection.commit()
        print(f"Movie '{title}' added successfully.")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.begin() as connection:
        result = connection.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
        if result.rowcount > 0:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

def update_movie(title, new_year, new_rating):
    """Update a movie's rating in the database."""
    with engine.begin() as conn:
        result = conn.execute(text(
            "UPDATE movies SET year = :year, rating = :rating WHERE title = :title"
        ), {"title": title, "year": new_year, "rating": new_rating})

        if result.rowcount > 0:
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")