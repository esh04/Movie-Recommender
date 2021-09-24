import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# apply the conditions as mentioned by the user
def conditions(genres, strDate, endDate, lang):
    
    df = pd.read_csv('../data/rated_data.csv')
    df = df[(df.genres.apply(lambda x: any(item for item in genres if item in x))) & df['orginalLanguage'].isin(lang) & (df['startYear'].astype(int) <= endDate) & (df['startYear'].astype(int) >= strDate)]
    return df

def get_recommendations( title, cosine_sim, indices , movie_title ):

    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    # enumerate adds counter to the iterable list cosine_sim
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 30 most similar movies
    sim_scores = sim_scores[1:31]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the titles of the corresponding indices
    return movie_title.iloc[movie_indices]

# https://towardsdatascience.com/basics-of-countvectorizer-e26677900f9c
# https://towardsdatascience.com/using-cosine-similarity-to-build-a-movie-recommendation-system-ae7f20842599

def fit_and_transform_soup(df):

    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
    count = CountVectorizer(ngram_range=(1, 2), min_df=0, stop_words='english')
  
    #https://stackoverflow.com/questions/39303912/tfidfvectorizer-in-scikit-learn-valueerror-np-nan-is-an-invalid-document
    #transform the text into vectors
    count_matrix = count.fit_transform(df['soup'].values.astype('U'))

    # find the cosΘ between the two vectors i.e. similarity
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # reset index of df and construct reverse mapping so that we can get index with the help of title
    df = df.reset_index()
    title = df['title']
    indice = pd.Series(df.index, index=df['title'])

    return cosine_sim, indice, title


########################################

df = (conditions((['Drama']),2000,2020, ['en']))
l = (len(df))

print(df.head(250).sample(n=10))

df = df.head(min(l,10000))
df['soup'] = df['soup'] + ' ' + df['overview']
sim, indice, titles = fit_and_transform_soup(df)

rec = get_recommendations('Harry Potter and the Deathly Hallows: Part 2', sim, indice, titles )
print(rec)