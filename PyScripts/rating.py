import pandas as pd
import pickle

df = pd.read_csv('../data/data.csv')
m = df.numVotes.mean()*0.1
C = df.averageRating.mean()

df['weightedRating'] = ((df['numVotes'] / df['numVotes'] + m )*df['averageRating']) + ((m/ m + df['numVotes'])*C )

df.drop(df[df['genres'] == '\\N'].index, inplace = True)

df['genres'] = df['genres'].str.split(',')

genres = df.genres.explode().unique()

with open('../data/genres.pkl', 'wb') as f:
    pickle.dump(genres, f)

df.sort_values('weightedRating', ascending=False, inplace=True)

df.to_csv('../data/rated_data.csv', index=False)