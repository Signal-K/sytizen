from flask import Flask, Blueprint, jsonify
from .app import app
from .models import Planet

# views.py
main = Blueprint('main', __name__)

@main.route('/add_planet', methods=['POST'])
def add_planet():
    return 'Done', 201

@main.route('/planets', methods=['GET']) # Retrieve these from Supabase
def get_planets():
    planets = []
    return jsonify({ 'planets' : planets })

# Retrieve a single planet
@app.route('/planetss/<id>', methods=['GET'])
def get_planet(id):
  planet = Planet.query.get(id)
  del planet.__dict__['_sa_instance_state']
  return jsonify(planet.__dict__)

# Retrieve all the planets
@app.route('/planetss', methods=['GET'])
def get_planetss():
  planets = []
  for planet in db.session.query(Planet).all():
    del planet.__dict__['_sa_instance_state']
    planets.append(planet.__dict__)
  return jsonify(planets)

# Create a new planet
@app.route('/planets', methods=['POST'])
def create_item():
  body = request.get_json()
  db.session.add(Planet(body['name'], body['moons']))
  db.session.commit()
  return "item created"