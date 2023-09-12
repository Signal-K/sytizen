from flask import Flask, jsonify, request, g
import requests

app = Flask(__name__)

# Store authentication details in a global variable 'auth'
auth = None

@app.route("/")
def index():
    return "Hello world"

@app.route('/login', methods=['POST'])
def login():
    global auth  # Use the global 'auth' variable to store authentication details

    # Parse the JSON request data
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

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
        # Store authentication details in the 'auth' variable
        auth = (username, password)
        return jsonify(token_response)
    else:
        return jsonify({'error': 'Login failed'}), 401

@app.route('/get_geolocation', methods=['POST'])
def get_geolocation():
    global auth  # Use the global 'auth' variable for authentication

    # Check if authentication details are available
    if not auth:
        return jsonify({'error': 'Authentication required'}), 401

    # Parse the JSON request data
    data = request.get_json()
    address = data.get('address')

    # Check if address is provided
    if not address:
        return jsonify({'error': 'Address is required'}), 400

    # Send a POST request to fetch geolocation using stored authentication
    response = requests.get(
        f'https://geocode.maps.co/search?q={address}',
        auth=auth
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        geoloc_data = response.json()
        return jsonify(geoloc_data)
    else:
        return jsonify({'error': 'Geolocation fetch failed'}), 500

if __name__ == "__main__":
    app.run()