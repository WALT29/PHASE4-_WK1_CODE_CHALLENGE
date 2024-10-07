#!/usr/bin/env python3

from flask import Flask, request, make_response,jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


@app.route('/heroes')
def heroes():
    heroes=[]
    for hero in Hero.query.all():
        hero_dict={
            "id":hero.id,
            "name":hero.name,
            "super_name":hero.super_name
        }
        heroes.append(hero_dict)
    
    return make_response(jsonify(heroes),200)

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    hero=Hero.query.filter(Hero.id==id).first()
    
    if hero:
        body=hero.to_dict();
        response=200
    else:
        body={
            "error":"Hero not found"
        }
        response=404
    
    return make_response(body,response)

@app.route('/powers')
def powers():
    powers=[]
    for power in Power.query.all():
        power_dict={
            'description': power.description,
            'id':power.id,
            'name':power.name        
        }
        powers.append(power_dict)
    
    return make_response(jsonify(powers),200)

@app.route('/powers/<int:id>',methods=['GET', 'PATCH'])
def powers_by_id(id):
    power=Power.query.filter(Power.id==id).first()
    if not power :
        body={
            'error':"Power not found"
        }
        return make_response(body,404)
        
    
    if request.method =='GET':
        body={
            'description':power.description,
            'id':power.id,
            'name':power.name
        }
        return make_response(body,200)
    elif request.method == 'PATCH':
        data=request.json
        description = data.get('description')
    
        if len(description)<20:
            return {'errors':['validation errors']},400
        for key, value in data.items():
            setattr(power, key, value)
        
        db.session.commit()
        return make_response(jsonify(power.to_dict()), 200)


@app.route('/hero_powers', methods=['GET', 'POST'])
def hero_powers():
    if request.method == 'GET':
        hero_powers=[]
        for hero_power in HeroPower.query.all():
            hero_powers.append(hero_power.to_dict())
        
        return make_response(hero_powers, 200)

    elif request.method == 'POST':
        strength = request.json.get('strength')
        power_id = request.json.get('power_id')
        hero_id = request.json.get('hero_id')

        
        strengths = ['Strong', 'Weak', 'Average']
        if strength not in strengths:
            return {"errors": ["validation errors"]}, 400
    
        new_power = HeroPower(
            strength=strength,
            power_id=power_id,
            hero_id=hero_id
        )

        db.session.add(new_power)
        db.session.commit()
        return make_response(new_power.to_dict(), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
