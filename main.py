import datetime
import random

from flask import Flask, render_template, request, url_for, redirect, flash

import tmdb

FAVORITES = set()

app = Flask(__name__)
app.secret_key = b'zgadnij'


@app.route('/')
def homepage():
    available_lists = ['now_playing', 'popular', 'top_rated', 'upcoming']
    selected_list = request.args.get('list_type', "popular")
    if selected_list not in available_lists:
        selected_list = 'popular'
    displayed_number = int(request.args.get('how_many', 8))
    movies = tmdb.get_movies(how_many=displayed_number,
                                    list_type=selected_list)
    return render_template("homepage.html", movies=movies,
                           current_list=selected_list,
                           available_lists=available_lists)


@app.context_processor
def utility_processor():                # str 25 materiałów
    def tmdb_image_url(path, size):
        return tmdb.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb.get_single_movie(movie_id)
    cast = tmdb.get_single_movie_cast(movie_id)
    movie_images = tmdb.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])
    return render_template("movie_details.html", movie=details,
                           cast=cast, selected_backdrop=selected_backdrop)


@app.route('/search')
def search():
    return render_template("series.html", movies=movies,
                           search_query=search_query)


@app.route('/today')
def today():
    movies = tmdb.get_airing_today()
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)


@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Dodano film {movie_title} do ulubionych!')
    return redirect(url_for('homepage'))


@app.route("/favorites")
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template("homepage.html", movies=movies)


if __name__ == '__main__':
    app.run(debug=True)