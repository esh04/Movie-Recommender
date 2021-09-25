# Movie-Recommender
- Need someone to just recommend one movie to you without having the hassle to go through ten different streaming apps? 
- This recommendation system is designed to minimize the users overthinking and contemplation.
- We will give you one perfect choice so that you dont have to spend hours searching for what you like. 
- What if you dont like the movie we recommended? No worries, just press pass and we will provide you with another movie. It is that simple. 

## How it works
- Choose the genre you are in the mood for.
- User can also specify the language and the preferable release date of the movie they wish to watch.
- We ask the user to select the movies they have watched and like from a list of 10 movies randomly selected from the top 250 in that genre.
- Depending on the choices they make we provide them with one movie perfectly suited for them

## Recommendation System
- We use the Content-Based Recommendation system where we take your previous likings in order to recommend a movie to you.
- Similar movies are found by transforming parameters like plot, keywords, director, writer, actor, and genre to vectors and then using cosine similarity on them. 
- We use `sklearn CountVectorizer` to convert the parameters from text to vector/token counts. 
- `Cosine Similarity` is used to plot the similarities. The output varies from 0-1 where where 1 denotes 100% similarity. 
- Using this we can find the cosΘ between the two vectors. 
- Once the user selects the movies they like, we find movie recommendations for all of those choices.
- To find the one perfect movie, we primarily sort them on the basis of common suggestions. If two movies are suggested the same number of times, the weighted rating of the movie is considered. 

## Dataset
- We got ratings, crew information, genre for every movie on iMDb from https://www.imdb.com/interfaces/.
- We then got the poster, plot, original language and keywords for every movie using the unique iMDb id with the help of `TMDB API`
- We then grouped all the movies by genre and rated them using the **True Bayesian estimation**.
- Weighted Rating(WR) = (v/v+m).R + (m/m+v).C 
    - Where v is the number of votes, m is the minimum number of votes the movie should get to be considered, C is mean vote and R is the average rating of the movie.
    - We chose m to be 80th percentile of the number of votes in the database which turns out to be 4229 votes.
    - C for our dataset was around 6.

