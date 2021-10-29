import aiohttp
import asyncio
import pandas as pd
from secrets import api_key

df = pd.read_csv('../data/data.csv', low_memory=False)

len = df.shape[0]

overview = [""]*len
poster = [""]*len
keywords = [""]*len
org_lang = [""]*len
display_title = [""]*len


# assigning the request functions to tasks and storing all tasks in a list
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, row in df.iterrows():
            task = asyncio.ensure_future(
                get_data(session, row['titleId'], index))
            task2 = asyncio.ensure_future(
                get_key(session, row['titleId'], index))
            tasks.append(task)
            tasks.append(task2)

        await asyncio.gather(*tasks)


# getting data about the movie from the TMDB API and storing them in respective lists
async def get_data(session, titleId, index):
    url = 'https://api.themoviedb.org/3/movie/' + titleId + \
        '?api_key=' + api_key + '&external_source=imdb_id'

    try:
        async with session.get(url) as response:
            details = await response.json()
            try:
                overview[index] = details['overview']
            except:
                print(details)

            try:
                poster[index] = details['poster_path']
            except:
                print(details)

            try:
                org_lang[index] = details['original_language']
            except:
                print(details)
            try:
                display_title[index] = details['title']
            except:
                print(details)

    except asyncio.TimeoutError:
        print("Error on ", index)

    print("done", index)


# getting keywords for the movie from the TMDB API and storing them in respective list
async def get_key(session, titleId, index):
    url = 'https://api.themoviedb.org/3/movie/' + \
        titleId + '/keywords?api_key=' + \
        api_key + '&external_source=imdb_id'

    try:
        async with session.get(url) as response:
            details = await response.json()
            try:
                keywords[index] = ' '.join(
                    [item["name"] for item in details['keywords']])
            except:
                print(details)

    except asyncio.TimeoutError:
        print("Error on ", index)

    print("done with key", index)

# running all the tasks at once
asyncio.run(main())

# storing the data in from the apis in the dataframe
df['overview'] = overview
df['poster'] = poster
df['keywords'] = keywords
df['originalLanguage'] = org_lang
df['displayTitle'] = display_title

df.to_csv('../data/data.csv', index=False)

# dropping rows with empty overview
df = df[~df.overview.isnull()]

df.to_csv('../data/data.csv', index=False)
# https://image.tmdb.org/t/p/original/ + path
