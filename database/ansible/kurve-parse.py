from flask import Flask, jsonify, request
import requests
import psycopg2
import lightkurve as lk
import matplotlib.pyplot as plt
from thirdweb import ThirdwebSDK

# Flask Initialisation
app = Flask(__name__)

# Lightcurve initialisation 
planetTic = ""

# Contract Initialisation
sdk = ThirdwebSDK("mumbai")
contract = sdk.get_contract("0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9")
_receiver = ""
_tokenId = 0
_quantity = 0
data = contract.call("claim", 0xCdc5929e1158F7f0B320e3B942528E6998D8b25c, 2, 1)

# Flask/api routes
@app.route('/planet')
def planet():
    return jsonify({'planet' : 'planet'})

@app.post('/select_planet')
def select_planet():
    data = request.get_json()
    planetId = data['planetId']
    planetName = data['planetName']
    planetTic = data['planetTic']
    sector_data = lk.search_lightcurve(planetTic, author = 'SPOC', sector = 23)
    #lc = sector_data.download()
    #lc.plot()
    return sector_data

# Show planet data on frontend
@app.post('/show_planet') # Can we do some calculation for nft revealing using this (i.e. mint nft after classification)
def show_tic():
    lc = sector_data.plot()
    return lc

@app.post('/mint-planet')
def mint_planet():
    data = request.get_json()
    _receiver = data['profileAddress']
    _tokenId = data['tokenId']
    _quantity = 1
    data = contract.call("claim", _receiver, _tokenId, _quantity)

app.run(host='0.0.0.0', port=8080)

import lightkurve as lk
import random
import string
from supabase import create_client

# Connect to Supabase
supabase_url = 'https://<your-project>.supabase.co'
supabase_key = '<your-anon-key>'
client = create_client(supabase_url, supabase_key)

# Define a function to generate random TIC ids
def generate_tic_id():
    letters = string.ascii_uppercase
    digits = string.digits
    random_letters = ''.join(random.choice(letters) for i in range(3))
    random_digits = ''.join(random.choice(digits) for i in range(4))
    return f'KOI-{random_letters}{random_digits}'

# Define a function to upload data to Supabase
def upload_to_supabase(name, image_link, radius, period):
    data = {
        'name': name,
        'image': image_link,
        'radius': radius,
        'period': period
    }
    response = client.table('lightcurves').insert(data).execute()
    if response['status'] == 201:
        print(f'Successfully uploaded {name} to Supabase!')
    else:
        print(f'Failed to upload {name} to Supabase.')

# Generate 5 random TIC ids and create Lightcurve objects
for i in range(5):
    tic_id = generate_tic_id()
    print(f'Generating Lightcurve for TIC ID: {tic_id}')
    lc = lk.search_lightcurve(tic_id).download_all()

    # Save the Lightcurve plot to a file and get the link
    fig = lc[0].plot()
    image_file = f'{tic_id}.png'
    fig.savefig(image_file)
    image_link = client.storage.from_file(image_file, f'lightcurves/{image_file}').public_url()

    # Get the name, radius, and orbital period
    name = lc[0].target_name
    radius = lc[0].header['RADIUS']
    period = lc[0].header['TPERIOD']

    # Upload the data to Supabase
    upload_to_supabase(name, image_link, radius, period)
