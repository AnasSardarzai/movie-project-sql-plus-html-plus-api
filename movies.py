import sys
from storage import storage
from utils import fetch_movie_data, add_movie, get_stats, generate_website

def command_list_movies():
    """List all movies in the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies found.")
        return

    print(f"{len(movies)} movies in total:")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_add_movie():
    """Add a movie using OMDb API."""
    title = input("Enter movie title: ").strip()
    if title:
        add_movie(title)
    else:
        print("Title cannot be empty.")


def command_delete_movie():
    """Delete a movie by title."""
    title = input("Enter movie title to delete: ").strip()
    if storage.delete_movie(title):
        print(f"Deleted '{title}'.")
    else:
        print(f"Movie '{title}' not found.")


def command_update_movie():
    """Update an existing movie."""
    title = input("Enter the movie title to update: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    new_title = input("Enter new title (or leave empty): ").strip() or None
    new_rating = input("Enter new rating (or leave empty): ").strip() or None
    new_year = input("Enter new year (or leave empty): ").strip() or None

    if storage.update_movie(title, new_title, new_rating, new_year):
        print("Movie updated successfully.")
    else:
        print("Update failed.")


def command_search_movie():
    """Search movies by keyword."""
    keyword = input("Enter keyword to search: ").strip()
    if not keyword:
        print("Keyword cannot be empty.")
        return

    results = storage.search_movie(keyword)
    if not results:
        print("No movies found.")
        return

    print(f"Found {len(results)} movie(s):")
    for title, data in results.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_sort_movies():
    """Sort movies by rating (highest first)."""
    sorted_movies = storage.sort_movies_by_rating()
    if not sorted_movies:
        print("No movies found.")
        return

    print("Movies sorted by rating:")
    for title, data in sorted_movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_stats():
    """Show statistics about movies."""
    stats = get_stats()
    print(f"Total movies: {stats['count']}")
    print(f"Average rating: {stats['average']}")

    if stats['best_movies']:
        print(f"Best movie(s): {', '.join(stats['best_movies'])}")
    if stats['worst_movies']:
        print(f"Worst movie(s): {', '.join(stats['worst_movies'])}")


def command_generate_website():
    """Generate HTML website from movies."""
    generate_website()


def main():
    """Main menu loop."""
    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie (from OMDb API)")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Search movie")
        print("6. Sort movies by rating")
        print("7. Stats")
        print("9. Generate website")

        choice = input("Choose an option: ").strip()
        if choice == "0":
            sys.exit()
        elif choice == "1":
            command_list_movies()
        elif choice == "2":
            command_add_movie()
        elif choice == "3":
            command_delete_movie()
        elif choice == "4":
            command_update_movie()
        elif choice == "5":
            command_search_movie()
        elif choice == "6":
            command_sort_movies()
        elif choice == "7":
            command_stats()
        elif choice == "9":
            command_generate_website()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
