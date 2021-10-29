import pandas as pd

# the .tsv used in the above code can be downloaded from these sites
# names='https://datasets.imdbws.com/name.basics.tsv.gz'
# main = "https://datasets.imdbws.com/title.akas.tsv.gz"
# secondary = "https://datasets.imdbws.com/title.basics.tsv.gz"
# directors = "https://datasets.imdbws.com/title.crew.tsv.gz"
# series = "https://datasets.imdbws.com/title.episode.tsv.gz"
# crew= "https://datasets.imdbws.com/title.principals.tsv.gz"
# ratings = "https://datasets.imdbws.com/title.ratings.tsv.gz"

# from main.tsv we wish to extract the titleID, titles and languages of movies available on iMDb
def main_data():
    chunksize = 100000 # the number of rows to be read into the dataframe at any single time in order to fit into the local memory. 

    list_of_dataframes = []

    for df in pd.read_csv('../data/main.tsv', sep='\t', chunksize=chunksize):
        # taking only those movies that are in hindi or english
        df1 = df[(df['language'] == 'hi') | (df['language'] == 'en')]
        list_of_dataframes.append(df1[['titleId','title','language']])

    main = pd.concat(list_of_dataframes)
    main.to_csv('../data/main_new.csv', index=False)
    return main

# from secondary.tsv we wish to extract the genre, year of release and whether the movie is an adult movie
def secondary_data():
    chunksize = 100000

    list_of_dataframes = []

    for df in pd.read_csv('../data/secondary.tsv', sep='\t', chunksize=chunksize):
        # taking only those titles that belong to movies
        df1 = df[df['titleType'] == 'movie']
        list_of_dataframes.append(df1[['tconst','isAdult','genres','startYear']])

    sec = pd.concat(list_of_dataframes)
    sec.to_csv('../data/secondary_new.csv', index=False)
    return sec

# from names.tsv names of all the crew members along with their unique ids
def names_of_crew():

    chunksize = 100000

    list_of_dataframes = []

    for df in pd.read_csv('../data/names.tsv', sep='\t', chunksize=chunksize):
        list_of_dataframes.append(df[['nconst','primaryName']])

    names_d = pd.concat(list_of_dataframes)

    names = names_d.set_index('nconst')['primaryName']
    return names

# from crew.tsv we extract unique ids of actors corresponding to every movie
def crew_data():
    chunksize = 100000

    list_of_dataframes = []

    for df in pd.read_csv('../data/crew.tsv', sep='\t', chunksize=chunksize):
        # take only those members of crew that are actors
        df1 = df[(df['category'] == 'actor') | (df['category'] == 'actress')]
        list_of_dataframes.append(df1[['tconst','nconst']])

    crew = pd.concat(list_of_dataframes)
    crew.to_csv('../data/crew_new.csv', index=False)
    return crew

# map corresponding actor ids to their names
def actor_data(crew, names):
    crew['nconst'] = crew['nconst'].map(names)
    # making a list of all actors that acted in the same movie
    actor_new = crew.groupby('tconst')['nconst'].apply(list)
    actor_new.to_csv('../data/actor_new.csv', index=False)
    return actor_new

# merging all the data recieved
def merge(main,sec,actor,names):

    # from directors.tsv we extract unique ids of directors and writers corresponding to every movie id
    directors = pd.read_csv('../data/directors.tsv', sep='\t')

    # from rating.tsv we extract the number of votes and average rating given to every movie on iMDb
    ratings = pd.read_csv('../data/rating.tsv', sep='\t')

    # the merge between main and secondary data is inner as we want the ids to be of *movies* of the the given languages hence they must be in both dataframes
    final=pd.merge(main,sec,how='inner',
                left_on=['titleId'],
                right_on=['tconst'])

    # all the other merges are left as we need them to compulsorily exist in the final dataframe, values in the other dataframe can be null
    final=pd.merge(final,directors,how='left',
                left_on=['titleId'],
                right_on=['tconst'])
    final=pd.merge(final,ratings,how='left',
               left_on=['titleId'],
               right_on=['tconst'])  
    final=pd.merge(final,actor,how='left',
               left_on=['titleId'],
               right_on=['tconst']) 

    # mapping the unique ids of writers and directors to their names
    final['writers'] = final['writers'].map(names)
    final['directors'] = final['directors'].map(names)

    # filtering the final dataframe
    df=final[['titleId', 'title','language','startYear','isAdult','genres','directors','writers','nconst','averageRating','numVotes']]   
    return df


# _______________________________________________________________________

main_d = main_data()
sec_d = secondary_data()

#once csv is created can directly get data from csv to speed up the process
# main_d=pd.read_csv('../data/main_new.csv')
# sec_d=pd.read_csv('../data/secondary_new.csv')       

names_d = names_of_crew()

crew_d = crew_data()
# crew_d = pd.read_csv('../data/crew_new.csv')
actor_d = actor_data(crew_d, names_d)
# actor_d=pd.read_csv('../data/actor_new.csv')

df = merge(main_d,sec_d,actor_d,names_d)

# some movies are repetative and some are present in both chosen languages
df.drop_duplicates(subset='titleId', inplace = True)

# only wish to recommend movies after 1990
df = df[df['startYear'] > '1990']

df.to_csv("../data/data.csv", index=False)

