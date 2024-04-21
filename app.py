import os
import json
import sys
from flask import (
    Flask,
    request,
    abort,
    render_template,
    flash,
    session,
    redirect,
    url_for,
    jsonify
)
from models import setup_db, db_drop_and_create_all, setup_db, Actor, Movie
from flask_cors import CORS, cross_origin
from auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')
API_AUDIENCE = os.getenv('API_AUDIENCE')
AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY')


def create_app(test_config=None):

    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config['SECRET_KEY'] = SECRET_KEY
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
        return jsonify({
            'message': 'Welcome to the Capstone project: Casting Agency',
            'author': 'Hsin-Wen Chang',
            'date': '2023-03-14'
        }), 200

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
            movies_data = list(map(lambda movie: movie.format(), movies))

            print('Movies: {}'.format(movies_data))

            if len(movies_data) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'movies': movies_data,
                'total_movies': len(movies_data)
            })

        except Exception as e:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth(permission='patch:movies')
    def update_movie(payload, movie_id):

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            print('Movie: {}'.format(movie))
            movie = Movie(
                title=request.json['title'],
                release_date=request.json['release_year']
            )
            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.id
            }), 200

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

        # add user-submitted data and commit to db
        movie = Movie(
            title=request.json['title'],
            release_date=request.json['release_year']
        )

        try:
            movie.insert()

        except BaseException:
            abort(422)

        return jsonify({
            'success': True,
            'movie': movie.id
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                return json.dumps({
                    'success': False,
                    'error': 'Movie could not be found'
                }), 404

            movie.delete()

            return jsonify({
                'deleted': movie_id,
                'success': True

            }), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors', methods=['GET'])
    @cross_origin()
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        actors_data = list(map(lambda actor: actor.format(), actors))

        # print actors
        print('Actors: {}'.format(actors_data))

        if len(actors_data) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "actors": actors_data
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, actor_id):
        try:
            print('Actor ID: {}'.format(actor_id))
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if actor is None:
                return json.dumps({
                    'success': False,
                    'error': 'Actor could not be found to be deleted',
                }), 404

            actor.delete()

            return jsonify({
                'success': True,
                '   deleted': actor_id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/create', methods=['POST'])
    @cross_origin()
    @requires_auth('post:actors')
    def add_actor(payload):

        if request.json['name'] == '' or request.json['gender'] == '' or request.json['age'] == '':
            abort(422)
        try:
            actor = Actor(
                gender=request.json['gender'],
                name=request.json['name'],
                age=request.json['age'])
            actor.insert()

        except Exception as e:
            print(e)
            abort(422)

        return jsonify({
            "success": True,
            "created_actor_id": actor.id
        }), 200

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app


app = create_app()
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url='https://dev-2rphxhqkvfsgcgle.us.auth0.com' +
    '/oauth/token',
    authorize_url='https://dev-2rphxhqkvfsgcgle.us.auth0.com' +
    '/authorize',
    client_kwargs={
        'scope': 'openid profile email'})


@app.route('/login', methods=['GET'])
@cross_origin()
def login():
    print('Audience: {}'.format(API_AUDIENCE))
    return auth0.authorize_redirect(
        redirect_uri='%s/post-login' % AUTH0_CALLBACK_URL,
        audience=API_AUDIENCE
    )


@app.route('/post-login', methods=['GET'])
@cross_origin()
def post_login():
    token = auth0.authorize_access_token()
    session['token'] = token['access_token']
    print(session['token'])
    return render_template('pages/home.html'), 200


@app.route('/logout')
def log_out():
    session.clear()
    params = {
        'returnTo': url_for(
            'index',
            _external=True),
        'client_id': AUTH0_CLIENT_ID}
    return redirect(
        'https://dev-2rphxhqkvfsgcgle.us.auth0.com' +
        '/v2/logout?' +
        urlencode(params))


if __name__ == '__main__':
    app.run()
