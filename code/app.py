from dataclasses import dataclass
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
from db_create import User, Food, Feel, Relation
from db_create import db

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

# show
@app.route('/food', method=["GET"])
def show_foods():
    all_food = db.session.query(Food).all()
    send_data = []
    for now in all_food:
        current_input = {'id':now.id, 'name':now.name}
        send_data.append(current_input)
    return jsonify(send_data)

@app.route('/feel', defaults={'path':''},method=["GET"])
def show_feels():
    all_feel = db.session.query(Feel).all()
    send_data = []
    for now in all_feel:
        current_input = {'id':now.id, 'name':now.name}
        send_data.append(current_input)
    return jsonify(send_data)

@app.route('/relation', method=["GET"])
def show_relations():
    all_relation = db.session.query(Relation).all()
    send_data = []
    for now in all_relation:
        food_name = db.session.query(Food).filter(Food.id == now.food_id).first().name
        feel_name = db.session.query(Feel).filter(Feel.id == now.feel_id).first().name
        current_data = {
            'id':now.id,
            'evaluation':now.evaluation,
            'food':{'id':now.food_id, 'name':food_name},
            'feel':{'id':now.feel_id, 'name':feel_name},
        }
        send_data.append(current_data)
    return jsonify(send_data)

# register
@app.route('/relation', method=["POST"])
def register_relation():
    # create feels and foods
    post_data = request.get_json()
    print(post_data)
    food_id = Food.query.filter(Food.name == post_data['food_name']).get(id)
    feel_id = Feel.query.filter(Feel.name == post_data['feel_name']).get(id)
    today   = datetime.datetime().today()
    new_relation = Relation(user_id=1, food_id=food_id, feel_id=feel_id, evaluation=post_data['evaluation'], created_at=today)
    db.add(new_relation)
    db.commit()
    return jsonify({})

@app.route('/food', method=["POST"])
def register_food():
    post_data = request.get_json()
    food = Food(name=post_data['food_name'])
    db.session.add(food)
    db.session.commit()
    return jsonify({})

@app.route('/feel', method=["POST"])
def register_feel():
    post_data = request.get_json()
    feel = Feel(name=post_data['feel_name'])
    db.session.add(feel)
    db.session.commit()
    return jsonify({})

# @app.route('/<path:path>')
# def index(path):
#     return render_template('index.html') 

db.init(app)
if __name__ == '__main__':
    app.run()