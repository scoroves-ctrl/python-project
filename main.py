from tmdbv3api import TMDb, Movie, Person
# TMDb, Movie, Discover, and Person classes are added. This is for searching movie recommendations
import pandas as pd
# Pandas is added for DataFrames, which are very helpful for stored and gathering data
import json
# json is a built in module used for converting dictionaries to JSON strings which can be readily stored in users.csv
tmdb = TMDb()
# an object created with TMDb class from tmdbv3api
tmdb.api_key = "7264a55d7bdda57808b10751e37b54ab"
# key used to access tmdbv3api functionality
tmdb.language = "en"
# language set to English

movie_api = Movie()
# an object created with the Movie class from tmdbv3api before Movie class is overwritten
person_api = Person()
# an object created with Person class from tmdbv3api

class Movie:
  def __init__(self, title, director, year, genre):
    """This function is run every time a new movie is created and allows each movie to store its title, director, year, and genre."""
    self.title = title
    self.director = director
    self.year = year
    self.genre = genre

  def to_dict(self):
    """This function can convert the movie class into a dictionary, which is easier to store in a csv"""
    return {
      "title": self.title,
      "director": self.director,
      "year": self.year,
      "genre": self.genre
    }

  @staticmethod
  # staticmethod decorator is used here so the method is bound to the class itself, rather than instances
  def from_dict(data):
    """This function can convert the dictionary form of a movie class back into a movie object"""
    return Movie(
      data["title"],
      data["director"],
      data["year"],
      data["genre"]
    )

  def update(self, title=None, director=None, year=None, genre=None):
    """This functions sets the title, director, year, and genre to none unless the user updates them"""
    if title is not None:
      self.title = title
    if director is not None:
      self.director = director
    if year is not None:
      self.year = year
    if genre is not None:
      self.genre = genre

  def __str__(self):
    """This function prints the movie in an organized way that allows it to be read nicely"""
    return f"{self.title} ({self.year}), directed by {self.director} - {self.genre}"

class User:
  def __init__(self):
    """This function runs whenever a new user is created, and creates a new empty list of movies that belongs to the user."""
    self.movies = []
    
  def __len__(self):
    """Operator overload for length of movie list"""
    return len(self.movies)

  def add_movie(self, movie):
    """This function allows the user to append a movie to their list"""
    self.movies.append(movie)

  def view_movies(self):
    """This function shows all the movies in the users list"""
    if not self.movies:
      #If the list of users movies remains empty, the function returns the message letting them know, and it does not let the user edit or remove things that are not there 
      print("You don't have any movies in your list yet.")
      return 1
    else:
      #Lists and numbers the movies that are already in the users list
      format_movie = lambda i, movie: f"{i}: {movie}"
      #lambda function organizes the movie message with its number 
      for i, movie in enumerate(self.movies):
        print(format_movie(i, movie))

  def edit_movie(self, index, **kwargs):
    """This function allows the user to edit a specific number movie"""
    if 0 <= index < len(self):
      # This makes sure that the number given is less than or equal to the number of movies that the user has
      self.movies[index].update(**kwargs)
    else:
      # If the number given does not corrolate to a movie the user get an error message
      print("Index invalid.")

  def remove_movie(self, index):
    """This function allows the user to remove a movie from the list"""
    if 0 <= index < len(self):
      # only lets user choose a number of an existing movie
      self.movies.pop(index)
    else:
      # Gives user an error if given index is invalid
      print("Index invalid.")

users = "users.csv"
def load_data():
  """This function allows the code to check that the users.csv exists and will load the csv"""
  try:
    return pd.read_csv(users)
  except FileNotFoundError:
    # if the file isn't found, it will simply create the file
    print("users.csv not found. Creating new file.")
    df = pd.DataFrame(columns=["username", "password", "movies"])
    df.to_csv(users, index=False)
    return df

def save_user(username, password, user_obj):
  """This function is used to save the user in a csv file and converts the movies into dictionaries"""
  df = load_data()
  # users.csv is load
  movies_data = [movie.to_dict() for movie in user_obj.movies]
  # creates a dictionary called movies_data from the movies list in a user object
  movies_json = json.dumps(movies_data)
  # converts said dictionary into a json file, json file will be blank for new users
  
  new_row = {
    "username": username,
    "password": password,
    "movies": movies_json
  }
  
  df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
  # adds the data to the dataframe
  df.to_csv(users, index=False)
  # uploads dataframe to users.csv file

