# Movie-Recommender

## Dataset

- We got ratings, crew information, genre for every movie on iNDb from https://www.imdb.com/interfaces/.

- We then got the poster, plot and keywords for every movie using the unique iNDb id with the help of `TMDB API`

- We then grouped all the movies by genre and rated them using the **True Bayesian estimation**.
- Weighted Rating(WR) = (v/v+m).R + (m/m+v).C 

    - Where v is the number of votes, m is the minimum number of votes the movie should get to be considered, C is mean vote and R is the average rating of the movie.
    - We chose m to be 80th percentile of the number of votes in the database which turns out to be 4229 votes.
    - C for our dataset was around 6.