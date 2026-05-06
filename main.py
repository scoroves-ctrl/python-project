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
    self.movies = []

  def add_movie(self, movie):
    self.movies.append(movie)

  def view_movies(self):
    if not self.movies:
      print("You don't have any movies in your list yet.")
      return 1
    else:
      for i, movie in enumerate(self.movies):
        print(f"{i}: {movie}")

  def edit_movie(self, index, **kwargs):
    if 0 <= index < len(self.movies):
      self.movies[index].update(**kwargs)
    else:
      print("Index invalid.")

  def remove_movie(self, index):
    if 0 <= index < len(self.movies):
      self.movies.pop(index)
    else:
      print("Index invalid.")

movie_list = User()

def sign_in():
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
      movie_list.add_movie(Movie(title, director, year, genre))

    elif choice == 2:
      movie_list.view_movies()

    elif choice == 3:
      if movie_list.view_movies() != 1:
        while True:
          index = int(input("Number of movie to edit: "))
          if 0 <= index < len(movie_list.movies):
            break
          else:
            print("Enter a valid movie number.")

        title = input("New title (leave blank if already correct): ")
        director = input("New director (leave blank if already correct): ")
        year = input("New year (leave blank if already correct): ")
        genre = input("New genre (leave blank if already correct): ")

        movie_list.edit_movie(
          index,
          title=title or None,
          director=director or None,
          year=year or None,
          genre=genre or None
        )
      else:
        continue
    elif choice == 4:
      if movie_list.view_movies() != 1:
        try:
          index = int(input("Number of movie to remove: "))
        except ValueError:
          print("Enter a number.")
          continue
        movie_list.remove_movie(index)
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
df = df.sort_values(by="Score", ascending=False.head(10)

print("\nMovie Recommendations:")
for _, row in df.iterrows():
  print(f"{row['Title']} ({row['Year']}) - {row['Director']} - {row['Genre']} - row['Studio']} - row['Medium']}")
