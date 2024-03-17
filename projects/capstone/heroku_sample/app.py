import os
import json
import sys
from flask import (
    Flask,
    request,
    abort,
    render_template,
    jsonify
)
from models import setup_db, db_drop_and_create_all, setup_db, Actor, Movie
from flask_cors import CORS, cross_origin
from auth import AuthError, requires_auth
from forms import ActorForm, MovieForm

ACTORS_PER_PAGE = 10


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    @cross_origin()
    def index():
        return render_template('pages/home.html')

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available actors.
    """
    @app.route('/movies', methods=['GET'])
    @cross_origin()
    @requires_auth(permission='get:movies')
    def get_movie(payload):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            movies_data = []
            for movie in movies:
                movies_data.append({
                    'id': movie.id,
                    'title': movie.title,
                    'release_date': movie.release_date
                })

            if len(movies_data) == 0:
                abort(404)

            return render_template(
                'pages/movies.html', movies=movies_data), 200

        except Exception as e:
            print(sys.exc_info())
            abort(422)

    # hadle rout to create new movie from form
    @app.route('/movies', methods=['GET'])
    @cross_origin()
    @requires_auth(permission='post:movies')
    def create_movie_form(payload):
        form = MovieForm()
        return render_template('forms/new_movie.html', form=form)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth(permission='patch:movies')
    def update_movie(payload, id):
        form = MovieForm()
        movie = form.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            return json.dumps({
                'success': False,
                'error': 'Movie could not be found to be updated',
            }), 404

        try:
            if movie:
                form.title.data = movie.title
                form.release_date.data = movie.release_date

            return render_template(
                'forms/edit_movie.html', form=form, movie=movie)

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies', methods=['POST'])
    @cross_origin()
    @requires_auth('post:movies')
    def add_movie(payload):
        '''
        Add a new movie to the database
        '''
        body = request.get_json()

        if body is None:
            abort(400)

        title = body.get('title')
        date = body.get('release_date')

        if date is None or title is None:
            abort(422)

        try:
            new_movie = Movie(
                title=title,
                release_date=date)
            new_movie.insert()

            return render_template('pages/home.html')

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, id):
        try:
            movie = Movie.query.filter(
                Movie.id == id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors', methods=['GET'])
    @cross_origin()
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        actors_data = []
        for actor in actors:
            actors_data.append({
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender,
            })

        return render_template('pages/actors.html', actors=actors_data)
    
    # hadle rout to create new actor from form
    @app.route('/actors', methods=['GET'])
    @cross_origin()
    @requires_auth(permission='post:actors')
    def create_actor_form(payload):
        form = ActorForm()
        return render_template('forms/new_actor.html', form=form)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, id):
        try:
            actor = Actor.query.filter(
                Actor.id == id).one_or_none()

            if actor is None:
                return json.dumps({
                    'success': False,
                    'error': 'Actor could not be found to be deleted',
                }), 404

            actor.delete()

            return render_template('pages/home.html')

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors', methods=['POST'])
    @cross_origin()
    @requires_auth('post:actors')
    def add_actor(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        gender = body.get('gender')
        name = body.get('name')
        age = body.get('age')

        if name is None or name is None or gender is None or age is None:
            abort(422)

        try:
            actor = Actor(
                gender=gender,
                name=name,
                age=age)
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth(permission='patch:actors')
    def update_actor(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        body = request.get_json()

        if body is None:
            abort(422)

        try:
            if 'name' in body:
                actor.name = body.get('name')

            if 'age' in body:
                actor.age = body.get('age')

            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.id
            })

        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return render_template('errors/422.html'), 422

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return render_template('errors/401.html'), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
