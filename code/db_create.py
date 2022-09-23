from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
import datetime
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///schedule_matching.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECREAT_KEY"] = os.urandom(24)

db = SQLAlchemy(app)

class Food(db.Model):
    __tablename__ = 'Food'
    id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), null=False, unique=True)

class Fell(db.Model):
    __tablename__ = 'Feel'
    id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), null=False, unique=True)


class Relation(db.Model):
    __tablename__ = 'Relation'
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer) # Foreign key
    feel_id = db.Column(db.Integer) # Foreign key
    user_id = db.Column(db.Integer) # Foreign key
    evaluation = db.Column(db.Integer)
    created_at = db.Column(db.DATE)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), null=False, unique=True)

db.init_app(app)
db.create_all()