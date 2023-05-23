from .connection import supabase

# Function to retrieve planet data from supa
def find_all_planets(): # Right now this is just demo data, we'll push this data to Supa from Lightkurve later
    data = supabase.table("Planets").select("*").execute()
    return data['data']

planets = find_all_planets()
print(planets)

# Function to add a new planet to the store/supa
def add_planet_to_DB(title, ticId) -> dict: # See `models/TIC.py`
    planet = {
        "title": title,
        "ticId": ticId,
    }
    data = supabase.table("Planetss").insert(planet).execute() # Planetsss table on "Testing Playground" project

    return data['data']