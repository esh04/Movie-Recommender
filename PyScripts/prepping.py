import pandas as pd
import pickle

def clean(list_):
    list_ = list_.replace(' ','')
    list_ = list_.replace(',', ' ')
    list_ = list_.replace("'", '')
    list_ = list_.replace('[', '')
    list_ = list_.replace(']', '')
    return list_

def rating(df):

    m = df.numVotes.quantile(0.80)
    C = df.averageRating.mean()

    df['weightedRating'] = ((df['numVotes'] / (df['numVotes'] + m) )*df['averageRating']) + ((m/ (m + df['numVotes']))*C )
    df.sort_values('weightedRating', ascending=False, inplace=True)

    return df

def genres(df):
    df.drop(df[df['genres'] == '\\N'].index, inplace = True)

    df = df[df.startYear.str.isnumeric()]

    df['genres'] = df['genres'].str.split(',')

    genres = df.genres.explode().unique()

    with open('../data/genres.pkl', 'wb') as f:
        pickle.dump(genres, f)
    return df

def clean_data(df):
    df['nconst'] = df['nconst'].fillna('[]')
    df['nconst'] = df['nconst'].apply(clean)
    
    df['directors'] = df['directors'].fillna('')
    df['directors'] = df['directors'].apply(clean)
    
    df['writers'] = df['writers'].fillna('')
    df['writers'] = df['writers'].apply(clean)

    return df

def soup(df):
    df['genreString'] = df['genres'].str.join(' ')

    #director is included three times in the soup as it should have more weight as compared to the other cast
    df['soup'] = df['keywords'] + ' ' + df['nconst'] + ' ' +  df['genreString'] + ' ' +  df['writers'] + ' ' +  df['directors'] + ' ' +  df['directors'] +  ' ' + df['directors']
    df = df.drop(['genreString'], axis = 1)
    df['soup'] = df['soup'].fillna('')

    return df

df = pd.read_csv('../data/data.csv')

df = genres(df)
df = rating(df)
df = clean_data(df)
df = soup(df)

df.to_csv('../data/rated_data.csv', index=False)