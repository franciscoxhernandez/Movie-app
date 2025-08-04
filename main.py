import statistics
import random
import matplotlib.pyplot as plt
from rapidfuzz import fuzz
import os
from storage import movie_storage_sql as storage
from storage.movie_storage_sql import add_movie, list_movies
from storage.movie_storage_sql import fetch_movie_from_omdb


def menu():
    """Main menu function"""
    print()
    print("\033[94m********** My Movies Database **********\033[0m") # blue
    print()
    print("\tMenu ")
    print()
    print("0. \tExit\n"
          "1. \tList Movies\n"
          "2. \tAdd Movie\n"
          "3. \tDelete Movie\n"
          "4. \tUpdate Movie\n"
          "5. \tStats\n"
          "6. \tRandom Movie\n"
          "7. \tSearch Movie\n"
          "8. \tMovies Sorted by Rating\n"
          "9. \tCreate Rating Histogram\n"
          "10.\tMovies Sorted by Year\n"
          "11.\tGenerate website")
    print()

def list_movies():
    """Prints the list of movies in the database"""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total\n")

    for title, details in movies.items():
        print(f"{title}: ({details['year']}) - Rating: {details['rating']}")
        poster = details.get("poster_url")
        if poster and poster != "N/A":
            print(f"Poster URL: {poster}")
        else:
            print("Poster not available.")
        print()

def add_movie_ui():
    """Add a movie to the database"""
    user_title = input("\033[96mEnter movie title to add: \033[0m").strip()
    if not user_title:
        print("\033[91mMovie title cannot be empty.\033[0m")
        return

    movie_data = fetch_movie_from_omdb(user_title)
    if movie_data:
        add_movie(
            title=movie_data["title"],
            year=movie_data["year"],
            rating=movie_data["rating"],
            poster_url=movie_data["poster_url"]
        )
    else:
        print("\033[91mCould not fetch movie data.\033[0m")

def delete_movie():
    """Delete a movie from the database"""
    user_delete_movie = (input("Enter movie name to delete: "))
    if not user_delete_movie:
        print("\033[91mMovie name cannot be empty\033[0m")
        return
    movies = storage.list_movies()
    if user_delete_movie in movies:
        storage.delete_movie(user_delete_movie)
        print(f"Movie {user_delete_movie} successfully deleted")
    else:
        print("Movie doesn't exist")

def update_movie():
    """ Update Movie Rating Histogram """
    user_update_movie = (input("Enter movie name to be updated: "))
    if not user_update_movie:
        print("\033[91mMovie name cannot be empty\033[0m")
        return
    movies = storage.list_movies()
    if user_update_movie in movies:
        current_year = movies[user_update_movie]["Year"]
        print(f"The current year of {user_update_movie} is {current_year}")

        while True:
            try:
                question_new_rating = float(input("Enter new movie rating: "))
                break
            except ValueError:
                print("\033[91mInvalid input, please enter a number for the rating\033[0m")
        while True:
            try:
                question_new_year = int(input(f"Enter new movie year: "))
                break
            except ValueError:
                print("\033[91mInvalid input, please enter a valid year\033[0m")
        movies[user_update_movie]['rating'] = question_new_rating
        movies[user_update_movie]['year'] = question_new_year
        storage.save_movies(movies)
        print(f"Movie {user_update_movie} successfully updated")
    else:
        print(f"Movie {user_update_movie} doesn't exist")

def stats():
    """Prints statistics about the database"""
    ratings = []
    movies = storage.list_movies()
    for details in movies.values():
        ratings.append(details["rating"])
    average_rating = sum(ratings) / len(ratings)
    print(f"Average rating is: {average_rating:.2f}")
    median_rating = statistics.median(ratings)
    print(f"Median rating is : {median_rating:.2f}")
    max_rating = max(ratings)
    for title, details in movies.items():
        if details["rating"] == max_rating:
            print(f"The best movie is {title} with a rating of {max_rating}")
    min_rating = min(ratings)
    for title, details in movies.items():
        if details["rating"] == min_rating:
            print(f"The worst movie is {title} with a rating of {min_rating}")

def random_movie():
    """Prints a random movie from the database"""
    movies = storage.list_movies()
    movie_list = list(movies.items())
    title, details = random.choice(movie_list)
    print(f"Your movie for tonight is: {title} ({details['year']}) with a rating of {details['rating']}")

def search_movie():
    """Prints a search movie from the database"""
    user_search = input("Enter part of the movie name: ").strip().lower()
    if not user_search:
        print("\033[91mSearch cannot be empty\033[0m")
        return

    movies = storage.list_movies()
    matches = []
    for title in movies:
        if title.lower().startswith(user_search):
            matches.append(title)
    if matches:
        print(f"\nMovies starting with {user_search}")
        for title in matches:
            details = movies[title]
            print(f"{title}: ({details['year']}): "
                  f"Rating {details['rating']}")
        return

    for title in movies:
        if user_search == title.lower():
            details = movies[title]
            print(f"Exact match found: {title}: ({details['year']}): "
                  f"Rating {details['rating']}")
            return
    best_match = ""
    best_score = 0
    for title, _ in movies.items():
        score = fuzz.partial_ratio(user_search.lower(), title.lower())
        if score > best_score:
            best_score = score
            best_match = title

    if best_score >= 70:
        details = movies[best_match]
        print(f"No exact match found. \nDid you mean: {best_match}?")
        print(f"{best_match}: ({details['year']}): Rating {details['rating']} "
              f"(match score: {best_score:.2f})")
    else:
        print("\033[91mMovie with that title not found\033[0m")

