import os
import requests
from dotenv import load_dotenv
from storage.storage import list_movies, add_movie_to_db

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")


def fetch_movie_data(title):
    """Fetch movie details from OMDb API."""
    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "False":
            print(f"Movie '{title}' not found.")
            return None
        return {
            "title": data["Title"],
            "year": data["Year"],
            "rating": float(data.get("imdbRating", 0))
        }
    except Exception as e:
        print(f"Error fetching movie: {e}")
        return None


def add_movie(title):
    """Add a movie using OMDb API."""
    movie = fetch_movie_data(title)
    if movie:
        add_movie_to_db(movie["title"], movie["year"], movie["rating"])
        print(f"Added movie: {movie['title']}")


def get_stats():
    """Return stats about all movies (handles duplicates)."""
    movies = list_movies()
    if not movies:
        return {"count": 0, "average": 0, "best_movies": [], "worst_movies": []}

    ratings = [m["rating"] for m in movies.values()]
    avg = round(sum(ratings) / len(ratings), 2)
    max_rating = max(ratings)
    min_rating = min(ratings)

    best_movies = [t for t, m in movies.items() if m["rating"] == max_rating]
    worst_movies = [t for t, m in movies.items() if m["rating"] == min_rating]

    return {
        "count": len(movies),
        "average": avg,
        "best_movies": best_movies,
        "worst_movies": worst_movies
    }


def generate_website():
    """Generate an HTML file with the movie list."""
    try:
        movies = list_movies()
        with open("_static/index_template.html", "r") as f:
            template = f.read()

        movie_html = "\n".join(
            [f"<li>{t} ({d['year']}) - {d['rating']}</li>" for t, d in movies.items()]
        )

        output = template.replace("__TEMPLATE_MOVIE_LIST__", movie_html)

        with open("index.html", "w") as f:
            f.write(output)

        print("Website generated successfully.")
    except Exception as e:
        print(f"Error generating website: {e}")
