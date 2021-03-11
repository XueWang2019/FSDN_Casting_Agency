import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor
from datetime import datetime,date
from dotenv import load_dotenv

load_dotenv()


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "casting_agency_3"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        #self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'xxxx', 'localhost:5432', self.database_name)
        #self.database_path = os.getenv("postgresql://postgres:xxxx@localhost:5432/casting_agency_3")
        self.database_path = 'postgres://otbhtrmxtwmtpi:e00a8e4c6deaf0dde8216132acb9cb10f3bfeed738ef018612e387b85044a6d7@ec2-54-145-102-149.compute-1.amazonaws.com:5432/d5a8bq91i5u0hk'

        release_date = datetime(date.today().year, date.today().month, date.today().day)

        self.new_movie = {
            "title": "udacity13",
            "release_date":release_date
        }
        self.new_actor = {
            'name': 'hahaha',
            'age': '45',
            'gender':'femal'
        }
        setup_db(self.app)


        self.assistant_header='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1vLVRYY2NGeUF4YU5sdXIwUFhkZiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY2V1ZGFjaXR5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDQyNDljYzhlZGZjYzAwNjk0ZmU0MTMiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MTU0ODk0MjEsImV4cCI6MTYxNTU3NTgyMSwiYXpwIjoiV2k2QWtNYWxiUXNxNmIzczR4QUNkMGJzSE9JSldKSEciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.jduncE14ZWzaSp79MigyQxUUFX7YcL9rYOwDtIpGWOVXMqrcAHCEdbzsNtK8gwF-zvvGPNuxsFlzZrXA8fTgRD5IcMqI4wLLogoQ81ZRIQWy6JDcApErbAI_ltMZsudHrAftxBXjuessmfXYzs6h8jODigFQc7l4FM_7lUrI2UwJweid-4Jg9-1icoxLGw8HCZ_ZcbnC9ztBHL9FgbWiTGf0oAAsvjh7TjFsOVFrXIY2T35EXCP5UdFJklR0WlKzL7s-rP7gEdvt_rK43kGVLgVoklMfntYDW3fadHrGEuLpZWdz8l25x-ri7-nusY2oTAtzVcPLMS3PoYQi16Q0gw'
        self.director_header='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1vLVRYY2NGeUF4YU5sdXIwUFhkZiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY2V1ZGFjaXR5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDQyNGEyMDZiMzMzYzAwNjkzMTRkMmIiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MTU0ODkwODksImV4cCI6MTYxNTU3NTQ4OSwiYXpwIjoiV2k2QWtNYWxiUXNxNmIzczR4QUNkMGJzSE9JSldKSEciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.eybI61OkjtsNvVk7JSdV4qWbQnA9Bp2JePAqOjHogRw0RyMpXqL0uMbBbBZmWetOISk_Q0WbpncZSS0KcHSaSeEuaY7aE-g30rb9oJQcMNio8v6gTe_ytmKKV5Ln9m1JB9EaS8ds_By838wQ8aKRg0jPr_0aXK7lunsAILIE4xzJKWexUeJIykhl-qBdR0fEOVrMFQ8t6tzC85DG8E_xzxIBRTZ9FEV-dnvQX0qfM0aXPsdkgyJOzP-DjcLN9I1xzeKDb0GJmGHCxBc0mTeH2yNqXspCwK2nEBoZi0dF8KZZw8m9D6snAbc_TaCuuB_uvk6VzbXeLOTaWYaG3t5YJA'
        self.producer_header='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1vLVRYY2NGeUF4YU5sdXIwUFhkZiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY2V1ZGFjaXR5LmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDQyNGE2NThlZGZjYzAwNjk0ZmU0NmYiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MTU0NTcyMDUsImV4cCI6MTYxNTU0MzYwNSwiYXpwIjoiV2k2QWtNYWxiUXNxNmIzczR4QUNkMGJzSE9JSldKSEciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.hk-jfcgD1H3k8N5PoWneQINx_En46Le0CeCjP05zOlW4QUUHoWxZ-CZOc8L87_4CtzuE8otTDZokxyfFZrV2m248AdPgq6nLjo6g_AWMIpzwfGhxPMUYnz6JjTgaqTgzTjhPmVm5vEY_rBkd8gpBXzaAVgXRPC-TeHS7nCcsXCvNj3hK4zYdUWatpvsnL4xPpszn3yIsX6k0MnsTr8lLgH0cHiHVhcmMdb32tfDwWR6r_1Jj5xpAo4tDEvhfEha7F2iklYHvf7SN-3vERCPaHYyjb9jcDwiyEBjMLMO0HdVTKSsTQGLb3W8QyWq0b96Mv42kPDUChY4yLNraMWcHjA'
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #self.db.drop_all()
            #self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    #error test for post_movie
    def test_1_401_post_movie_without_auth_header(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    #post:movies endpoint test
    def test_2_post_movies(self):
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization':'Bearer ' + self.producer_header})
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
    

    #post:actors endpoint error test
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
        res = self.client().delete('/movies/1', headers={'Authorization':'Bearer ' + self.producer_header})
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
        res = self.client().delete('/actors/1', headers={'Authorization':'Bearer ' + self.producer_header})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()