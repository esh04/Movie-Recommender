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


def get_recommendations(title, cosine_sim, indices, movie_title, len):

    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    # enumerate adds counter to the iterable list cosine_sim
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    if (len > 5):
        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]
    else:
        sim_scores = sim_scores[1:16]

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
    all_rec = pd.Series(dtype=object)

    l = len(movies_list)

    # filter out data
    df = (conditions(genres, startYear, endYear, languages))

    #fit and transform
    cosine_sim, indice, title = fit_and_transform_soup(df)

    # get recommendations for each movie
    for movie in movies_list:
        rec = get_recommendations(movie, cosine_sim, indice, title, l)
        all_rec = pd.concat([rec, all_rec])

    # find count of all movies recommended
    new_df = all_rec.value_counts().rename_axis('displayTitle').to_frame('count')

    # find details of those movies
    final_rec = pd.merge(df, new_df, how='right', on=['displayTitle'])

    # sort them primarily on the basis of count, if count is same then by rating
    final_rec = final_rec.sort_values(
        ['count', 'weightedRating'], ascending=False)

    # drop the movies that the user has selected
    final_rec.drop(final_rec[final_rec['displayTitle'].isin(
        movies_list)].index, inplace=True)
    return final_rec
