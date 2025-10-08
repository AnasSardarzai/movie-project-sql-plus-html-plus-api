import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import requests

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise ValueError("OMDb API Key not found. Bitte in .env eintragen.")

DB_PATH = "data/movies.db"
DB_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DB_URL, echo=False)  # echo=False schaltet SQL-Logs aus


with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT
        )
    """))
    connection.commit()


def fetch_movie_from_api(title):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("Response") == "False":
            print(f"Movie '{title}' not found in OMDb API.")
            return None
        return {
            "title": data.get("Title"),
            "year": int(data.get("Year", 0)),
            "rating": float(data.get("imdbRating", 0)) if data.get("imdbRating") != "N/A" else 0.0,
            "poster": data.get("Poster")
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie: {e}")
        return None


def add_movie(title):
    movie = fetch_movie_from_api(title)
    if not movie:
        return

    with engine.connect() as connection:
        try:
            connection.execute(text(
                "INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"
            ), movie)
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def list_movies():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}

def delete_movie(title):
    with engine.connect() as connection:
        try:
            result = connection.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
            connection.commit()
            if result.rowcount == 0:
                print(f"No movie found with title '{title}'.")
            else:
                print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")

# ----------------------------
# Website Generator
# ----------------------------
def generate_website():
    movies = list_movies()

    template_path = "static/index_template.html"
    if not os.path.exists(template_path):
        print("Template file not found:", template_path)
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    movie_grid = ""
    for title, data in movies.items():
        movie_grid += f"""
        <div class="movie">
            <img src="{data['poster']}" alt="{title}" />
            <h3>{title} ({data['year']})</h3>
            <p>Rating: {data['rating']}</p>
        </div>
        """

    html_content = template.replace("__TEMPLATE_TITLE__", "My Movie Library")
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
