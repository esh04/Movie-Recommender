import pandas as pd
import requests # to make TMDB API calls
from secrets import api_key

df = pd.read_csv('./data/data.csv')

overview = []
poster = []
keywords = []

for index, row in df.iterrows():
    url = 'https://api.themoviedb.org/3/movie/' + row['titleId'] + '?api_key=' + api_key + '&external_source=imdb_id'

    url_key = 'https://api.themoviedb.org/3/movie/' + row['titleId'] + '/keywords?api_key=' + api_key +'&external_source=imdb_id'

    response = requests.get(url)
    details = response.json()

    response_key = requests.get(url_key)
    details_key = response_key.json()

    try:
        overview.append(details['overview'])

    except:
        overview.append([])
        print(details)

    try:
        poster.append(details['poster_path'])
    except:
        poster.append([])
        print(details)

    try:
        keywords.append(details_key['keywords'])
    except:
        keywords.append([])
        print(details_key)

    print("done")

df['overview'] = overview
df['poster'] = poster
df['keywords'] = keywords

df.to_csv('./data/data_new.csv')
# https://image.tmdb.org/t/p/original/ + path 