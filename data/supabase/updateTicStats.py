# A script to look through your supabase `planetsss` table (assuming your Star Sailors instance is the same as ours) and update its star stats based on tic id
import os
from supabase import create_client, Client
from astroquery.mast import Catalogs

# Initialize Supabase client
url = "https://qwbufbmxkjfaikoloudl.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY2OTk0MTc1OSwiZXhwIjoxOTg1NTE3NzU5fQ.YEicNFgQ3DolbXQVBRMrbqoJS3qLDEf5TKJ8dphZRRc"
supabase = create_client(url, key)

# Function to update a row with star information
def update_star_info(row):
    tic_id = row['ticId']
    
    # Fetch star information using the TIC ID
    result = Catalogs.query_criteria(catalog="Tic", ID=tic_id)
    
    if len(result) > 0:
        star = result[0]
        metallicity = star['Teff']
        luminosity = star['lum']
        mass = star['mass']
        color = star['Tmag']
        
        # Update the row with star information
        data, count = supabase.table('planetsss') \
            .update({'Metallicity': metallicity, 'Luminosity': luminosity, 'Mass': mass, 'Color': color}) \
            .eq('id', row['id']) \
            .execute()

        if count == 1:
            print(f"Updated row {row['id']} with star information.")
        else:
            print(f"Failed to update row {row['id']}.")
    else:
        print(f"No information found for TIC ID {tic_id}.")

# Retrieve all rows from the 'planetsss' table
response = supabase.table('planetsss').select("*").execute()

print(response)

if response.status_code == 200:
    rows = response.data  # Access the data using response.data

    for row in rows:
        try:
            update_star_info(row)
        except Exception as e:
            print(f"Error updating row {row['id']}: {str(e)}")
else:
    print(f"Failed to fetch data from 'planetsss' table: {response.status_code} - {response.error}")