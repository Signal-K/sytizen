from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from supabase_py import client, create_client
import os

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")

url = "https://afwwxlhknelxylrfvexi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmd3d4bGhrbmVseHlscmZ2ZXhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjY0MzQ4MTgsImV4cCI6MTk4MjAxMDgxOH0.gk1F8Br9__04cvzqYIeeQ-U08KATiHovAw3r3ofNGAo"

supabase: client = create_client(url, key)

# Function to retrieve planet data from supa
def find_all_planets(): # Right now this is just demo data, we'll push this data to Supa from Lightkurve later
    data = supabase.table("Planetss").select("*").execute()
    return data['data']

planets = find_all_planets()
print(planets)

# Function to add a new planet to the store/supa
def add_planet_to_DB(title, ticId) -> dict: # See `models/TIC.py`
    planet = {
        "title": title,
        "ticId": ticId,
    }
    data = supabase.table("Planetss").insert(planet).execute()
    planets = find_all_planets()

    return data['data']

# GET request -> return all planets in storage/db in JSON format
@app.route('/planets')
def get_planets():
    planets = find_all_planets()
    return jsonify({
        'planets': planets, # Then present this on react frontend, port 5000 -> 3000
    })

@app.route('/planets/add', methods=['POST'])
def add_planet():
    data = request.get_json()
    try:
        title = data['title']
        ticId = data['ticId']
        if data:
            data = add_planet_to_DB(title, ticId)
            planets = find_all_planets()
            return jsonify(data), 201
    except:
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')