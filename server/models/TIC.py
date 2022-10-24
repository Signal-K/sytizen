from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort
from server.main import app#, db
import lightkurve as lk

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # location of the database -> see `database.db` in root directory (inside `./api` in signal-k/polygon)
db = SQLAlchemy(app) # Wrap the database around the flask app

# Gathered from notebook -> export notebook to py and add matplotlib graphs as endpoints?
class TicModel(db.Models):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)

tics = {}

# Lightkurve CLI
def get_sector_data(tic_id):
    pass

# Create a model for movement/player location on a planet (include planet ID as foreign key in this table)