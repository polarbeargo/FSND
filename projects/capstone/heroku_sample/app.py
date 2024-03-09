import os
from flask import Flask, request, jsonify, abort
from models import setup_db, db_drop_and_create_all, setup_db, Actor, Movie
from flask_cors import CORS
from projects.capstone.heroku_sample.auth import AuthError, requires_auth

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

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available actors.
    """
    @app.route('/movies', methods=['GET'])
    @requires_auth(permission='get:movies')
    def get_movie(payload):
        try:
            selection = Movie.query.order_by(Movie.id).all()
            # Use the paginate method already provide in the flask-sqlalchemy
            current_movie = Movie.query.order_by(
                Movie.id).paginate(
                page=1, per_page=ACTORS_PER_PAGE).items

            if len(current_movie) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'actors': current_movie,
                'total_actors': len(selection)
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def update_movie(payload, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        body = request.get_json()

        if body is None:
            abort(422)

        try:
            if 'title' in body:
                movie.title = body.get('title')

            if 'age' in body:
                movie.release_date = body.get('release_date')

            movie.update()
            return jsonify({
                'success': True,
                'actor': movie.id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
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

            return jsonify({
                'success': True,
                'created': new_movie.id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
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
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            selection = Actor.query.order_by(Actor.id).all()
            # Use the paginate method already provide in the flask-sqlalchemy
            current_actors = Actor.query.order_by(
                Actor.id).paginate(
                page=1, per_page=ACTORS_PER_PAGE).items

            if len(current_actors) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'actors': current_actors,
                'total_actors': len(selection)
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, id):
        try:
            actor = Actor.query.filter(
                Actor.id == id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors', methods=['POST'])
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

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
