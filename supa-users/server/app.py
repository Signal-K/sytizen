from flask import Flask, request
import os
from datetime import datetime, timezone
#from dotenv import load_dotenv
import requests
import psycopg2

# Database/table initialisation & Queries
CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
)

CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL, date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, data) VALUES (%s, %s, %s);"
)

GLOBAL_NUMBER_OF_DAYS = (
    """SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures;"""
)
GLOBAL_AVG = """SELECT AVG(temperature) as average FROM temperatures;"""

# Tables that will be used
CREATE_USER_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (user_id INTEGER, profileId TEXT, address TEXT);"
)

#INSERT_USER_RETURN_ID = "INSERT INTO users (profileId, address) VALUES (%s %s) RETURNING id;"

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, profileId TEXT);"
)

INSERT_USER_RETURN_ID = "INSERT INTO users (profileId) VALUES (%s) RETURNING id;"

# Flask + DB Connection
app = Flask(__name__)
DATABASE_URL = "postgresql://postgres:KBqI9fPB3h4mgFcU@db.afwwxlhknelxylrfvexi.supabase.co:5432/postgres"
connection = psycopg2.connect(DATABASE_URL)

# Routes
@app.get("/")
def home():
    return "Hello, World!"

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

@app.post("/api/user") # Post request to create a new user
def create_user():
    data = request.get_json() # dict of data from post request
    profileId = data["profileId"]
    with connection: # Start connection to db
        with connection.cursor() as cursor: # Object to manipulate entries in db
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER_RETURN_ID, (profileId,)) # Insert room & retrieve id
            profile_id = cursor.fetchone()[0] # access first column ([0])
    return {"id" : profile_id, "message": f"User {profileId} created."}, 201

"""@app.post("/api/user") # Post request to create a new user
def create_user():
    data = request.get_json()
    profileId = data["profileId"]
    address = data["address"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER_RETURN_ID, (profileId, address))
            user_id = cursor.fetchone()[0]
    return {"id": user_id, "message": f"User {profileId} created."}, 201"""

@app.post("/api/temperature") # Post request to add a new temperature reading for a room
def add_temperature(): # Currently not working!!
    data = request.get_json()
    temperature = data["temperature"]
    room_id = data["room"]

    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TEMPS_TABLE)
            cursor.execute(INSERT_TEMP, (room_id, temperature, date))
    
    return {"message": "Temperature added."}, 201

@app.get("/api/average") # Get request to calculate average temperatures
def get_global_avg():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GLOBAL_AVG) # Select average temperature of all temperatures in the table
            average = cursor.fetchone()[0]
            cursor.execute(GLOBAL_NUMBER_OF_DAYS)
            days = cursor.fetchone()[0]
    
    return {"average": round(average, 2), "days": days}

@app.route('/flask-user')
def current_user_flask():
    requestUrl = 'https://authapi.moralis.io/challenge/request/evm'
    requestPayload = {
        'resources': ["https://docs.moralis.io/"],
        "timeout": 15,
        "domain": "sytizen.vercel.app",
        "chainId": 1,
        "address": "0xa5f45F72702b3b7cFA6D2eaC8334F864B50FF367",
        "statement": "Please confirm",
        "uri": "https://defi.finance/",
        "expirationTime": "2020-01-01T00:00:00.000Z",
        "notBefore": "2020-01-01T00:00:00.000Z"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "kJfYYpmMmfKhvaWMdD3f3xMMb24B4MHBDDVrfjslkKgTilvMgdwr1bwKUr8vWdHH"
    }
    response = requests.post(requestUrl, json=requestPayload, headers=headers) # Run this output (or `response.text`) into function `create_user`!

    return(response.text)