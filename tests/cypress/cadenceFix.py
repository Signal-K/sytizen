import random
import uuid
import os
import urllib.request
from supabase import create_client
from lightkurve import search_lightcurvefile, search_lightcurve

# Supabase credentials
supabase_url = 'https://qwbufbmxkjfaikoloudl.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk'

# Output directory for saving lightcurve images
OUTPUT_DIR = 'output'

# Supabase table name
TABLE_NAME = 'lightkurves'

# Connect to Supabase
supabase = create_client(supabase_url, supabase_key)

# Search for lightcurve file
lcf = search_lightcurve('KOI-5737').download()

try:
    # Generate planet ID
    planet_id = str(uuid.uuid4())

    # Save lightcurve image to output directory
    filename = "KOI-5737.png"
    path = os.path.join(OUTPUT_DIR, filename)
    lcf.plot().figure.savefig(path)

    # Upload image to Supabase storage bucket
    
    supabase.storage().from_('lightkurves').upload('output/' + filename, file)
    #with open('output/' + filename, 'rb+') as f:
        #res = supabase.storage().from_('planets').upload(filename, os.path.abspath(filename))

    image_url = supabase.storage.upload(filename, image_data)

    # Insert data into Supabase table
    data = {
        'planetId': planet_id,
        'image': image_url.public_url,
        'name': 'KOI-5737',
        'radius': random.uniform(0.1, 1.0),
        'orbital_period': random.uniform(1, 100)
    }
    supabase.table(TABLE_NAME).insert(data).execute()

    print("Inserted planet KOI-5737")
except Exception as e:
    print(f"Failed to insert planet: {e}")