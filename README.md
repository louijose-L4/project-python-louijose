# project-python-louijose
This is a captsone project for Advanced Python course.

The python script scraps top 50 US english movies based on genres by selenium from the website www.imdb.com.

It instantiates a class 'MovieExtract' and opens the url www.imdb.com through webchrome browser in the constructor method.

'data_extract' method loops through imdb url based on genres and scraps data like title, year, ratings, certification, director and actors.It saves the data in a list and further writes it in a csv file.

'movie_picker' method accepts an argument 'gender list' which is returned from the data_extract method. It reads the saved csv file created in the data_extract , using pandas library. It filter the dataframe based genre provided by user input. It uses random library to choose a list of film titles and prints out film details.
Libaries used: selenium, csv, pandas,os
