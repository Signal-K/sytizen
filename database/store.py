import os
from supabase_py import client, create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")

url = "https://afwwxlhknelxylrfvexi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmd3d4bGhrbmVseHlscmZ2ZXhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjY0MzQ4MTgsImV4cCI6MTk4MjAxMDgxOH0.gk1F8Br9__04cvzqYIeeQ-U08KATiHovAw3r3ofNGAo"

supabase: client = create_client(url, key)

# Function to retrieve planet data from supa
def find_all_planets(): # Right now this is just demo data, we'll push this data to Supa from Lightkurve later
    data = supabase.table("Planets").select("*").execute()
    return data['data']

planets = find_all_planets()
print(planets)

# Function to add a new planet to the store/supa
def add_planet_to_DB(title) -> dict: # See `models/TIC.py`
    planet = {
        "title": title,
    }
    data = supabase.table("Planets").insert(planet).execute()

    return data['data']