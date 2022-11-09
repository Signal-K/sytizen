from flask import Blueprint, jsonify, request
from main import db
from models import User

main = Blueprint('main', __name__)

@main.route('/add_user', methods=["POST"])
def add_user():
    user_data = request.get_json()
    new_user = User(email=user_data['email'], userid=user_data['userid'])

    db.session.add(new_user)
    db.session.commit()
    return 'Added new user', 201

@main.route('/users')
def users():
    user_list = User.query.all() # This is queried from the db -> how do we get this to also query from Supa?
    users = []

    for user in user_list:
        users.append({'email' : user.email, 'userid' : user.userid})

    return jsonify({'users' : users})