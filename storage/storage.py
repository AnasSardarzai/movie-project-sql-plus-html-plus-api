import os
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# .env laden
load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
if not API_KEY:
    print("⚠️  OMDB_API_KEY not found in .env file!")

# SQLite-Datei im aktuellen Verzeichnis
DB_PATH = os.path.join(os.path.dirname(__file__), "movies.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Tabelle erstellen
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            title TEXT PRIMARY KEY,
            year TEXT,
            rating REAL
        )
    """))
    conn.commit()


# ---- Funktionen ---- #

def fetch_movie_data(title):
    """Hole Filmdaten von der OMDb API"""
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
        print(f"Error fetching movie from OMDb: {e}")
        return None


def add_movie(title):
    """Fügt einen Film hinzu (holt Daten von OMDb)"""
    movie_data = fetch_movie_data(title)
    if not movie_data:
        return

    with engine.connect() as conn:
        try:
            conn.execute(
                text("INSERT INTO movies (title, year, rating) VALUES (:t, :y, :r)"),
                {"t": movie_data["title"], "y": movie_data["year"], "r": movie_data["rating"]}
            )
            conn.commit()
            print(f"Added movie: {movie_data['title']}")
        except Exception:
            print(f"Movie '{title}' already exists.")


def delete_movie(title):
    with engine.connect() as conn:
        result = conn.execute(text("DELETE FROM movies WHERE title = :t"), {"t": title})
        conn.commit()
        if result.rowcount:
            print(f"Deleted '{title}'.")
        else:
            print(f"Movie '{title}' not found.")


def update_movie(title, new_title=None, new_rating=None, new_year=None):
    with engine.connect() as conn:
        existing = conn.execute(text("SELECT * FROM movies WHERE title=:t"), {"t": title}).fetchone()
        if not existing:
            print("Movie not found.")
            return

        new_title = new_title or existing[0]
        new_year = new_year or existing[1]
        new_rating = new_rating or existing[2]

        conn.execute(
            text("UPDATE movies SET title=:nt, year=:ny, rating=:nr WHERE title=:t"),
            {"nt": new_title, "ny": new_year, "nr": new_rating, "t": title}
        )
        conn.commit()
        print("Movie updated successfully.")


def list_movies():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM movies")).fetchall()
        return {r[0]: {"year": r[1], "rating": r[2]} for r in rows}


def search_movie(keyword):
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM movies WHERE title LIKE :kw"), {"kw": f"%{keyword}%"}).fetchall()
        return {r[0]: {"year": r[1], "rating": r[2]} for r in rows}


def sort_movies_by_rating():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM movies ORDER BY rating DESC")).fetchall()
        return {r[0]: {"year": r[1], "rating": r[2]} for r in rows}


def get_stats():
    movies = list_movies()
    if not movies:
        return {"count": 0, "average": 0, "best_movie": None, "best_rating": 0, "worst_movie": None, "worst_rating": 0}

    ratings = [data["rating"] for data in movies.values()]
    best = max(movies.items(), key=lambda x: x[1]["rating"])
    worst = min(movies.items(), key=lambda x: x[1]["rating"])

    return {
        "count": len(movies),
        "average": round(sum(ratings) / len(ratings), 2),
        "best_movie": best[0],
        "best_rating": best[1]["rating"],
        "worst_movie": worst[0],
        "worst_rating": worst[1]["rating"],
    }


def generate_website():
    """Erzeugt eine HTML-Datei aus den gespeicherten Filmen."""
    movies = list_movies()
    with open("_static/index_template.html", "r") as f:
        template = f.read()

    movie_list_html = ""
    for title, data in movies.items():
        movie_list_html += f"<li>{title} ({data['year']}) - Rating: {data['rating']}</li>\n"

    output_html = template.replace("__TEMPLATE_MOVIE_LIST__", movie_list_html)

    with open("index.html", "w") as f:
        f.write(output_html)
