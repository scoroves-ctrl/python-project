READMD 

Project Title: RGS Movie Recommendation 



COMMENT LAMDA FUNCTION

Team member names, emails, and Stevens IDs:
Robert Olson, rolson2@stevens.edu, 20013766
Gianna Felice, gfelice@stevens.edu, 20006129
Stella Corovessis, scoroves@stevens.edu, 20006071


Project description: 
	Project Overview:
	The project has two classes that are used called user and movies. These classes are used to run functions every time a movie or a user is created. The functions that are run are load data, save user, load user, update user, sign in, and get recommendations. The sign in function allows the user to save a list of their favorite movies, and the get recommendations function allows the user to search for movies. If recommendations are wanted the user can choose to enter they way they want their recommendation and then they are prompted to enter their key word. These are the two main functions that address the project. Exceptions found in the project are in the user class and the view movies function. It allows the user to view their movies if the created list of movies is not empty. There is another exception found in the function get recommendation, which allows for the code to not break if a problem comes up. The code uses csv files to store and read the user data. There are several loop statements two of which are used to allow the user to use a menu. One in the sign in function, and one in the get recommendation function. The two mutable types are a list for the movies, and a dictionary used to have the movies with their categories. The immutable lists are the menus that use the integers to make the choices. The __str__() function in this code is used to organize the movie data in an organized way in the movie class. The code contains a lambda function in the user class and the view movies function, which organizes the users movie list class with its numbers. The code also is able to use list comprehension to track movies for the user and the movie recommendations. The built in library that was used is called OS. Recursion is also used several times to keep the code from breaking and return the user back to the original function.  
	
	
	Libraries: 
		- tmdbv3api
		- Pandas 
		- JSON

 

How to run the Program: 

The user is initially directed to a sign in screen where they must say if they want to get a movie recommendation or sign in. If they are a new user or returning user They will have the option to sign in or make an account. If they are new, they are directed to make a new account with a user name and password, and if they are returning, they will be asked to sign into their account. Once the user is signed into the account, they will have the option to add a movie to their list, view their list, edit their list, remove movie from list, or go back to home screen. If the user wishes to get a movie recommendation, they are directed to choose the category they wish to get recommendations on then they are directed to enter the key word. 

Team Member contributions: 
  Gianna Felice -> Planning, Requirement Checks, Debugging, Comment and Docstrings, and README file
	Robert Olson -> Planning, Classes, Requirement checks, debugging 
	Stella Corovessis -> Planning, Library Research, Initial Menu and functions connected, Debugging 
	Gianna Felice -> Planning, Requirement Checks, Debugging, Comment and Docstrings, and README file
	Robert Olson -> Planning, Classes, Requirement checks, debugging 
	Stella Corovessis -> Planning, Library Research, Initial Menu and functions connected, Debugging 
