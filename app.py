import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

from models import setup_db, Movie, Actor, Scene, db_drop_and_create_all
from auth import AuthError, requires_auth

from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """ uncomment at the first time running the app """
    # db_drop_and_create_all()

    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'message': 'Hello,hello, World!'})

    @app.route("/movies")
    @requires_auth("get:movies")
    def get_movies(payload):
        try:
            movies = Movie.query.order_by(Movie.release_date).all()
            movie = []
            movie = [mov.title for mov in movies]
            return jsonify(
                {
                    "success": True,
                    "movie name": movie
                }
            ), 200
        except:
            abort(500)

    @app.route("/actors")
    @requires_auth("get:actors")
    def get_actors(payload):
        try:
            actors = Actor.query.order_by(Actor.name).all()
            actor = []
            actor = [act.name for act in actors]
            return jsonify(
                {
                    "success": True,
                    "actor": actor
                }
            ), 200
        except:
            abort(500)

    @app.route("/movies", methods=['POST'])
    @requires_auth("post:movies")
    def add_movies(payload):
        try:
            body = request.get_json()
            title = body.get('title')
            release_date = body.get('release_date')

            if title is None:
                abort(400)
            else: movie = Movie(title=title, release_date=release_date)

            movie.insert()
            return jsonify(
                {
                    "success": True,
                    "title": title,
                    "release_date": release_date
                }
            ), 200
        except:
            abort(422)

    @app.route("/actors", methods=['POST'])
    @requires_auth("post:actors")
    def add_actors(payload):
        try:
            body = request.get_json()
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')

            if name is None:
                abort(404)
            else:
                actor = Actor(name=name, age=age, gender=gender)

            actor.insert()
            return jsonify(
                {
                    "success": True,
                    "name": name,
                    "age": age,
                    "gender": gender
                }
            ), 200
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth("patch:movies")
    def update_movies(payload, id):
        req = request.get_json()
        movies = Movie.query.filter(Movie.id == id).one_or_none()
        if not movies:
            abort(404)
        try:
            req_title = req.get('title')
            req_release_date = req.get('release_date')
            if req_title:
                movies.title = req_title
            if req_release_date:
                movies.release_date = req_release_date
        except Exception as e:
            print(e)
            abort(401)
        return jsonify({"success": True, "movie": [movies.details()]}), 200

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth("patch:actors")
    def update_actors(payload, id):
        req = request.get_json()
        actors = Actor.query.filter(Actor.id == id).one_or_none()
        if not actors:
            abort(404)
        try:
            req_name = req.get('name')
            req_age = req.get('age')
            req_gender = req.get('gender')

            if req_name:
                actors.name = req_name
            if req_age:
                actors.age = req_age
            if req_gender:
                actors.gender= req_gender
        except Exception as e:
            print(e)
            abort(401)
        return jsonify({"success": True, "actor": [actors.details()]}), 200

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth("delete:movies")
    def delete_movies(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify(
                {
                    "success": True,
                    "delete": id
                }
            )
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth("delete:actors")
    def delete_actors(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            return jsonify(
                {
                    "success": True,
                    "delete": id
                }
            )
        except:
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def Auth_Error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error['description']
        }), e.status_code

    return app
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='127.0.0.1', port=port, debug=True)
