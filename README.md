# Movie-Recommender
Need someone to just recommend one movie to you without having the hassle to go through ten different options? 

We will give you one perfect choice so that you dont have to spend hours searching for what you like. 

Choose the genre, language and preferred time period depending on your mood. When provided with the ten most popular movies in that genre, choose the ones you have seen and you like. That is it. Your work is done. We will then based on those choices provide you with one perfect option and all the details you need to know about that movie.

What if you dont like the movie we recommended? No worries, just press pass and we will provide you with another movie. It is that simple. 

## Recommendation System
We use the Content-Based Recommendation system where we take your previous likings in order to recommend a movie to you based on their overview, keywords, genre, director, writer and the main cast as parameters to calculate similarity

We used `sklearn CountVectorizer` to convert the parameters from text to vector/token counts. 

Then, `Cosine Similarity` is used to plot the similarities. The output varies from 0-1 where where 1 denotes 100% similarity. 

Using this we can find the cosΘ between the two vectors. 

## Dataset

- We got ratings, crew information, genre for every movie on iMDb from https://www.imdb.com/interfaces/.

- We then got the poster, plot, original language and keywords for every movie using the unique iMDb id with the help of `TMDB API`

- We then grouped all the movies by genre and rated them using the **True Bayesian estimation**.
- Weighted Rating(WR) = (v/v+m).R + (m/m+v).C 

    - Where v is the number of votes, m is the minimum number of votes the movie should get to be considered, C is mean vote and R is the average rating of the movie.
    - We chose m to be 80th percentile of the number of votes in the database which turns out to be 4229 votes.
    - C for our dataset was around 6.

