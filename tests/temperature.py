import random
import time
from datetime import datetime
import lightkurve as lk
from supabase_py import create_client

# Define your Supabase credentials
supabase_url = 'https://qwbufbmxkjfaikoloudl.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk'
# Connect to supabase

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# List of TIC IDs
tic_ids = [
    'KOI-4878', 'KOI-3456', 'KOI-5737', 'KOI-5806', 'KOI-5499', 'KOI-2194',
    'KOI-6108', 'KOI-5938', 'KOI-5087', 'KOI-5948', 'KOI-5176', 'KOI-5949',
    'KOI-5506', 'KOI-6239', 'KOI-5888', 'KOI-5068', 'KOI-5541', 'KOI-5959',
    'KOI-5236', 'KOI-5819', 'KOI-5413', 'KOI-5202', 'KOI-1871', 'KOI-5653',
    'KOI-5237', 'KOI-6151', 'KOI-5545'
]

# Loop through each TIC ID
for tic_id in tic_ids:
    # Set the ticId value to the current TIC ID
    tic_id_value = tic_id

    # Generate a random planet name
    planet_name = random.choice(['Alderaan', 'Tatooine', 'Hoth', 'Endor', 'Naboo'])

    # Set the 'content' value to the random planet name
    content_value = planet_name

    # Set 'owner' to null
    owner_value = None

    # Set 'id' value to 58
    id_value = 58

    # Set 'media' value to an empty array
    media_value = []

    # Estimate the radius of the TIC ID using lightkurve
    search_result = lk.search_lightcurvefile(f'TIC {tic_id}')
    if search_result:
        lc_file = search_result.download(quality_bitmask='hardest')
        lc = lc_file.PDCSAP_FLUX.normalize().remove_nans().remove_outliers()
        periodogram = lc.to_periodogram(method='bls', period=np.arange(1, 10, 0.01))
        best_fit = periodogram.get_best_fit()
        estimated_radius = best_fit.rp

        # Set the 'radius' value to the estimated radius
        radius_value = estimated_radius
    else:
        # If the TIC ID is not found, set the 'radius' value to None
        radius_value = None

    # Set the 'cover' value
    cover_value = f'https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planets/{planet_name.lower()}_cover.png'

    # Set the 'avatar_url' value
    avatar_url_value = f'https://qwbufbmxkjfaikoloudl.supabase.co/storage/v1/object/public/planets/{planet_name.lower()}_avatar.png'

    # Set the 'contract' value to null
    contract_value = None

    # Estimate the orbital period
    estimated_orbital_period = 1.0  # Replace with your own method to estimate orbital period

    # Set the 'orbital_period' value to the estimated orbital period
    orbital_period_value = estimated_orbital_period

    # Define the data for the new row
    data = {
        'ticId': tic_id_value,
        'content': content_value,
        'owner': owner_value,
        'id': id_value,
        'media': media_value,
        'radius': radius_value,
        'cover': cover_value,
        'avatar_url': avatar_url_value,
        'contract': contract_value,
        'orbital_period': orbital_period_value
    }

    # Insert the new row into the 'planetsss' table
    supabase.table('planetsss').insert([data]).execute()

    # Wait for a brief moment to avoid rate limiting
    time.sleep(1)

print('Data insertion completed.')