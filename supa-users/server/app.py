import os
from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from data.users import users
from supabase import create_client, Client

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

url = "https://afwwxlhknelxylrfvexi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmd3d4bGhrbmVseHlscmZ2ZXhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjY0MzQ4MTgsImV4cCI6MTk4MjAxMDgxOH0.gk1F8Br9__04cvzqYIeeQ-U08KATiHovAw3r3ofNGAo"
supabase: Client = create_client(url, key)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<User {self.email}>'

def find_all_planets():
    data = supabase.table("Planets").select("*").execute()
    return data['data']

Planets = find_all_planets()
print(Planets)

@app.route('/')
def index():
    return "Hello World"

@app.route('/users')
def all_users():
    return jsonify({
        'users': users,
    })

@app.route('/users/<user_id>')
def find_user_by_id(user_id):
    for user in users:
        if user["id"] == int(user_id):
            return jsonify({
                "user": user,
            })

@app.route('/add_user', methods=['POST'])
def add_user():
    user_data = request.get_json()
    new_user = User(title=user_data['title'])

    db.session.add(new_user)
    db.session.commit()
    return 'Done', 201

"""@app.route('/users')
def users():
    user_list = User.query.all()
    users = []
    
    for user in user_list:
        users.append({'email' : user.email})

    return jsonify({'users' : users})

@app.route('/add_user', methods=['POST'])
def add_user():
    user_data = request.get_json()
    new_user = User(email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()

    return 'Done', 201"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', Debug = True)