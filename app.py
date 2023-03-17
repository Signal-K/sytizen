from flask import Flask, request, make_response, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from supabase_py import client, create_client
 
import base64
from io import BytesIO

from .datastore import supabase, find_all_planets, add_planet_to_DB
# from Generator import gen_image # add this to a blueprint

from views import main

# Flask application/container initialisation
app = Flask(__name__)

# Flask blueprints
app.register_blueprint(main, url_prefix='/classify')
CORS(app)

if __name__ == '__main__':
    app.run(debug = True)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hello world'