def load_user(username, password):
  """This function loads an existing user from the csv file"""
  df = load_data()

  # normalize the stored data
  df["username"] = df["username"].astype(str).str.strip()
  df["password"] = df["password"].astype(str).str.strip()

  # normalizes the input
  username = username.strip()
  password = password.strip()

  # finds the user by username first
  user_row = df[df["username"] == username]

  if user_row.empty:
      print("User not found.")
      # if username isn't found then an error is printed
      return None

  row = user_row.iloc[0]
  # this is done to access password information in the next cell over

  # then check passowrd
  if row["password"] != password:
      print("Incorrect password.")
      return None

  user = User()
  #this defines user as an object of user class 

  movies_list = json.loads(row["movies"]) if pd.notna(row["movies"]) else []
  # turns the text into a list

  for movie_data in movies_list:
      user.add_movie(Movie.from_dict(movie_data))
      # adds the movie to the user object 

  return user

def update_user(username, user_obj):
  """This function is used to update the user after the user has changed their movie list """
  df = load_data()

  movies_data = [movie.to_dict() for movie in user_obj.movies]
  movies_json = json.dumps(movies_data)
  # same logic as save_user function

  df.loc[df["username"] == username, "movies"] = movies_json
  # finds the user name in the file and adds the correct movie to the correct user

  df.to_csv(users, index=False)
  # uploads dataframe to the users.csv

def sign_in():
  """This function allows the user to sign in and select the option they want"""
  choice = input("Are you a returning user? (y/n): ")
  if choice == "y":
    # for a returning user, they are asked to enter their username and password
    username = input("What is your username?: ")
    password = input("What is your password?: ")
    loaded_user = load_user(username, password)
    # user is loaded for csv as loaded_user
    if loaded_user == None:
      # if the username or password are incorrect, the function sign_in is recursively called so the user can try again
      print("Try again")
      return sign_in()
  elif choice == "n":
    # for a new user, they are asked to create a username and password
    movie_list = User()
    username = input("What would you like as your username?: ")
    password = input("What would you like as your password?: ")
    save_user(username, password, movie_list)
    loaded_user = load_user(username, password)
    # the username, password, and a blank json file are added to the csv
    # then, the data is loaded as loaded_user
  else:
    print("Invalid input.")
    return sign_in()
    # function recursively called if there is an error
  while True:
    print("\n1. Add Movie")
    print("2. View List")
    print("3. Edit List")
    print("4. Remove Movie")
    print("5. Go back to homescreen")
    # options for editing a user object

    try:
      # for if they enter an invalid input
      choice = int(input("Enter your choice (1-5)\n"))
    except ValueError:
      print("Enter a number.")
      continue

    if choice == 1:
      # adds movie to user list 
      title = input("Title: ")
      director = input("Director: ")
      year = input("Year: ")
      genre = input("Genre: ")
      loaded_user.add_movie(Movie(title, director, year, genre))
      update_user(username, loaded_user)
      # the update user function used to update the csv

    elif choice == 2:
      # view users movie list 
      loaded_user.view_movies()

    elif choice == 3:
      # edit list 
      if loaded_user.view_movies() != 1:
        # checks if a 1 is returned. if a 1 is returned, then the list is blank
        while True:
          index = int(input("Number of movie to edit: "))
          if 0 <= index < len(loaded_user):
            #this if statement ensures a valid movie index is entered
            break
          else:
            print("Enter a valid movie number.")

        title = input("New title (leave blank if already correct): ")
        director = input("New director (leave blank if already correct): ")
        year = input("New year (leave blank if already correct): ")
        genre = input("New genre (leave blank if already correct): ")

        loaded_user.edit_movie(
          index,
          title=title or None,
          director=director or None,
          year=year or None,
          genre=genre or None
        )
        update_user(username, loaded_user)
        # the update user function used to update the csv
      else:
        continue
    elif choice == 4:
      # removes movie from user list
      if loaded_user.view_movies() != 1:
        #checks if a 1 is returned. if a 1 is returned, then the list is blank
        try:
          # Exception handling for if an nondigit is entered
          index = int(input("Number of movie to remove: "))
        except ValueError:
          print("Enter a number.")
          continue
        loaded_user.remove_movie(index)
        update_user(username, loaded_user)
        # the update user function used to update the csv
      else:
        continue

    elif choice == 5:
      #signs out and returns to home screen
      print("Return to home screen")
      break

    else:
      #tells the user that they entred an invalid input 
      print("Choice invalid.")

