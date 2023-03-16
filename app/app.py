from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Planet(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), unique=True, nullable=False)
  content = db.Column(db.String(120), unique=True, nullable=False)

  def __init__(self, title, content):
    self.title = title
    self.content = content

db.create_all()

# Get a specific planet
@app.route('/planets/<id>', methods=['GET'])
def get_planet(id):
  planet = Planet.query.get(id)
  del planet.__dict__['_sa_instance_state']
  return jsonify(planet.__dict__)

# Get & return all planets
@app.route('/planets', methods=['GET'])
def get_planets():
  planets = []
  for planet in db.session.query(Planet).all():
    del planet.__dict__['_sa_instance_state']
    planets.append(planet.__dict__)
  return jsonify(planets)

# Create a planet
@app.route('/planets', methods=['POST'])
def create_planet():
  body = request.get_json()
  db.session.add(Planet(body['title'], body['content']))
  db.session.commit()
  return "planet created"

# Update a specific planet
@app.route('/planets/<id>', methods=['PUT'])
def update_planet(id):
  body = request.get_json()
  db.session.query(Planet).filter_by(id=id).update(
    dict(title=body['title'], content=body['content']))
  db.session.commit()
  return "planet updated"

# Delete a specific planet
@app.route('/planets/<id>', methods=['DELETE'])
def delete_planet(id):
  db.session.query(Planet).filter_by(id=id).delete()
  db.session.commit()
  return "planet deleted"