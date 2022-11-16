from flask import Flask, jsonify, request
import time
import requests
import psycopg2

# App & Data configuration =====>
app = Flask(__name__)
DATABASE_URL = "postgresql://postgres:KBqI9fPB3h4mgFcU@db.afwwxlhknelxylrfvexi.supabase.co:5432/postgres"
connection = psycopg2.connect(DATABASE_URL)

# Table configuration =====>
CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
)

CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL, date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"

CREATE_PLANETS_TABLE = ( # If the planet table doesn't exist on Supabase
    "CREATE TABLE IF NOT EXISTS planets (planetId INTEGER PRIMARY KEY, profileId TEXT, planetName TEXT);"
) # Would be a good idea to double check that this configuration is aligned with https://skinetics.notion.site/Inventory-what-goes-where-1fb9b1e776c048ed9a9b5c1ff1def491

INSERT_PLANET_RETURN_ID = "INSERT INTO users (profileId) VALUES (%s) RETURNING id;"

CREATE_PLANETSDEMO_TABLE = ( # Demo table that is to test out the post request from flask to `add_planet` decorator
    "CREATE TABLE IF NOT EXISTS planetsdemo (planetId SERIAL PRIMARY KEY, name TEXT, moons INTEGER);"
)
INSERT_PLANETSDEMO = "INSERT INTO planetsdemo (name, moons) VALUES (%s, %s);"

@app.route('/time')
def get_time():
    return {'time': time.time()}

@app.route('/planets')
def planet():
    planets = [{'name': 'Mars', 'moons': 2}, {'name': 'Earth', 'moons': 1}]
    return jsonify({'planets' : planets})

# Example, working POST request to Supabase
@app.post("/api/room") # Post request to create a new room
def create_room():
    data = request.get_json() # dict of data from post request
    name = data["name"]
    with connection: # Start connection to db
        with connection.cursor() as cursor: # Object to manipulate entries in db
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID, (name,)) # Insert room & retrieve id
            room_id = cursor.fetchone()[0] # access first column ([0])
    return {"id" : room_id, "message": f"Room {name} created."}, 201

@app.post('/add_planets')
def add_planets():
    data = request.get_json()
    planetId = data['planetId'] # is this the primary key, or is it something else?
    #profileId = data['profileId'] # Magic id -> will be retrieved from the user id (if they have a magic account attached, otherwise use their supabase profile id)
    planetName = data['name'] # Other potential properties -> address, tokenId, holder (foreign key to user/profile ID), etc

    with connection:
        with connection.cursor() as cursor: # object to manipulate entries in database
            cursor.execute(CREATE_PLANETS_TABLE)
            cursor.execute(INSERT_PLANET_RETURN_ID, (planetId,)) # Insert planet & retrieve ID
            planet_id = cursor.fetchone()[0] # access first column ([0])
    return {"id" : planet_id, "message": f"User {planetId} created."}, 201

@app.post('/add_planet')
def add_planet():
    data = request.get_json()
    name = data['name']
    moons = data['moons']

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PLANETSDEMO_TABLE)
            cursor.execute(INSERT_PLANETSDEMO, (name, moons))