def get_recommendations():
  """This function gives the user a list of movie recommendations based on a keyword search using the tmdbv3api"""
  search_type = input("Search by 1. title, 2. actor, or 3. director? (type the number): ").lower()
  # This prompt asks the user which keyword type they would like to search by
  query = input("Enter search term: ")
  # This prompt asks the user which the keyword they would like to search
  movies = []
  # A blank list of movies is made, movies that match the inputted keyword will be added to this list
  try:
    if search_type == "1":
    # for title searchs
      results = movie_api.search(query)
      # uses built in search method from the tmdbv3api Movie class, returns a json
      for movie in list(results)[:10]:
        # converts json to list and limits to the first 10 results. list comprehension is used for each movie in the list
        details = movie_api.details(movie.id)
        # fetches movie details using the built in details method
        title = getattr(details, "title", "Unknown")
        # uses getattr to fetch the title from the details, Unknown is set as the default value
        release_date = getattr(details, "release_date", "")
        # uses getattr to fetch the release date from details, default value is set blank
        year = release_date[:4] if release_date else "Unknown"
        # limits the release date to the first 4 characters using string splicing, which happens to be the year. if release date isnt found default value is unknown
        movies.append({
        # adds the 10 movies to the blank movie list
          "Title": title,
          "Year": year
        })
    elif search_type in ["2", "3"]:
      # for if 2 or 3 are entered
      people = person_api.search(query)
      # uses built in search method of the tmdbv3api People class, returns a json
      if not people:
      # for if the person cannot be found
        print("No person found.")
        return
      person = people[0]
      # the person is set as the first and most likely match in the list of people
      credits = person_api.movie_credits(person.id)
      # retrieves a list of all movies a specific person has participated in
      if search_type == "2":
        movie_list = credits.cast
        # searches cast for actors
      else:
        movie_list = credits.crew
        # searches crew for directors
      added = set()
      # creates a set object
      for movie in list(movie_list)[:10]:
        # converts json to list and limits to the first 10 results. list comprehension is used for each movie in the list
        details = movie_api.details(movie.id)
        # fetches movie details using the built in details method
        title = getattr(details, "title", "Unknown")
        # uses getattr to fetch the title from the details, Unknown is set as the default value
        release_date = getattr(details, "release_date", "")
        # uses getattr to fetch the release date from details, default value is set blank
        year = release_date[:4] if release_date else "Unknown"
        # limits the release date to the first 4 characters using string splicing, which happens to be the year. if release date isnt found default value is unknown
        movies.append({
        # adds the 10 movies to the blank movie list
          "Title": title,
          "Year": year
        })
    else:
      # if the user enters something other than 1 2 or 3
      print("Invalid search type.")
      return

  except Exception as e:
    #general exception added for any errors that may occur
    print("Error:", e)
    return

  if not movies:
    # for if no recommended movies can be found
    print("No recommendations found.")
    return

  print("\nMovie Recommendations:")

  for movie in movies:
    # prints the list of movie recommendations
    print(f"{movie['Title']} ({movie['Year']})")

if __name__ == "__main__":
# this is added so that importing this file will not start the main.py program
  while True:
  # this while loop can be thought of as the homescreen of the program
    print("\n1. Sign in to view or add to your watched movie list") 
    print("2. Get a movie recomendation")
    print("3. Quit")
  
    try:
      choice = int(input("Enter your choice (1-3)\n"))
    # exception handling added with try/except
    except ValueError:
      print("Enter a number.")
      continue
      
    if choice == 1:
      sign_in()
  
    elif choice == 2:
      get_recommendations()
  
    elif choice == 3:
      # quits the program with break
      print("Goodbye!")
      break
  
    else:
      # added for invalid choices
      print("Choice invalid.")
