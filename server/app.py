from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.get("/heroes")
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([
        hero.to_dict(only=("id", "name", "super_name"))
        for hero in heroes
    ])

@app.get("/heroes/<int:id>")
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return {"error": "Hero not found"}, 404

    return hero.to_dict(), 200

@app.get("/powers")
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.get("/powers/<int:id>")
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404
    return power.to_dict(), 200




    