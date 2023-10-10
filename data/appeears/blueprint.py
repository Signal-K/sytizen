from flask import Flask, request, render_template, jsonify
import requests
import random
import json

app = Flask(__name__)

# Auth setup (non-Supabase, for NASA-EDC)
username = 'mcdepth'
pswd = 'VgZ#MNYz5&Fv$@TPF!q*kJCeKw' # getpass.getpass('Password: ')

def fetch_geolocation(address):
    response = requests.get(f'https://geocode.maps.co/search?q={address}')
    geoloc_data = response.json()
    return geoloc_data

def fetch_nasa_data():
    response = requests.get('https://appeears.earthdatacloud.nasa.gov/api/product')
    product_response = response.json()
    return product_response

@app.route('/', methods=['GET'])
def index():
    return "Hello, World"

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

@app.route('/locationTest', methods=['GET', 'POST'])
def locationTest():
    if request.method == 'POST':
        address = request.form['address']
        geolocation = fetch_geolocation(address)
        
        nasa_data = fetch_nasa_data()
        random_product = random.choice(nasa_data)
        
        output = {
            'address': address,
            'geolocation': geolocation,
            'nasa_data': random_product,
        }
        
        return render_template('output.html', data=output)
    
    return render_template('input.html')

if __name__ == '__main__':
    app.run()