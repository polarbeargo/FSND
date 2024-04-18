import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

TEST_DB_NAME = os.getenv('TEST_DB_URL')


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = TEST_DB_NAME
        # Define tokens for testing
        self.actors_token = os.getenv('ACTORS_TOKEN')
        self.movies_token = os.getenv('MOVIES_TOKEN')
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_create_movie(self):
        updated_movie = {
            'title': 'Kong: Skull Island',
            'release_year': '2020-01-01'
        }
        res = self.client().post(
            '/movies',
            json=updated_movie,
            headers={
                'Authorization': self.movies_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_movie(self):
        res = self.client().get('/movies', headers={'Authorization':
                                                    self.movies_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_create_actor(self):
        new_actor = {
            'name': 'Michael Bay',
            'age': '60',
            'gender': 'M'
        }
        res = self.client().post('/actors/create', json=new_actor,
                                 headers={'Authorization': self.actors_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_actor(self):
        res = self.client().get('/actors', headers={'Authorization':
                                                    self.actors_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(type(data["actors"]), type([]))

    def test_delete_actor(self):
        res = self.client().delete('/actors/51', headers={'Authorization':
                                                          self.actors_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/0', headers={'Authorization':
                                                         self.movies_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_422_create_actor(self):
        res = self.client().post(
            '/actors/create',
            json={
                'name': '',
                'age': '',
                'gender': '!'},
            headers={
                'Authorization': self.actors_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/11', headers={'Authorization':
                                                          self.actors_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        updated_movie = {
            'title': 'Dune',
            'release_year': '2023-01-01'
        }
        res = self.client().patch('/movies/2', json=updated_movie,
                                  headers={'Authorization': self.movies_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
