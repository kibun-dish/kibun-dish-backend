from operator import methodcaller
import os
from unicodedata import category
from weakref import ref 
from xml.etree.ElementPath import prepare_parent
from flask import Flask, render_template, jsonify
from flask import request, redirect, url_for
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import column
from flask_cors import CORS
import datetime

app = Flask(__name__) # ここのtemplate_folder, static_folderを追記

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///schedule_matching.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECREAT_KEY"] = os.urandom(24)

db = SQLAlchemy(app)

CORS(app)

# @app.route('/', defaults={'path':''},method=["GET"])
# def index():
#     return json.dumps()

@app.route('/foods', defaults={'path':''},method=["GET"])
def show_foods():
    return json.dumps()

@app.route('/feels', defaults={'path':''},method=["GET"])
def show_feels():
    return json.dumps()

@app.route('/relations', defaults={'path':''},method=["GET"])
def show_relations():
    return json.dumps()

@app.route('/create/relations', defaults={'path':''},method=["POST"])
def show_relations():
    # create feels and foods
    return "200"

# @app.route('/<path:path>')
# def index(path):
#     return render_template('index.html') 

db.init(app)
if __name__ == '__main__':
    app.run()