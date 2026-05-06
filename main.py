from imdb import Cinemagoer
import pandas as pd
movie_api = Cinemagoer()

class Movie:
  def __init__(self, title, director, year, genre):
    """
    This function is run every time a new movie is created and allows each movie 
    to store its title, director, year, and genre.
    """
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
    """
    This functions sets the title, director, year, and genre to none unless the user updates them
    """
    if title is not None:
      self.title = title
    if director is not None:
      self.director = director
    if year is not None:
      self.year = year
    if genre is not None:
      self.genre = genre

  def __str__(self):
    """
    This function prints the movie in an organized way that allows it to be read nicely
    """
    return f"{self.title} ({self.year}), directed by {self.director} - {self.genre}"

class User:
  def __init__(self):
    """
    This function runs whenever a new user is created, 
    and creates a new empty list of movies that belongs to the user.
    """
    self.movies = []

  def add_movie(self, movie):
    """
    This function allows the user to append a movie to their list
    """
    self.movies.append(movie)

  def view_movies(self):
    """
    This function shows all the movies in the users list
    """
    if not self.movies:
      #If the list of users movies remains empty, the function returns the message letting them know,
      #and it does not let the user edit or remove things that are not there 
      print("You don't have any movies in your list yet.")
      return 1
    else:
      #Lists and numbers the movies that are already in the users list
      for i, movie in enumerate(self.movies):
        print(f"{i}: {movie}")

  def edit_movie(self, index, **kwargs):
    """
    This function allows the user to edit a specific number movie 
    """
    if 0 <= index < len(self.movies):
      # This makes sure that the number given is less than or equal to the number of movies that the user has
      self.movies[index].update(**kwargs)
    else:
      # If the number given does not corrolate to a movie the user get an error message
      print("Index invalid.")

  def remove_movie(self, index):
    """
    This function allows the user to remove a movie from the list
    """
    if 0 <= index < len(self.movies):
      # only lets user choose a number of an existing movie
      self.movies.pop(index)
    else:
      # Gives user an error
      print("Index invalid.")

users = "users.csv"
def load_data():
  if os.path.exists(users) and os.path.getsize(users) > 0:
      return pd.read_csv(users)
  else:
      return pd.DataFrame(columns=["username", "password", "movies"])

