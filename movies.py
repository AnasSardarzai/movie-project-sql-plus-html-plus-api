from storage import storage
import sys


def command_list_movies():
    movies = storage.list_movies()
    if not movies:
        print("No movies found.")
        return

    print(f"{len(movies)} movies in total:")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_add_movie():
    title = input("Enter movie title: ")
    storage.add_movie(title)


def command_delete_movie():
    title = input("Enter movie title to delete: ")
    storage.delete_movie(title)


def command_update_movie():
    title = input("Enter the movie title to update: ")
    new_title = input("Enter new title (or leave empty): ") or None
    new_rating = input("Enter new rating (or leave empty): ") or None
    new_year = input("Enter new year (or leave empty): ") or None
    storage.update_movie(title, new_title, new_rating, new_year)


def command_search_movie():
    keyword = input("Enter keyword to search: ")
    results = storage.search_movie(keyword)
    if not results:
        print("No movies found.")
        return
    for title, data in results.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_sort_movies():
    sorted_movies = storage.sort_movies_by_rating()
    for title, data in sorted_movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_stats():
    stats = storage.get_stats()
    print(f"Total movies: {stats['count']}")
    print(f"Average rating: {stats['average']}")
    print(f"Best movie: {stats['best_movie']} ({stats['best_rating']})")
    print(f"Worst movie: {stats['worst_movie']} ({stats['worst_rating']})")


def command_generate_website():
    storage.generate_website()
    print("Website was generated successfully.")


def main():
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
