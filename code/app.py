from asyncio.windows_events import NULL
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
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from db_create import User, Food, Feel, Relation
from db_create import db
import traceback

app = Flask(__name__) # ここのtemplate_folder, static_folderを追記

app.config['JSON_AS_ASCII'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/kibun_dish"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///schedule_matching.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECREAT_KEY"] = os.urandom(24)

db = SQLAlchemy(app)

CORS(app)

# @app.route('/', defaults={'path':''},method=["GET"])
# def index():
#     return json.dumps()

@app.route('/', methods=["GET"])
def index():
    return "hello"

@app.route('/food', methods=["GET"])
def show_foods():
    all_food = db.session.query(Food).all()
    send_data = []
    for now in all_food:
        current_input = {'id':now.id, 'name':now.name}
        send_data.append(current_input)
    return jsonify(send_data)

@app.route('/feel',methods=["GET"])
def show_feels():
    all_feel = db.session.query(Feel).all()
    send_data = []
    for now in all_feel:
        current_input = {'id':now.id, 'name':now.name}
        send_data.append(current_input)
    return jsonify(send_data)

@app.route('/relation',methods=["GET"])
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

@app.route('/create/relation',methods=["POST"])
def register_relations():
    # create feels and foods
    post_data = request.get_json()
    print(post_data)
    try:
        new_food  = Food(name = post_data['food_name'])
        db.session.add(new_food)
        db.session.commit()   
        print("saved food")    
    except IntegrityError as e:
        db.session.rollback()
        print(traceback.format_exc())
        
    try:
        new_feel  = Feel(name = post_data['feel_name'])
        db.session.add(new_feel)
        db.session.commit()
        print("saved feel")
    except IntegrityError as e:
        db.session.rollback()
        print(traceback.format_exc())
         
    food = Food.query.filter(Food.name == post_data['food_name']).first()
    feel = Feel.query.filter(Feel.name == post_data['feel_name']).first()
    if food is not None and feel is not None:
        today   = datetime.date.today()
        new_relation = Relation(user_id=1, food_id=food.id, feel_id=feel.id, evaluation=int(post_data['evaluation']), created_at=today)
        try:
            db.session.add(new_relation)
            db.session.commit()
            print("saved relation")
        except IntegrityError as e:
            db.session.rollback()
            print(traceback.format_exc())
        return jsonify([
            {
                'id':new_relation.id,
                'food_id': new_relation.food_id,
                'feel_id': new_relation.feel_id,
                'evaluation':new_relation.evaluation,
            }
            ])
    return jsonify([{"Error": "Did you confirm own request?"}])


# @app.route('/<path:path>')
# def index(path):
#     return render_template('index.html') 

db.init_app(app)
if __name__ == '__main__':
    app.run()