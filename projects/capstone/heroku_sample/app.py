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
from forms import ActorForm, MovieForm

ACTORS_PER_PAGE = 10

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
        return render_template('pages/home.html'), 200

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
    @app.route('/movies/create', methods=['GET'])
    @cross_origin()
    @requires_auth(permission='get:movieform')
    def create_movie_form(payload):
        form = MovieForm()
        return render_template('forms/new_movie.html', form=form),200

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth(permission='patch:movies')
    def update_movie(payload, movie_id):
        form = MovieForm()
        movie = form.query.filter(Movie.id == movie_id).one_or_none()

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
                'forms/edit_movie.html', form=form, movie=movie), 200

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
        print('Movie added successfully 1')
        # add user-submitted data and commit to db
        print(request.json['title'])
        movie = Movie(
            title=request.json['title'],
            release_date=request.json['release_year']
        )
        print('Movie added successfully 2')
        try:
            movie.insert()
            # print 1
            print('Movie added successfully')
             # On successful db insert, flash success
            flash(request.json['title'] + ' was successfully listed!')
        except:
            # On unsuccessful db insert, flash an error
            flash(
                'Error: Movie ' +
                request.json['title'] +
                ' was not listed. Please check your inputs and try again :)')
            print(sys.exc_info())

        return render_template('pages/home.html'),200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, movie_id):
        try:
            print('Movie ID: {}'.format(movie_id))
            movie = Movie.query.get(movie_id)

            if movie is None:
                return json.dumps({
                    'success': False,
                    'error': 'Movie could not be found'
                }), 404

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id
            }), 200

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

        return render_template('pages/actors.html', actors=actors_data), 200

    # hadle rout to create new actor from form
    @app.route('/actors/create', methods=['GET'])
    @cross_origin()
    @requires_auth(permission='pget:actorform')
    def create_actor_form(payload):
        form = ActorForm()
        return render_template('forms/new_actor.html', form=form), 200

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

            return render_template('pages/home.html'), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/create', methods=['POST'])
    @cross_origin()
    @requires_auth('post:actors')
    def add_actor(payload):
        print('Hi actor')
        print(request.json['name'])
        try:
            actor = Actor(
                gender=request.json['gender'],
                name=request.json['name'],
                age=request.json['age'])
            actor.insert()

        except Exception as e:
            print(e)
            abort(422)

        return render_template('pages/home.html'), 200

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @cross_origin()
    @requires_auth(permission='patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

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
            }), 200

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
