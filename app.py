import pickle
from PyScripts.content_based import conditions, final_rec
from flask import Flask, render_template, request, session
from flask_session import Session
import pandas as pd

app = Flask(__name__)
# Check Configuration section for more details
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':

        if not session.get("languages"):
            session["languages"] = []

        session["genre"] = request.form.get(
            'genre-select') if request.form.get('genre-select') else session["genre"]
        session["languages"] = request.form.getlist('languages') if len(
            request.form.getlist('languages')) else session["languages"]
        session["years"] = request.form.getlist('years') if len(
            request.form.getlist('years')) else session["years"]

        if session["years"][0] > session["years"][1]:
            return render_template('index.html',
                                   genres=session["genres"], error=1, genre=session["genre"])

        if len(session["languages"]) == 0:
            return render_template('index.html',
                                   genres=session["genres"], error=2)

        df = (conditions(([session["genre"]]), int(session["years"][0]),
              int(session["years"][1]), session["languages"]))
        l = len(df)
        options = df.head(min(250, l)).sample(n=min(10, l)).to_dict('records')

        session["data"] = ""
        return render_template('options.html', options=options)

    session["genres"] = []
    session["index"] = 0
    with open('data/genres.pkl', 'rb') as f:
        session["genres"] = pickle.load(f)

    return render_template('index.html',
                           genres=session["genres"], error=0)


@app.route("/suggestion", methods=['POST'])
def get():
    if request.method == 'POST':
        session["movies"] = request.form.getlist('movies') if len(
            request.form.getlist('movies')) else session["movies"]

        if session["data"] == "":
            print('weeeeeeeeeeeee')
            final_movies = final_rec([session["genre"]], session["languages"], session["movies"], int(
                session["years"][0]), int(session["years"][1]))

            dict_obj = final_movies.to_dict('list')
            session['data'] = dict_obj

        dict_obj = session['data'] if 'data' in session else ""
        df = pd.DataFrame(dict_obj)
        final_movie = df.iloc[session["index"]]
        session["index"] += 1

        return render_template('final.html', movie=final_movie)


if __name__ == '__main__':
    app.run(debug=True)