def save_user(username, password, user_obj):
    df = load_data()

    movies_data = [movie.to_dict() for movie in user_obj.movies]
    movies_json = json.dumps(movies_data)

    new_row = {
        "username": username,
        "password": password,
        "movies": movies_json
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(users, index=False)

def load_user(username, password):
    df = load_data()

    user_row = df[
        (df["username"] == username) & 
        (df["password"] == password)
    ]

    if user_row.empty:
        print("Invalid username or password.")
        return None

    row = user_row.iloc[0]

    user = User()

    import json
    movies_list = json.loads(row["movies"]) if row["movies"] else []

    for movie_data in movies_list:
        user.add_movie(Movie.from_dict(movie_data))

    return user

def update_user(username, user_obj):
    df = load_data()

    movies_data = [movie.to_dict() for movie in user_obj.movies]
    movies_json = json.dumps(movies_data)

    df.loc[df["username"] == username, "movies"] = movies_json

    df.to_csv(users, index=False)

def sign_in():
  """
  This function allows the user to sign in and select the option they want
  """
  choice = input("Are you a returning user? (y/n): ")
  if choice == "y":
      username = input("What is your username?: ")
      password = input("What is your password?: ")
      loaded_user = load_user(username, password)
      if loaded_user == None:
        print("Try again")
        return sign_in()
  elif choice == "n":
    movie_list = User()
    username = input("What would you like as your username?: ")
    password = input("What would you like as your password?: ")
    save_user(username, password, movie_list)
    loaded_user = load_user(username, password)
  else:
    print("Invalid input.")
    return sign_in()
  while True:
    print("\n1. Add Movie")
    print("2. View List")
    print("3. Edit List")
    print("4. Remove Movie")
    print("5. Go back to homescreen")

    try:
      choice = int(input("Enter your choice (1-5)\n"))
    except ValueError:
      print("Enter a number.")
      continue

    if choice == 1:
      title = input("Title: ")
      director = input("Director: ")
      year = input("Year: ")
      genre = input("Genre: ")
      loaded_user.add_movie(Movie(title, director, year, genre))
      update_user(username, loaded_user)

    elif choice == 2:
      loaded_user.view_movies()

    elif choice == 3:
      if loaded_user.view_movies() != 1:
        while True:
          index = int(input("Number of movie to edit: "))
          if 0 <= index < len(loaded_user.movies):
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
      else:
        continue
    elif choice == 4:
      if loaded_user.view_movies() != 1:
        try:
          index = int(input("Number of movie to remove: "))
        except ValueError:
          print("Enter a number.")
          continue
        loader_user.remove_movie(index)
        update_user(username, loaded_user)
      else:
        continue

    elif choice == 5:
      break

    else:
      print("Choice invalid.")
      
while True:
  print("\n1. Sign in to view or add to your watched movie list") 
  print("2. Get a movie recomendation") 
  print("3. Make a profile") 
  print("4. Quit")

  try:
    choice = int(input("Enter your choice (1-4)\n"))
  except ValueError:
    print("Enter a number.")
    continue
  
  if choice == 1:
    sign_in()

  elif choice == 2:
    get_recommendations()

  elif choice == 3:
    print("placeholder")

  elif choice == 4:
    print("Goodbye!")
    break

  else:
    print("Choice invalid.")







-----------------------------------------------------------------
def get_recommendations():
  criteria = {
  "title": [],
  "director": [],
  "actor": [],
  "genre": [],
  "year": [],
  "studio": [],
  "medium": []
}

  while True:
    print("\nChoose recommendation criteria:")
    print("1. Title")
    print("2. Director")
    print("3. Actor")
    print("4. Genre")
    print("5. Studio")
    print("6. Medium")
    print("7. Year")
    print("8. All criteria")
    print("9. Get recommendations")

    choice = input("Enter choice: ")

    if choice == "1":
      criteria["title"].append(input("Movie title: "))

    elif choice == "2":
      criteria["director"].append(input("Director: "))

    elif choice == "3":
      criteria["actor"].append(input("Actor: "))

    elif choice == "4":
      criteria["genre"].append(input("Genre: "))

    elif choice == "5":
      try:
        criteria["year"].append(int(input("Year: ")))
      except ValueError:
        print("Enter a valid year.")

    elif choice == "6":
      criteria["studio"].append(input("Studio: "))

    elif choice == "7":
      criteria["medium"].append(input("Medium (movie, tv, video, etc): ").lower())

    elif choice == "8":
      criteria["title"].append(input("Movie title: "))
      criteria["director"].append(input("Director: "))
      criteria["actor"].append(input("Actor: "))
      criteria["genre"].append(input("Genre: "))
      try:
        criteria["year"].append(int(input("Year: ")))
      except:
        pass
      criteria["studio"].append(input("Studio: "))
      criteria["medium"].append(input("Medium: ").lower())
      break

    elif choice == "9":
      if any(criteria.values()):
        break
      else:
        print("Enter at least one criterion first.")
    else:
      print("Choice invalid.")

movies = []

for term in search_terms:
  results = movie_api.search_movie(term)

  for result in results[:25]:
    try:
      movie = movie_api.get_movie(result.movieID)
      title = movie.get("title", "Unknown")
      year = movie.get("year", "Unknown")
      genres = movie.get("genres", [])
      directors = movie.get("director", [])
      cast = movie.get("cast", [])
      kind = movie.get("kind", "")
      production = movie.get("production companies", [])

      director_names = [d["name"] for d in directors]
      actor_names = [a["name"] for a in cast[:10]]
      studio_names = [p["name"] for p in production] if production else []

      score = 0

      if criteria["title"] and title.lower() not in [t.lower() for t in criteria["title"]]:
        score += 1

      if criteria["director"] and any(d.lower() in [dn.lower() for dn in director_names] for d in criteria["director"]):
        score += 3

      if criteria["actor"] and any(a.lower() in [an.lower() for an in actor_names] for a in criteria["actor"]):
        score += 3

      if criteria["genre"] and any(g.lower() in [gn.lower() for gn in genres] for g in criteria["genre"]):
        score += 2

      if criteria["year"] and year in criteria["year"]:
        score += 2

      if criteria["studio"] and any(s.lower() in [sn.lower() for sn in studio_names] for s in criteria["studio"]):
        score += 2

      if criteria["medium"] and any(m in kind.lower() for m in criteria["medium"]):
        score += 1

      if score > 0:
        movies.append({
          "Title": title,
          "Year": year,
          "Director": ", ".join(director_names),
          "Genre": ", ".join(genres)
          "Studio": ", ".join(studio_names),
          "Medium": kind
          "Score": score
        })
    except Exception:
      continue
df = pd.DataFrame(movies)

if df.empty:
  print("No recommendations found.")
  return

df = df.drop_duplicates(subset=["Title", "Year"])
#removes duplicate results
df = df.sort_values(by="Score", ascending=False.head(10)
#sorts the results by score, and shows the top 10

print("\nMovie Recommendations:")
#prints recomendations 
for _, row in df.iterrows():
  print(f"{row['Title']} ({row['Year']}) - {row['Director']} - {row['Genre']} - row['Studio']} - row['Medium']}")