def sorted_movies():
    """Prints a sorted list of movies in the database"""
    movies = storage.list_movies()
    list_of_movies = list(movies.items())
    def get_rating(movie_pairs):
        details = movie_pairs[1]
        return details['rating']

    list_of_movies.sort(key=get_rating, reverse = True)

    for title, details in list_of_movies:
        print(f"{title}: ({details['year']}): Rating {details['rating']}")

def create_histogram():
    """Creates a histogram of movies based on the ranking"""
    movies = storage.list_movies()
    titles = list(movies.keys())
    ratings = []
    for details in movies.values():
        ratings.append(details['rating'])

    plt.figure(figsize=(12,6))
    plt.bar(titles,ratings, color="lightblue")
    plt.title("Movie Ratings")
    plt.xlabel("Movie Title")
    plt.ylabel("Rating")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.ylim(0,10)

    filename = input("Enter a file name to save the Chart, for example, chart.png: ")

    if filename.strip() != "" and filename.strip().endswith(".png"):
        try:
            plt.savefig(filename.strip())
            print(f"Chart saved as {filename.strip()}")
        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")
    else:
        print("\033[91mInvalid file name. Please include .png at the end\033[0m")

    plt.show()

def sort_by_year():
    """Prints a sorted list of movies in the database"""
    movies = storage.list_movies()

    print("How would you like to sort the movies?")
    print("1. Newest First")
    print("2. Oldest First")

    user_choice = input("Enter 1 or 2: ").strip()
    if user_choice == "1":
        reverse_order = True
    elif user_choice == "2":
        reverse_order = False
    else:
        print("\033[91mInvalid choice. Please enter 1 or 2.\033[0m")
        return

    list_of_movies = list(movies.items())

    def get_year(movie_pairs):
        return movie_pairs[1]['year']

    list_of_movies.sort(key=get_year, reverse=reverse_order)

    for title, details in list_of_movies:
        print(f"{title}: ({details['year']}): Rating {details['rating']}")

def generate_website():
    """Generates a website based on the user input"""
    movies = storage.list_movies()

    with open("static/index_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    template_title = "My favorite movies collection"
    template = template.replace("__TEMPLATE_TITLE__", template_title)

    movie_grid_html =""
    for title, details in movies.items():
        poster_url = details.get('poster_url')
        if not poster_url or poster_url == "N/A":
            poster_url = "https://dummyimage.com/128x193/cccccc/000000.png&text=No+Image"
        year = details.get('year', 'N/A')
        movie_html = f"""
        <li>
            <div class="movie">
                <div class="movie-poster">
                    <img src="{poster_url}" alt="{title} poster" class="movie-poster">
                </div>
                <div class="movie-title">
                    <a href="https://www.imdb.com/find?q={title.replace(' ', '+')}" target="_blank" rel="noopener noreferrer">
                        {title}
                    </a>
                </div>
                <div class="movie-year">{year}</div>
                <div class="movie-rating"> Rating IMDB: {details.get('rating', 'N/A')}</div>
            </div>
        </li>
        """
        movie_grid_html += movie_html.strip() + "\n"

    template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html.strip())

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(template)
    print("\033[92mWebsite was generated successfully!!\033[0m")

def main():
    """Main function"""
    while True:
        menu()
        try:
            user_menu_choice = input("Enter choice between 1 and 10, select 0 to quit: ").strip()
            if not user_menu_choice:
                print("\033[91mInvalid choice. Please enter a number\033[0m")
                continue
            user_menu_choice = int(user_menu_choice)
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")
            continue
        if user_menu_choice == 0:
            print("Bye!")
            break
        if user_menu_choice == 1:
            list_movies()
        elif user_menu_choice == 2:
             add_movie_ui()
        elif user_menu_choice == 3:
            delete_movie()
        elif user_menu_choice == 4:
             update_movie()
        elif user_menu_choice == 5:
             stats()
        elif user_menu_choice == 6:
             random_movie()
        elif user_menu_choice == 7:
             search_movie()
        elif user_menu_choice == 8:
             sorted_movies()
        elif user_menu_choice == 9:
            create_histogram()
        elif user_menu_choice == 10:
            sort_by_year()
        elif user_menu_choice == 11:
            generate_website()
        else:
            print ("\033[91mInput invalid please try again\033[0m")
        input("\033[92mPlease Enter to continue: \033[0m")

if __name__ == "__main__":
  main()
