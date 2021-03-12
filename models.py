import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = "casting_agency_3"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
# database_path = "postgres://{}:{}@{}/{}".format('postgres', 'xxxx', 'localhost:5432', database_name)
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable
    to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    release_date = Column(db.DateTime)

    scenes_movie = db.relationship('Scene', backref='movies')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def details(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)

    scenes_actor = db.relationship('Scene', backref='actors')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Scene(db.Model):
    __tablename__ = 'scenes'

    movie_id = Column(Integer, db.ForeignKey(
        'movies.id'), primary_key=True)
    actor_id = Column(Integer, db.ForeignKey(
        'actors.id'), primary_key=True)
    start_time= Column(db.DateTime)
