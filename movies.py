from storage import movie_storage_sql as storage

def command_list_movies():
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")

def command_add_movie():
    title = input("Enter movie title: ")
    storage.add_movie(title)

def command_delete_movie():
    title = input("Enter movie title to delete: ")
    storage.delete_movie(title)

def command_generate_website():
    storage.generate_website()
    print("Website was generated successfully.")

def main():
    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("9. Generate website")

        choice = input("Choose an option: ")
        if choice == "0":
            break
        elif choice == "1":
            command_list_movies()
        elif choice == "2":
            command_add_movie()
        elif choice == "3":
            command_delete_movie()
        elif choice == "9":
            command_generate_website()
        else:
            print("Invalid choice")
