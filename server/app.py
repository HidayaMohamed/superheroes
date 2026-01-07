# Imports
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

# Create the Flask application instance
app = Flask(__name__)
# Configure the SQLite database location
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# Disable SQLAlchemy event notification
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Disable JSON response compacting 
app.json.compact = False

# Initialize Flask-Migrate with app and database
migrate = Migrate(app, db)
# Attach SQLAlchemy instance to the Flask app
db.init_app(app)

# App index route with a message on how to get to the  API endpoints
@app.route('/')
def index():
    return {
        "message": "Welcome to the Superheroes API",
        "available_routes": {
            "GET /heroes": "Get a list of all heroes",
            "GET /heroes/<id>": "Get a single hero and their powers",
            "GET /powers": "Get a list of all powers",
            "GET /powers/<id>": "Get a single power",
            "PATCH /powers/<id>": "Update a power description",
            "POST /hero_powers": "Assign a power to a hero"
        }
    }, 200

## GET /heroes
@app.get("/heroes")
def get_heroes():
    # Query all Hero records from the database
    heroes = Hero.query.all()
    # Return a list of heroes with 3(id, name, super_name) fields
    return jsonify([
        hero.to_dict(only=("id", "name", "super_name"))
        for hero in heroes
    ])

# GET /heroes/:id -> gets heroes by their id.
@app.get("/heroes/<int:id>")
def get_hero(id):
    # Find hero by primary key
    hero = Hero.query.get(id)
    # If hero does not exist, return error
    if not hero:
        return {"error": "Hero not found"}, 404

     # Return hero data including hero_powers
    return hero.to_dict(), 200

# GET /powers
@app.get("/powers")
def get_powers():
    # Query all Power records
    powers = Power.query.all()
    # Return all powers as JSON
    return jsonify([power.to_dict() for power in powers])


# GET /powers/:id -> Gets powers by their id
@app.get("/powers/<int:id>")
def get_power(id):
    # Find power by ID
    power = Power.query.get(id)
    # If power not found, return error
    if not power:
        return {"error": "Power not found"}, 404
    # Return power data
    return power.to_dict(), 200

# PATCH /powers/:id -> Updates power using their id
@app.patch("/powers/<int:id>")
def update_power(id):
     # Find power by ID
    power = Power.query.get(id)
    # If power does not exist, return error
    if not power:
        return {"error": "Power not found"}, 404

    # Update the description field from request body
    try:
        power.description = request.json.get("description")
        # Commit changes to the database
        db.session.commit()
        # Return updated power
        return power.to_dict(), 200
    except Exception as e:
        # Catch validation or database errors
        return {"errors": [str(e)]}, 400

# POST /hero_powers
@app.post("/hero_powers")
def create_hero_power():

    try:
        # Create a new HeroPower instance
        hero_power = HeroPower(
            strength=request.json["strength"],
            hero_id=request.json["hero_id"],
            power_id=request.json["power_id"]
        )
        # Add to database session
        db.session.add(hero_power)
        # Commit to persist the record
        db.session.commit()

        # Return newly created hero_power with related hero and power
        return hero_power.to_dict(), 201

    except Exception as e:
        # Catch validation or foreign key errors
        return {"errors": [str(e)]}, 400