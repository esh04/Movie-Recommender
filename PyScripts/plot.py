import aiohttp
import asyncio
import pandas as pd
from secrets import api_key

df = pd.read_csv('../data/data.csv')

overview = [""]*73160
poster = [""]*73160
keywords = [""]*73160


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


async def get_data(session, titleId, index):
    url = 'https://api.themoviedb.org/3/movie/' + titleId + \
        '?api_key=' + api_key + '&external_source=imdb_id'

    try:
        async with session.get(url) as response:
            details = await response.json()
            try:
                overview[index] = details['overview']
            except:
                overview[index] = []
                print(details)

            try:
                poster[index] = details['poster_path']
            except:
                poster[index] = []
                print(details)
    except asyncio.TimeoutError:
        print("Error on ", index)

    print("done", index)


async def get_key(session, titleId, index):
    url = 'https://api.themoviedb.org/3/movie/' + \
        titleId + '/keywords?api_key=' + \
        api_key + '&external_source=imdb_id'

    try:
        async with session.get(url) as response:
            details = await response.json()
            try:
                keywords[index] = details['keywords']
            except:
                keywords[index] = []
                print(details)

    except asyncio.TimeoutError:
        print("Error on ", index)

    print("done with key", index)

asyncio.run(main())

df['overview'] = overview
df['poster'] = poster
df['keywords'] = keywords

df.to_csv('../data/data_new.csv')
# https://image.tmdb.org/t/p/original/ + path
