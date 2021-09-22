#id = plot-synopsis-content
import wikipedia
import pandas as pd

df = pd.read_csv('./data/data.csv')

plot = []

for index, row in df.iterrows():
    
    search = row['title'] + ' (' + row['startYear'] + ' film)'
    try:
        section = wikipedia.WikipediaPage(search).section('Plot')
        plot.append(section)
        # print(section)
    except:
        plot.append('')
    
df['plot'] = plot

df.to_csv('./data/data_plots.csv')