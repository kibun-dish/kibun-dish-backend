import os
from unicodedata import category
from weakref import ref 
from xml.etree.ElementPath import prepare_parent
from flask import Flask, render_template, jsonify
from flask import request, redirect, url_for

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


@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html') 

db.init(app)
if __name__ == '__main__':
    app.run()