import os
import random
import uuid
import requests
from lightkurve import search_lightcurvefile
from supabase import create_client
from supabase.errors import ClientError

# Set up Supabase client
supabase_url = 'https://<your-project>.supabase.co'
supabase_key = '<your-anon-key>'
supabase = create_client(supabase_url, supabase_key)

# Create "planets" storage bucket if it doesn't exist
try:
    supabase.storage.create_bucket('planets')
except ClientError as e:
    if e.status_code != 409:
        raise e

# Function to upload light curve graph to Supabase storage
def upload_to_supabase(planet_id, image_path):
    # Create folder for planet in "planets" storage bucket
    folder_name = str(52 + planet_id) # Start folder iteration at 52
    supabase.storage.create_folder('planets', folder_name)
    # Upload light curve graph to folder
    with open(image_path, 'rb') as f:
        supabase.storage.upload(f'planets/{folder_name}/download.png', f.read())

# Loop to generate and upload data for multiple planets
for i in range(10): # Change this number to generate more or fewer planets
    # Generate random TIC ID
    koi_id = f"KOI-{random.randint(1000, 9999)}"
    # Search for light curve data for TIC ID using Lightkurve package
    lcf = search_lightcurvefile(koi_id).download()
    # Save light curve graph to file
    lc = lcf.PDCSAP_FLUX.normalize().remove_nans().flatten()
    fig = lc.plot()
    fig.savefig(f"output/{koi_id}.png")
    # Get planet name, radius, and orbital period from lightkurve object
    planet_name = lcf.target_name
    planet_radius = lcf.get_header()['PRADIUS']
    planet_period = lcf.get_header()['TPERIOD']
    # Upload data to Supabase table
    planet_id = 52 + i # Start planet iteration at 52
    data = {
        'planetId': str(uuid.uuid4()), # Generate UUID for planet ID
        'image': f'https://<your-project>.supabase.co/storage/v1/object/public/planets/{planet_id}/download.png',
        'name': planet_name,
        'radius': planet_radius,
        'orbital period': planet_period
    }
    supabase.table('planets').insert(data).execute()
    # Upload light curve graph to Supabase storage
    upload_to_supabase(planet_id, f"output/{koi_id}.png")
