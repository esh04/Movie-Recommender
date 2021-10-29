import pickle
from PyScripts.content_based import conditions, final_rec
from flask import Flask, render_template, request, session
from flask_session import Session
import pandas as pd

app = Flask(__name__)

# Configure session to use as filesystem
app.secret_key = 'superSecretKey'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)

# Initial route for the app


@app.route("/", methods=['GET', 'POST'])
def search():
    # If the user has selected the filters then direct them to the options page
    if request.method == 'POST':

        # If the user submitted the form then store the values in the session and check for errors
        # If there are any errors then redirect the user back to initial page with appropriate error message
        if request.form.get("submit"):
            session["genre"] = request.form.get('genre-select')
            session["languages"] = request.form.getlist('languages')
            session["years"] = request.form.getlist('years')

            # Make sure start year isnt greater than end year
            if session["years"][0] > session["years"][1]:
                return render_template('index.html', error=1)

            # Make sure the user has selected at least one language
            if len(session["languages"]) == 0:
                return render_template('index.html', error=2)

        # If the user has selected the options correctly then get the top 10 movies for those filters
        df = (conditions(([session["genre"]]), int(session["years"][0]),
              int(session["years"][1]), session["languages"]))
        l = len(df)

        options = df.head(min(250, l)).sample(n=min(10, l)).to_dict('records')

        session["data"] = ""
        # redirect to the options page
        return render_template('options.html', options=options)

    # Initialize the session variables
    session["genres"] = []
    session["index"] = 0
    session["movies"] = []
    if not session.get('languages'):
        session["languages"] = []

    # Get the available genres
    with open('data/genres.pkl', 'rb') as f:
        session["genres"] = pickle.load(f)

    # Render the initial page
    return render_template('index.html', error=0)


@app.route("/suggestion", methods=['POST'])
def get():

    # If the user has selected the movies then render the recommendation page
    if request.method == 'POST':

        # If the user has submitted the form then store the selected movies in the session else load previously selected movies
        session["movies"] = request.form.getlist('movies') if len(
            request.form.getlist('movies')) else session["movies"]

        # If this is the first time getting the recommendation then use the approriate function
        if session["data"] == "":
            final_movies = final_rec([session["genre"]], session["languages"], session["movies"], int(
                session["years"][0]), int(session["years"][1]))

            dict_obj = final_movies.to_dict('list')
            session['data'] = dict_obj

        dict_obj = session['data'] if 'data' in session else ""
        df = pd.DataFrame(dict_obj)
        final_movie = df.iloc[session["index"]]

        # Increase the index the user is on so that when user presses pass then we can suggest the next movie in the list
        session["index"] += 1

        # Render the recommendation page with the recommended movie
        return render_template('final.html', movie=final_movie)


if __name__ == '__main__':
    app.run()
