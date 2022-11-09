from flask import Blueprint, jsonify
from . import db

main = Blueprint('main', __name__)

@main.route('/add_user', methods=["POST"])
def add_user():
    return 'Done', 201

@main.route('/users')
def users():
    users = []
    return jsonify({'users': users})