from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    from .views import main
    from . import models

    with app.app_context():
        db.create_all()

    app.register_blueprint(main)

    return app