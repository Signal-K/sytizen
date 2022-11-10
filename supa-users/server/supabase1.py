from supabase import create_client, Client

url = "https://afwwxlhknelxylrfvexi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmd3d4bGhrbmVseHlscmZ2ZXhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjY0MzQ4MTgsImV4cCI6MTk4MjAxMDgxOH0.gk1F8Br9__04cvzqYIeeQ-U08KATiHovAw3r3ofNGAo"

supabase: Client = create_client(url, key)

def find_all_planets():
    data = supabase.table("Planets").select("*").execute()
    return data['data']

Planets = find_all_planets()
print(Planets)