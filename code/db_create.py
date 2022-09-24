from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{username}:{}@localhost:5432/kibun_dish"
database_uri = os.environ.get('DATABASE_URL')
if database_uri and database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kibun-dish.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECREAT_KEY"] = os.urandom(24)

db = SQLAlchemy(app)

class Food(db.Model):
    __tablename__ = 'food'
    id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

class Feel(db.Model):
    __tablename__ = 'feel'
    id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

class Relation(db.Model):
    __tablename__ = 'relation'
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer) # Foreign key
    feel_id = db.Column(db.Integer) # Foreign key
    user_id = db.Column(db.Integer) # Foreign key
    evaluation = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DATE, default=datetime.date.today())

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

db.init_app(app)
db.create_all()