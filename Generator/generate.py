import random
import uuid
import os
import urllib.request
from supabase import create_client
from lightkurve import search_lightcurvefile

# Supabase credentials
supabase_url = 'https://qwbufbmxkjfaikoloudl.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk'
#supabase = create_client(supabase_url, supabase_key)

# Output directory for saving lightcurve images
OUTPUT_DIR = 'output'

# Supabase table name
TABLE_NAME = 'lightkurves'

# Connect to Supabase
supabase = create_client(supabase_url, supabase_key)

# Generate random TIC IDs
tic_ids = ['KOI-' + str(random.randint(1000, 9999)) for i in range(5)]

# Loop over TIC IDs
for tic_id in tic_ids:
    try:
        # Search for lightcurve file
        lcf = search_lightcurvefile(tic_id).download()
        
        # Generate planet ID
        planet_id = str(uuid.uuid4())
        
        # Save lightcurve image to output directory
        filename = f"{tic_id}.png"
        path = os.path.join(OUTPUT_DIR, filename)
        lcf.plot().savefig(path)
        
        # Upload image to Supabase storage bucket
        with open(path, 'rb') as f:
            image_data = f.read()
        image_url = supabase.storage.from_filename(filename).upload(image_data)
        
        # Insert data into Supabase table
        data = {
            'planetId': planet_id,
            'image': image_url.public_url,
            'name': tic_id,
            'radius': random.uniform(0.1, 1.0),
            'orbital_period': random.uniform(1, 100)
        }
        supabase.table(TABLE_NAME).insert(data).execute()
        
        print(f"Inserted planet {tic_id}")
    except:
        print(f"Failed to insert planet {tic_id}")
