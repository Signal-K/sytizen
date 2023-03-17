from flask import Flask, request, make_response, jsonify, Blueprint, send_file
from flask_cors import CORS, cross_origin
from supabase_py import client, create_client
 
import base64
from io import BytesIO

from .datastore import supabase, find_all_planets, add_planet_to_DB, planets
# from Generator import gen_image # add this to a blueprint

from .classify import classify

from .main import gen_image

# Flask application/container initialisation
app = Flask(__name__)

# Flask blueprints
app.register_blueprint(classify, url_prefix='/classify')
CORS(app)

if __name__ == '__main__':
    for seed in range(0, 10):
        gen_image(seed)
    app.run(debug = True)

@app.route('/get_image')
def get_image():
    #for seed in range(0, 10):
       #gen_image(seed)
    return send_file('out0.png', mimetype='image/png')