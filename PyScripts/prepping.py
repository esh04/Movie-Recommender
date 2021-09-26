import pandas as pd
import pickle

def clean(list_):
    list_ = list_.replace(' ','')
    list_ = list_.replace(',', ' ')
    list_ = list_.replace("'", '')
    list_ = list_.replace('[', '')
    list_ = list_.replace(']', '')
    return list_

# rate all movies based in the true bayesian estimation (refer README.md)
def rating(df):

    m = df.numVotes.quantile(0.80)
    C = df.averageRating.mean()

    df['weightedRating'] = ((df['numVotes'] / (df['numVotes'] + m) )*df['averageRating']) + ((m/ (m + df['numVotes']))*C )
    df.sort_values('weightedRating', ascending=False, inplace=True)

    return df

# store all possible genres in a pickle file
def genres(df):
    # drop all null genres
    df.drop(df[df['genres'] == '\\N'].index, inplace = True)

    # filter out only valid years
    df = df[df.startYear.str.isnumeric()]

    # convert string of genres to list
    df['genres'] = df['genres'].str.split(',')

    genres = df.genres.explode().unique()

    # pickle file of possible genres
    with open('../data/genres.pkl', 'wb') as f:
        pickle.dump(genres, f)
    return df

# clean the data so they can be combined to form a final string of parameters, remove space between first name and last name
def clean_data(df):
    df['nconst'] = df['nconst'].fillna('[]')
    df['nconst'] = df['nconst'].apply(clean)
    
    df['directors'] = df['directors'].fillna('')
    df['directors'] = df['directors'].apply(clean)
    
    df['writers'] = df['writers'].fillna('')
    df['writers'] = df['writers'].apply(clean)

    return df

# combine all parameters together
def soup(df):
    # make a string out of list of genre
    df['genreString'] = df['genres'].str.join(' ')

    #director is included three times in the soup as it should have more weight as compared to the other cast
    df['soup'] = df['keywords'] + ' ' + df['nconst'] + ' ' +  df['genreString'] + ' ' +  df['writers'] + ' ' +  df['directors'] + ' ' +  df['directors'] +  ' ' + df['directors'] + ' ' + df['overview']
    df = df.drop(['genreString'], axis = 1)
    df['soup'] = df['soup'].fillna('')

    return df

df = pd.read_csv('../data/data.csv')

df = genres(df)
df = rating(df)
df = clean_data(df)
df = soup(df)

df = df[(df['originalLanguage'] == 'hi') | (df['originalLanguage'] == 'en')]
df['poster'] = df['poster'].fillna(' ')
df = df[['titleId','displayTitle','genres', 'startYear','originalLanguage', 'soup', 'weightedRating', 'overview', 'poster', 'directors','averageRating','nconst']]

df.to_pickle('../data/data.pkl')
df.to_csv('../data/rated_data.csv')

