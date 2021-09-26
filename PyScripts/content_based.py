from numpy.core.numeric import NaN
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# apply the conditions as mentioned by the user


def conditions(genres, strDate, endDate, lang):

    df = pd.read_pickle('data/data.pkl')
    df = df[(df.genres.apply(lambda x: any(item for item in genres if item in x))) & df['originalLanguage'].isin(
        lang) & (df['startYear'].astype(int) <= endDate) & (df['startYear'].astype(int) >= strDate)]

    l = len(df)

    # take not more than 10k movies
    df = df.head(min(l, 10000))

    return df


def get_recommendations(title, cosine_sim, indices, movie_title):

    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    # enumerate adds counter to the iterable list cosine_sim
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # return 50 similar movies
    sim_scores = sim_scores[1:51]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the titles of the corresponding indices
    return movie_title.iloc[movie_indices]

# https://towardsdatascience.com/basics-of-countvectorizer-e26677900f9c
# https://towardsdatascience.com/using-cosine-similarity-to-build-a-movie-recommendation-system-ae7f20842599


def fit_and_transform_soup(df):

    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
    count = CountVectorizer(ngram_range=(1, 2), min_df=0, stop_words='english')

    # https://stackoverflow.com/questions/39303912/tfidfvectorizer-in-scikit-learn-valueerror-np-nan-is-an-invalid-document
    # transform the text into vectors
    count_matrix = count.fit_transform(df['soup'].values.astype('U'))

    # find the cosΘ between the two vectors i.e. similarity
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # reset index of df and construct reverse mapping so that we can get index with the help of title
    df = df.reset_index()
    title = df['displayTitle']
    indice = pd.Series(df.index, index=df['displayTitle'])

    return cosine_sim, indice, title


def final_rec(genres, languages, movies_list, startYear, endYear):

    # filter out data
    df = (conditions(genres, startYear, endYear, languages))
    chosen_movies = (df[df['displayTitle'].isin(movies_list)])
    soup = chosen_movies['soup'].str.cat(sep = ' ')
    new = {'displayTitle' : 'selectedMovies', 'soup' : soup}
    df = df.append(new, ignore_index=True)

    #fit and transform
    cosine_sim, indice, title = fit_and_transform_soup(df)

    # get recommendations 
    rec = get_recommendations('selectedMovies', cosine_sim, indice, title)

    # find details of those movies
    final_rec = pd.merge(df, rec, how='right', on=['displayTitle'])

    # drop the movies that the user has selected
    final_rec.drop(final_rec[final_rec['displayTitle'].isin(
        movies_list)].index, inplace=True)

    return final_rec