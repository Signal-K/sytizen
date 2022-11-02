from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin
import time

import click

#from models.planets import planets
from data.store import planets, add_planet_to_DB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # location of the database -> see `database.db` in root directory (inside `./api` in signal-k/polygon)
db = SQLAlchemy(app) # Wrap the database around the flask app
CORS(app)

# CLI Main
@click.group()
def main():
    pass

@click.command()
def web():
    from .wsgi import app
    app.run()

# Begin flask routes
@app.route('/')
def hello_world():
    return jsonify({
        'greeting': 'Hello World!'
    })

# Test GET request -> display time (Then retrieved by React)
@app.route('/time')
def get_current_time():
    return {'time': time.time()} # If this remains in any format, consider changing to block time

# GET request -> return all planets in storage/db in JSON format
@app.route('/planets')
def get_planets():
    return jsonify({
        'planets': planets, # Then present this on react frontend, port 5000 -> 3000
    })

@app.route('/planets/<planet_id>')
def find_planet_by_id(planet_id):
    for planet in planets:
        if planet["id"] == int(planet_id):
            return jsonify({
                "planet": planet,
            })

@app.route('/planets/add', methods=['POST'])
def add_planet():
    data = request.get_json()
    try:
        title = data['title']
        if title:
            data = add_planet_to_DB(title)
            return jsonify(data), 201
    except:
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)