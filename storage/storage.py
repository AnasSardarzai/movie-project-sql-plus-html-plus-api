import os
from sqlalchemy import create_engine, text

DB_PATH = os.path.join(os.path.dirname(__file__), "movies.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Create table
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            title TEXT PRIMARY KEY,
            year TEXT,
            rating REAL
        )
    """))
    conn.commit()


def list_movies():
    """Return all movies from the database."""
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT * FROM movies")).fetchall()
            return {r[0]: {"year": r[1], "rating": r[2]} for r in rows}
    except Exception as e:
        print(f"Error listing movies: {e}")
        return {}


def add_movie_to_db(title, year, rating):
    """Insert a new movie into the database."""
    try:
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO movies (title, year, rating) VALUES (:t, :y, :r)"),
                {"t": title, "y": year, "r": rating}
            )
            conn.commit()
    except Exception as e:
        print(f"Error adding movie '{title}': {e}")


def delete_movie(title):
    """Delete a movie by title."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM movies WHERE title = :t"), {"t": title})
            conn.commit()
            return result.rowcount > 0
    except Exception as e:
        print(f"Error deleting movie: {e}")
        return False


def update_movie(title, new_title=None, new_rating=None, new_year=None):
    """Update an existing movie."""
    try:
        with engine.connect() as conn:
            existing = conn.execute(text("SELECT * FROM movies WHERE title=:t"), {"t": title}).fetchone()
            if not existing:
                return False

            new_title = new_title or existing[0]
            new_year = new_year or existing[1]
            new_rating = new_rating or existing[2]

            conn.execute(
                text("UPDATE movies SET title=:nt, year=:ny, rating=:nr WHERE title=:t"),
                {"nt": new_title, "ny": new_year, "nr": new_rating, "t": title}
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Error updating movie: {e}")
        return False
