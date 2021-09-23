#extracting features from plot to compute similarity/dissimilarity
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

def get_recommendations(title, cosine_sim, indices, movie_title):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 30 most similar movies
    sim_scores = sim_scores[1:31]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 30 most similar movies
    return movie_title.iloc[movie_indices]
    # return df['title'].iloc[movie_indices]

def conditions(genres, strDate, endDate, lang):

    df = pd.read_csv('../data/rated_data.csv')
    df = df[(df.genres.apply(lambda x: any(item for item in genres if item in x))) & df['language'].isin(lang) & (df['startYear'].astype(int) <= endDate) & (df['startYear'].astype(int) >= strDate)]
    return df

def fit_and_transform_plot(df):
    tfidf = TfidfVectorizer(analyzer='word',ngram_range=(1, 3),min_df=0, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['overview'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    df = df.reset_index()
    title = df['titles']
    indice = pd.Series(df.index, index=df['title'])
    return cosine_sim, indice, title

def fit_and_transform_soup(df):
    count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    #https://stackoverflow.com/questions/39303912/tfidfvectorizer-in-scikit-learn-valueerror-np-nan-is-an-invalid-document
    count_matrix = count.fit_transform(df['soup'].values.astype('U'))
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    df = df.reset_index()
    title = df['titles']
    indice = pd.Series(df.index, index=df['title'])
    return cosine_sim, indice, title




########################################

df = (conditions(['Drama'],2000,2020, ['hi','en']))
sim, indice, titles = fit_and_transform_soup(df)

get_recommendations('The Shawshank Redemption', sim, indice, titles )
