class Movie:
  def __init__(self, title, director, year, genre):
    self.title = title
    self.director = director
    self.year = year
    self.genre = genre

  def update(self, title=None, director=None, year=None, genre=None):
    if title is not None:
      self.title = title
    if director is not None:
      self.director = director
    if year is not None:
      self.year = year
    if genre is not None:
      self.genre = genre

  def __str__(self):
    return f"{self.title} ({self.year}), directed by {self.director} - {self.genre}"

class User:
  def __init__(self):
    self.movies = []

  def add_movie(self, movie):
    self.movies.append(movie)

  def view_movies(self):
    if not self.movies:
      print("You don't have any movies in your list yet.")
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
      movie_list.view_movies()
      try:
        index = int(input("Number of movie to edit: "))
      except ValueError:
        print("Enter a number.")
        continue

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
    elif choice == 4:
      movie_list.view_movies()
      try:
        index = int(input("Number of movie to remove: "))
      except ValueError:
        print("Enter a number.")
        continue
      movie_list.remove_movie(index)

    elif choice == 5:
      break

    else:
      print("Choice invalid.")

while True:
  print("1. Sign in to view or add to your watched movie list") 
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
    print("placeholder")

  elif choice == 3:
    print("placeholder")

  elif choice == 4:
    print("Goodbye!")
    break

  else:
    print("Choice invalid.")

