import pickle
from PyScripts.content_based import conditions
from flask import Flask, render_template, request
import sys
sys.path.append('/PyScripts/')

app = Flask(__name__)


@app.route('/')
def index():
    genres = []

    with open('data/genres.pkl', 'rb') as f:
        genres = pickle.load(f)

    return render_template('index.html',
                           genres=genres)


@app.route("/", methods=['GET', 'POST'])
def search():
    genre = request.form.get('genre-select')
    languages = request.form.getlist('languages')

    df = (conditions(([genre]), 2000, 2020, languages))
    options = df.head(250).sample(n=10).to_dict('records')

    return render_template('options.html', options=options)


@app.route("/suggestion", methods=['GET', 'POST'])
def get():
    movies = request.form.getlist('movies')

    # l = (len(df))

    # print(df.head(250).sample(n=10))

    # df = df.head(min(l, 10000))
    # df['soup'] = df['soup'] + ' ' + df['overview']
    # sim, indice, titles = fit_and_transform_soup(df)

    # rec = get_recommendations(
    #     'Harry Potter and the Deathly Hallows: Part 2', sim, indice, titles)
    # print(movies)

    return 'hey'


if __name__ == '__main__':
    app.run(debug=True)
