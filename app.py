from flask import Flask, render_template, Blueprint, jsonify
import lightkurve as lk
import os
# from supabase import create_client

"""# Flask blueprints ""
from database.classify import classify
from views.lightkurve import lightkurve_bp"""

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world"

@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the request data
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Send a POST request to the NASA Earthdata login API
    response = requests.post(
        'https://appeears.earthdatacloud.nasa.gov/api/login',
        auth=(username, password)
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        token_response = response.json()
        return jsonify(token_response)
    else:
        return jsonify({'error': 'Login failed'}), 401

if __name__ == "__main__":
    app.run()