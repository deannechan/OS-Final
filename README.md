# movie_recommender
Movie recommendation system

Preprocessing:

  1. Read .dat files and parse them using python code.
  2. Convert them to following formats,
  Create a USER.json file as follows
  
      {
        "user":"user-name",
        "movie_id":"movie-id",
        "rating":"rating"
      }
   
  and MOVIE.json file as follows,

      {
        "movie_name":"name",
        "movie_id":"id",
        "actors":["actor1","actor2"],
        "director":"director_name",
        "genre":"type"
      }

Training:
  
  1. Read jsin files and extract data.
  2. Create following lists from the data.
    1. List of user and movies:
       (user, movie, rating)
    2. List of movies:
       (id, movie)
    3. Similarly map list for actors, directors, genres (map each object to id).
    
  3. Calculate count of users, movies, actors, directors and genres.
  4. Create graph and import above parameters.
  5. Calculate affinities between actor-director, actor-genre, director-genre.
  6. Store weights in extrenal pickle file.
  
Recommendation:
  
  1. Create a query format.
  2. Load weights form pickle file.
  3. Recommend movies
  
