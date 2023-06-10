import os
import uuid
import lightkurve as lk
from lightkurve import search_targetpixelfile
import pandas as pd
from supabase import create_client
import matplotlib.pyplot as plt
import matplotlib

# Define the TIC IDs
#tic_ids = [
    #'KOI-4878',
    #'KOI-3456',
    # 'KOI-5737',
    # 'KOI-5806',
    # 'KOI-5499',
    # 'KOI-2194',
    # 'KOI-6108',
    # 'KOI-5938',
    # 'KOI-5087',
    # 'KOI-5948',
    # 'KOI-5176',
    # 'KOI-5949',
    # 'KOI-5506',
    # 'KOI-6239',
    # 'KOI-5888',
    # 'KOI-5068',
    # 'KOI-5541',
    # 'KOI-5959',
    # 'KOI-5236',
    # 'KOI-5819',
    # 'KOI-5413',
    # 'KOI-5202',
    # 'KOI-1871',
    # 'KOI-5653',
    # 'KOI-5237',
    # 'KOI-6151',
    # 'KOI-5545',
#]

matplotlib.use('Agg')

#TIC_IDS = ['KOI-5737', 'KOI-5806']#, 'KOI-5499', 'KOI-2194']
TIC_IDS = [ 'KOI-4878',
    'KOI-456',
    'KOI-3456',
    'KOI-5737',
    'KOI-5806',
    'KOI-5499']#,
    # 'KOI-2194',
    # 'KOI-6108',
    # 'KOI-5938',
    # 'KOI-5087',
    # 'KOI-5948',
    # 'KOI-5176',
    # 'KOI-5949',
    # 'KOI-5506',
    # 'KOI-6239',
    # 'KOI-5888',
    # 'KOI-5068',
    # 'KOI-5541',
    # 'KOI-5959',
    # 'KOI-5236',
    # 'KOI-5819',
    # 'KOI-5413',
    # 'KOI-5202',
    # 'KOI-1871',
    # 'KOI-5653',
    # 'KOI-5237',
    # 'KOI-6151',
    # 'KOI-5545', ]

# Initialize Supabase client with your Supabase credentials
supabase_url = 'https://qwbufbmxkjfaikoloudl.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk'
# Connect to supabase
supabase = create_client(supabase_url, supabase_key)
table_name = 'planetsss' # aka lightkurves

# Create output directory if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

# Loop over TIC ids
for tic_id in TIC_IDS:
    try:
        lc = lk.search_lightcurvefile(tic_id).download().PDCSAP_FLUX
        
        # Generate lightcurve plot
        fig, ax = plt.subplots()
        lc.plot(ax=ax)
        
        # Save lightcurve plot to disk
        filename = f'{tic_id}.png'
        filepath = os.path.join('output', filename)
        fig.savefig(filepath)
        
        # Upload data to Supabase
        planet_id = str(uuid.uuid4())
        image_url = f'https://yourwebsite.com/{filename}'
        name = tic_id
        radius = 1#'lc.header-radius'#"lc.header['radius']"
        period = 1#'lc.header-period'#"lc.header['period']"

        # Calculating temperature
        tpf = lk.search_targetpixelfile(tic_id).download()#, quarter=4).download() # Download target pixel file for the anomaly
        lctpf = tpf.to_lightkurve()
        lctpf_params = lctpf.estimate_stellar_parameters() #teff = tpf.estimate_stellar_parameters().effective_temperature.value # Estimate the effective temperature of the parent star"""
        tpf = lk.search_targetpixelfile(tic_id).download()
        lc = tpf.to_lightcurve().normalize()
        lctpf_params = tpf.get_lightcurve('PDCSAP_FLUX').estimate_stellar_parameters()
        # Estimate the temperature of the planet assuming a Bond albedo of 0.3
        a = tpf.pipeline_mask.sum() * tpf.pixel_scale_in_arcseconds # Planet area in square arcseconds
        d = tpf.target_distance # Distance to the star in parsecs
        r = 1.0 # Radius of the planet in Jupiter radii
        sigma_sb = 5.670374419e-08 # Stefan-Boltzmann constant in W/(m^2 K^4)
        t_planet = ((lctpf_params / 5777.0) ** 0.5) * ((1 - 0.3) ** 0.25) * ((r * 69.911e6))#teff / 5777.0) ** 0.5) * ((1 - 0.3) ** 0.25) * ((r * 69.911e6))"""
        
        supabase.table('planetsss').insert({
            #'id': tic_id,
            #'image': 'https://deepnote.com/workspace/star-sailors-49d2efda-376f-4329-9618-7f871ba16007/project/Star-Sailors-Light-Curve-Plot-b4c251b4-c11a-481e-8206-c29934eb75da/%2Foutput%2F',# + str(tic_id), + '.png'#image_url,
            'content': name,
            'radius': radius,
            'orbital_period': period,
            'temperature': 1,# t_planet,
            'contract': '',
        }).execute()
        
        print(f'Successfully processed {tic_id}')
        
    except Exception as e:
        print(f'Error processing {tic_id}: {e}')