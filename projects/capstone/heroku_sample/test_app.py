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
        self.database_path = TEST_DB_NAME
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

    def test_get_movie(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])

    def test_get_actor(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])

    def test_404_get_actors(self):
        res = self.client().get('/actors?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        res = self.client().delete('/actors/10')
        data = json.loads(res.data)

        question = Actor.query.filter(Actor.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 10)
        self.assertTrue(data['success'])
        self.assertEqual(question, None)

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_movie(self):
        res = self.client().post('/movies', json={
            'title': 'Test title',
            'release_date': '2021-01-01'
        })
        

    def test_422_create_movie(self):
       res = self.client().post('/movies', json={
           'title': 'Test title'
       })
       data = json.loads(res.data)
       self.assertEqual(res.status_code, 422)
       self.assertEqual(data['success'], False)
       
    def test_422_create_actor(self):
         res = self.client().post('/actors', json={
              'name': 'Test name'
         })
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 422)
         self.assertEqual(data['success'], False)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_actor(self):
        res = self.client().post('/actors', json={
            'name': 'Test name',
            'age': '20',
            'gender': 'M'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

