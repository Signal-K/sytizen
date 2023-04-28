from flask import Flask, jsonify, request, Blueprint
from supabase import create_client
import lightkurve as lk
import os
import uuid

# For supabase user authentication
from datetime import datetime, timedelta
from gotrue.exceptions import APIError

app = Flask(__name__)

# Create a Supabase client instance
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase_client = create_client(supabase_url, supabase_key)

# Initial/empty blueprint, route
@app.route('/')
def index():
    for seed in range(0, 10):
        gen_image(seed)
    return "Hello, this is the index"

# Authentication blueprint
auth_bp = Blueprint('auth', __name__)
email: tr = ''
password: str = ''
# user = supabase.auth.sign_up(email = email, password = password)

# Authentication method -> move this into a flask route/function
session = None
try:
    session = supabase.auth.sign_in( email = email, password = password )
    supabase.postgres.auth(session.access_token)
except APIError:
    print("Authentication failed due to API Error")

resp = supabase.storage().from_('images').get_public_url('cebdc7a2-d8af-45b3-b37f-80f328ff54d6/69893963-c755-4a46-802b-b729c5482cd5')
print(resp)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Authentication logic here
    return jsonify({'message': 'Logged in successfully!'})


# Retrieve data from Supabase blueprint
retrieve_bp = Blueprint('retrieve', __name__)

@retrieve_bp.route('/planets', methods=['GET'])
def get_planets():
    # Retrieve data from Supabase table
    planets = []
    return jsonify(planets)


# Post data to Supabase blueprint
post_bp = Blueprint('post', __name__)

@post_bp.route('/planets', methods=['POST'])
def create_planet():
    # Post data to Supabase table
    return jsonify({'message': 'Planet created successfully!'})


# Generate lightcurves blueprint
generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/lightcurves', methods=['POST'])
def generate_lightcurves():
    # Get TIC IDs from request
    data = request.json
    tic_ids = data['tic_ids']
    
    # Generate lightcurves and post to Supabase table
    for tic_id in tic_ids:
        # Generate lightcurve
        lc = lk.search_lightcurvefile(tic_id).download().PDCSAP_FLUX.normalize().remove_nans().flatten(window_length=101).fold(period=1.1235).bin(10)
        fig = lc.plot()
        fig.savefig(f'output/{tic_id}.png')
        
        # Upload image to Supabase storage
        bucket = 'planets'
        planet_id = str(uuid.uuid4())
        folder_id = supabase_client.storage.create_folder(bucket, {'name': planet_id + '/'}).data.id
        file_name = 'download.png'
        file_path = f'output/{tic_id}.png'
        supabase_client.storage.from_file(bucket, planet_id + '/' + file_name, file_path)
        
        # Post data to Supabase table
        planet_data = {
            'planetId': planet_id,
            'image': f'https://storage.supabase.io/{bucket}/t/{folder_id}/f/{file_name}',
            'name': tic_id,
            'radius': 0.0,  # Placeholder value for now
            'orbital_period': 0.0  # Placeholder value for now
        }
        supabase_client.table('planets').insert(planet_data).execute()
    
    return jsonify({'message': 'Lightcurves generated and uploaded successfully!'})


# Register blueprints with the app
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(retrieve_bp, url_prefix='/retrieve')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(generate_bp, url_prefix='/generate')

if __name__ == '__main__':
    for seed in range(0, 10):
        gen_image(seed)
    app.run(debug = True)