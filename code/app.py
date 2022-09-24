import os
from flask import Flask, jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
from sqlalchemy.exc import IntegrityError
from db_create import User, Food, Feel, Relation
from db_create import db
import traceback

app = Flask(__name__) # ここのtemplate_folder, static_folderを追記

app.config['JSON_AS_ASCII'] = False
database_uri = os.environ.get('DATABASE_URL')
if database_uri and database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/kibun_dish"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECREAT_KEY"] = os.urandom(24)

db = SQLAlchemy(app)

CORS(app)

# @app.route('/', defaults={'path':''},method=["GET"])
# def index():
#     return json.dumps()

@app.route('/food', methods=["GET","POST"])
def show_foods():
    if request.method == "GET":
        all_food = db.session.query(Food).all()
        send_data = []
        for now in all_food:
            current_input = {'id':now.id, 'name':now.name.decode('unicode-escape')}
            send_data.append(current_input)
        return jsonify(send_data)
    elif request.method == "POST":
        post_data = request.get_json()
        try:
            post_name = post_data['name'].encode('unicode-escape')
            new_food  = Food(name = post_name)
            db.session.add(new_food)
            db.session.commit()   
            print("saved food") 
        except IntegrityError as e:
            print(traceback.format_exc())
            db.session.rollback()
        posted = {
            "id":new_food.id,
            "name":post_data['name'], 
        }    
        return jsonify([posted])

@app.route('/feel',methods=["GET","POST"])
def show_feels():
    if request.method == "GET":
        all_feel = db.session.query(Feel).all()
        send_data = []
        for now in all_feel:
            current_input = {'id':now.id, 'name':now.name.decode('unicode-escape')}
            send_data.append(current_input)
        return jsonify(send_data)
    elif request.method == "POST":
        post_data = request.get_json()
        try:
            post_name = post_data['name'].encode('unicode-escape')
            new_feel  = Feel(name = post_name)
            db.session.add(new_feel)
            db.session.commit()   
            print("saved feel") 
        except IntegrityError as e:
            print(traceback.format_exc())
            db.session.rollback()
        posted = {
            "id":new_feel.id,
            "name":post_data['name'], 
        }    
        return jsonify([posted])


@app.route('/relation',methods=["GET","POST"])
def show_relations():
    if request.method == "GET":
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
    elif request.method == "POST":
        post_data = request.get_json()
        print(post_data)
        try:
            food_id  = int(post_data['food_id'])
            feel_id  = int(post_data['feel_id'])
            evaluation  = int(post_data['evaluation'])
            today = datetime.date.today()
            new_relation = Relation(user_id=1, food_id=food_id, feel_id=feel_id, evaluation=evaluation, created_at=today)
            db.session.add(new_relation)
            db.session.commit()
            print("saved relation")
        except IntegrityError as e:
            db.session.rollback()
        posted = {
            "user_id":new_relation.user_id,
            "food_id":new_relation.food_id,
            "feel_id":new_relation.feel_id,
            "evaluation":new_relation.evaluation, 
        }    
        return jsonify([posted])
    
# @app.route('/<path:path>')
# def index(path):
#     return render_template('index.html') 

db.init_app(app)
if __name__ == '__main__':
    app.run()