import os
import uuid
import random
import string
import requests
import supabase
import lightkurve as lk
import matplotlib.pyplot as plt

# Initialize Supabase client with your Supabase credentials
supabase_url = 'https://qwbufbmxkjfaikoloudl.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk'
# Connect to supabase
supabase_client = supabase.Client(supabase_url, supabase_key)

# Define TIC IDs to retrieve lightcurves for
tic_ids = [
    'KOI-4878.01',
    'KOI-456.04',
    'KOI-3456.02',
    'KOI-5737.01',
    'KOI-5806.01',
    'KOI-5499.01',
    'KOI-2194.03',
    'KOI-6108.01',
    'KOI-5938.01',
    'KOI-5087.01',
    'KOI-5948.01',
    'KOI-5176.01',
    'KOI-5949.01',
    'KOI-5506.01',
    'KOI-6239.01',
    'KOI-5888.01',
    'KOI-5068.01',
    'KOI-5541.01',
    'KOI-5959.01',
    'KOI-5236.01',
    'KOI-5819.01',
    'KOI-5413.01',
    'KOI-5202.01',
    'KOI-1871.01',
    'KOI-5653.01',
    'KOI-5237.01',
    'KOI-6151.01',
    'KOI-5545.01',
]

# Define output directory
output_dir = 'output'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through TIC IDs and retrieve lightcurves
for tic_id in tic_ids:
    # Construct filename for the lightcurve
    filename = f"{tic_id}.png"
    # Construct path for the lightcurve image
    path = os.path.join(output_dir, filename)
    # Retrieve the lightcurve data for the TIC ID
    lc = lk.search_lightcurvefile(tic_id).download_all().stitch()
    # Plot the lightcurve and save the image
    plt.gcf().savefig(path)#lc.plot().savefig(path)
    # Retrieve radius and orbital period from lightcurve metadata
    radius = lc.meta.get('r_star')
    period = lc.meta.get('orbital_period')
    # Generate a unique ID for the planet
    planet_id = str(uuid.uuid4())
    # Construct data object to be inserted into Supabase table
    data = {
        'planetId': planet_id,
        'image': f"https://your-website.com/{filename}",
        'name': tic_id,
        'radius': radius,
        'orbital_period': period,
    }
    # Insert data into Supabase table
    supabase_client.table('lightcurves').insert(data)
