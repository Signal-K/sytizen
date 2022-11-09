import os
#from dotenv import load_dotenv
from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource, reqparse

# Data patterns
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db' # location of the database -> see `database.db` in root directory (inside `./api` in signal-k/polygon)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app) # Wrap the db around flask
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)

    return app

"""@app.route('/')
def index():
    return jsonify({
        'message': 'Hello World!'
    })

@app.route('/add-user', methods=["POST"], strict_slashes=False)
def add_user():
    email = request.json['email']
    address = request.json['address']
    profileId = request.json['profileId']

    user = User"""