from flask import Flask, render_template, Blueprint, jsonify
import lightkurve as lk
import os
from supabase import create_client
# from supabase.errors import ClientError

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world"

lightkurve_bp = Blueprint("lightkurve_bp", __name__)

def generate_lightcurve(tic_id):
    # Download data and create a light curve
    lc = lk.search_lightcurvefile(tic_id).download_all().stitch()
    pg = lc.to_periodogram(oversample_factor=10)

    # Fold the light curve and create a phase-folded light curve
    period = pg.period_at_max_power.value
    phase = lc.fold(period=period).phase
    flux = lc.fold(period=period).flux

    # Plot the phase-folded light curve and save it to a file
    fig = lk.LightCurve(phase, flux).plot()
    fig.savefig(f"output/{tic_id}.jpg")

    # Estimate the radius, temperature, and orbital period of the planet candidate
    radius = pg.estimate_radius().value
    temperature = pg.estimate_temperature().value
    orbital_period = period

    # Insert the data into the supabase table
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_KEY"]
    client = create_client(supabase_url, supabase_key)
    content = {"id": tic_id, "radius": radius, "temperature": temperature, "orbital_period": orbital_period, "content": tic_id}
    try:
        client.from_table("lightcurve_stats").insert(content).execute()
    except:# ClientError as e:
        print('error') #(e)

@lightkurve_bp.route("/generate_lightcurve_all")
def generate_lightcurve_all():
    tics = ["KOI-456", "KOI-3456", "KOI-5737", "KOI-5806", "KOI-5499", "KOI-2194", "KOI-6108", "KOI-5938", "KOI-5087", "KOI-5948", "KOI-5176", "KOI-5949", "KOI-5506", "KOI-6239", "KOI-5888", "KOI-5068", "KOI-5541", "KOI-5959", "KOI-5236", "KOI-5819", "KOI-5413", "KOI-5202", "KOI-1871", "KOI-5653", "KOI-5237", "KOI-6151", "KOI-5545"]
    for tic in tics:
        generate_lightcurve(tic)
    return jsonify({"message": "Generated light curves for all TIC IDs"})

@lightkurve_bp.route("/generate_lightcurve_koi456")
def generate_lightcurve_koi456():
    generate_lightcurve("KOI-456")
    return jsonify({"message": "Generated light curve for KOI-456"})

    lc = lk.search_lightcurvefile('KOI-456').download_all().stitch()
    pg = lc.to_periodogram(oversample_factor=10)

    # Fold the light curve and create a phase-folded light curve
    period = pg.period_at_max_power.value
    phase = lc.fold(period=period).phase
    flux = lc.fold(period=period).flux

    # Plot the phase-folded light curve and save it to a file
    fig = lk.LightCurve(phase, flux).plot()
    fig.savefig(f"output/{tic_id}.jpg")

    # Estimate the radius, temperature, and orbital period of the planet candidate
    radius = pg.estimate_radius().value
    temperature = pg.estimate_temperature().value
    orbital_period = period

app.register_blueprint(lightkurve_bp)

if __name__ == "__main__":
    app.run()

"""from flask import Flask, jsonify, request, Blueprint
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
    app.run(debug = True)"""