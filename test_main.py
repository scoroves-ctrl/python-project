# This is a file for PyTest cases
# To run this test, type pytest in the terminal
import pytest

from main import Movie, User

def test_update():
  """This test function is for checking the update method in the Movie Class"""
  movie = Movie("Old Title", "Robert Olson", 1993, "Comedy")

  movie.update(title="New Title", year=2024)

  assert movie.title == "New Title"
  assert movie.year == 2024
  assert movie.director == "Robert Olson"

def test_remove():
  """This function tests is the remove movie method method in the User Class functions properly"""
  user = User()

  movie = Movie("Batman Begins", "Nolan", 2005, "Action")

  user.add_movie(movie)
  user.remove_movie(0)

  assert len(user) == 0
