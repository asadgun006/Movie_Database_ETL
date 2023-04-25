# Web-Scraping-and-Pipelining

This is a web scraping project that scrapes Wikipedia pages for Disney and movie information. 

For Disney information, the following link is used to extract the links for Disney movies, which are then used for extracting the relevant data:

https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films

For Marvel information, two Wikipedia webpages are used to extract MCU movie and tv show links, which are then used to extract relevant data:

https://en.wikipedia.org/wiki/List_of_Marvel_Cinematic_Universe_films
https://en.wikipedia.org/wiki/List_of_Marvel_Cinematic_Universe_television_series

The data is extracted, transformed, and loaded directly into a MongoDB database.

The project also has a GUI that is used to search the database based on Year and the IMDb rating of a movie/tv show. 

EDIT:

The Executables file now contains files that the user can run on their own machine. The movieWorldGUI folder has a file with the same name that can be run to interact
with the database. The user can apply filters on the database and fetch the intended information. Any issues with the program can be reported here.
