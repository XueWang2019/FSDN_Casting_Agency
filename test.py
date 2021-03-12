import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "casting_agency_3"
        # project_dir = os.path.dirname(os.path.abspath(__file__))
        # self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'xxxx', 'localhost:5432', self.database_name)
        self.database_path = os.environ['DATABASE_URL']

        release_date = datetime(date.today().year, date.today().month, date.today().day)

        self.new_movie = {
            "title": "udacity13",
            "release_date": release_date
        }
        self.new_actor = {
            'name': 'hahaha',
            'age': '45',
            'gender': 'femal'
        }
        setup_db(self.app)

        self.assistant_header = os.environ['assistant_token']
        self.director_header = os.environ['director_token']
        self.producer_header = os.environ['producer_token']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    # error test for post_movie
    def test_1_401_post_movie_without_auth_header(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # post:movies endpoint test
    def test_2_post_movies(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={'Authorization': 'Bearer ' + self.producer_header})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # post:actors endpoint test
    def test_3_post_actors(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={'Authorization': 'Bearer ' + self.producer_header})
        print(res.data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(data['new_actor'])

    # post:actors endpoint error test
    def test_4_401_post_actor_without_headers(self):
        res = self.client().post('/actors', json={"name": "aaa", "age": 15, "gender": "female"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # error test for post_movie
    def test_5_401_get_movie_without_auth_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')
    
    # get:movies endpoint test
    def test_6_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization':
                                                    'Bearer ' + self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # get:actors endpoint error test
    def test_7_401_get_actors_without_auth_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # get:actors endpoint tst
    def test_8_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization':
                                                    'Bearer ' + self.producer_header})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # patch:movies endpoint error test
    def test_9_patch_movies_without_auth_header(self):
        res = self.client().patch('/movies/1', json={"title": "fly"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # patch:movies endpoint test
    def test_90_patch_movies(self):
        res = self.client().patch('/movies/1',
                                  json={"title": "fly"}, headers={'Authorization':
                                                                  'Bearer ' + self.producer_header})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # patch:actors endpoint error test
    def test_91_patch_actors(self):
        res = self.client().patch('/actors/1', json={"name": "huhuhu"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # patch:actors endpoint test
    def test_92_patch_actors(self):
        res = self.client().patch('/actors/1',
                                  json={"name": "huhu"}, headers={'Authorization':
                                                                  'Bearer ' + self.producer_header})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # delete:movies endpoint error test
    def test_93_delete_movies(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # delete:movies endpoint test
    def test_94_delete_movies(self):
        res = self.client().delete('/movies/1', headers={'Authorization': 'Bearer ' + self.producer_header})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # delete:actors endpoint error test
    def test_95_delete_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # delete:actors endpoint test
    def test_96_delete_actors(self):
        res = self.client().delete('/actors/1', headers={'Authorization': 'Bearer ' + self.producer_header})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()