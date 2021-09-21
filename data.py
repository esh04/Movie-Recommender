import pandas as pd

# the .tsv used in the above code can be downloaded from these sites
# names='https://datasets.imdbws.com/name.basics.tsv.gz'
# main = "https://datasets.imdbws.com/title.akas.tsv.gz"
# secondary = "https://datasets.imdbws.com/title.basics.tsv.gz"
# directors = "https://datasets.imdbws.com/title.crew.tsv.gz"
# series = "https://datasets.imdbws.com/title.episode.tsv.gz"
# crew= "https://datasets.imdbws.com/title.principals.tsv.gz"
# ratings = "https://datasets.imdbws.com/title.ratings.tsv.gz"

def main_data():
    chunksize = 100000

    list_of_dataframes = []

    for df in pd.read_csv('./data/main.tsv', sep='\t', chunksize=chunksize):
        df1 = df[(df['language'] == 'hi') | (df['language'] == 'en')]
        list_of_dataframes.append(df1[['titleId','title','language']])

    main = pd.concat(list_of_dataframes)
    main.to_csv('./data/main_new.csv')
    return main

def secondary_data():
    chunksize = 100000

    list_of_dataframes = []

    for df in pd.read_csv('./data/secondary.tsv', sep='\t', chunksize=chunksize):
        df1 = df[df['titleType'] == 'movie']
        list_of_dataframes.append(df1[['tconst','isAdult','genres','startYear']])

    sec = pd.concat(list_of_dataframes)
    sec.to_csv('./data/secondary_new.csv')
    return sec

def crew_data():
    chunksize = 100000

    list_of_dataframes = []

    for df in pd.read_csv('./data/crew.tsv', sep='\t', chunksize=chunksize):
        df1 = df[(df['category'] == 'actor') | (df['category'] == 'actress')]
        list_of_dataframes.append(df1[['tconst','nconst']])

    crew = pd.concat(list_of_dataframes)
    crew.to_csv('./data/crew_new.csv')
    return crew

def actor_data(crew):
    actor_new = crew.groupby('tconst')['nconst'].apply(list)
    actor_new.to_csv('./data/actor_new.csv')
    return actor_new

def merge(main,sec,directors,ratings,actor):

    final=pd.merge(main,sec,how='inner',
                left_on=['titleId'],
                right_on=['tconst'])

    final=pd.merge(final,directors,how='left',
                left_on=['titleId'],
                right_on=['tconst'])
    final=pd.merge(final,ratings,how='left',
               left_on=['titleId'],
               right_on=['tconst'])  
    final=pd.merge(final,actor,how='left',
               left_on=['titleId'],
               right_on=['tconst']) 
    df=final[['titleId', 'title','language','startYear','isAdult','genres','directors','writers','nconst','averageRating','numVotes']]
    return df

main_d = main_data()
sec_d = secondary_data()

#once csv is created can directly get data from csv to speed up the process
# main_d=pd.read_csv('./data/main_new.csv')
# sec_d=pd.read_csv('./data/secondary_new.csv')

directors_d = pd.read_csv('./data/directors.tsv', sep='\t')
ratings_d = pd.read_csv('./data/rating.tsv', sep='\t')         

crew_d = crew_data()
# crew = pd.read_csv('./data/crew_new.csv')

actor_d = actor_data(crew_d)
# actor_d=pd.read_csv('./data/actor_new.csv')

df = merge(main_d,sec_d,directors_d,ratings_d,actor_d)
df.drop_duplicates(subset='titleId', inplace = True)

df.to_csv("./data/data.csv")

