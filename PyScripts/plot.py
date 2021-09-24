import aiohttp
import asyncio
import pandas as pd
from secrets import api_key

df = pd.read_csv('../data/data.csv', low_memory=False)

overview = [""]*73160
poster = [""]*73160
keywords = [""]*73160
org_lang = [""]*73160
display_title = [""]*73160


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

asyncio.run(main())

df['overview'] = overview
df['poster'] = poster
df['keywords'] = keywords
df['originalLanguage'] = org_lang
df['displayTitle'] = display_title

df.to_csv('../data/data.csv', index=False)

df = df[~df.overview.isnull()]

df.to_csv('../data/data.csv', index=False)
# https://image.tmdb.org/t/p/original/ + path
