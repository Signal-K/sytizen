from supabase_py import client, create_client
import os

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_ANON_KEY")

url = "https://afwwxlhknelxylrfvexi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFmd3d4bGhrbmVseHlscmZ2ZXhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjY0MzQ4MTgsImV4cCI6MTk4MjAxMDgxOH0.gk1F8Br9__04cvzqYIeeQ-U08KATiHovAw3r3ofNGAo"

supabase: client = create_client(url, key)