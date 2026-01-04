from flask import Flask,request, make_response,jsonify
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

def update_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404

    try:
        power.description = request.json.get("description")
        db.session.commit()
        return power.to_dict(), 200
    except Exception as e:
        return {"errors": [str(e)]}, 400


@app.post("/hero_powers")
def create_hero_power():
    try:
        hero_power = HeroPower(
            strength=request.json["strength"],
            hero_id=request.json["hero_id"],
            power_id=request.json["power_id"]
        )

        db.session.add(hero_power)
        db.session.commit()

        return hero_power.to_dict(), 201

    except Exception as e:
        return {"errors": [str(e)]}, 400