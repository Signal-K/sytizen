import numpy as np
from astroquery.mast import Catalogs
from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia

def get_star_info(tic_id):
    # Query the TIC catalog for star information
    result = Catalogs.query_criteria(catalog="Tic", ID=tic_id)
    
    if len(result) == 0:
        return "No information found for the given TIC ID."

    # Extract relevant information
    star = result[0]
    luminosity = star['lum']
    mass = star['mass']
    color = star['Tmag']
    temperature = star['Teff']
    # star_type = star['StarType']
    # metallicity = star['Teff']
    # metallicity = result[0]['[Fe/H]']

    return {
        "Metallicity (Teff)": metallicity,
        "Luminosity (lum)": luminosity,
        "Mass (mass)": mass,
        "Color (Tmag)": color,
        # "Star Type": star_type
    } # https://www.notion.so/skinetics/Unity-Randomisation-LightKurve-via-Flask-fac86634e02f4086b7c936c83e66f79a?pvs=4

def get_metallicity_from_gaia(tic_id):
    query = f"SELECT metallicity FROM gaiadr2.gaia_source WHERE source_id = {tic_id}"
    job = Gaia.launch_job(query)
    result = job.get_results()
    
    if len(result) == 0:
        return "No information found for the given TIC ID."

    metallicity = result['metallicity'][0]

    return {
        "Metallicity": metallicity,
    }

# Example usage:
tic_id = 55525572 
metallicity_info = get_metallicity_from_gaia(tic_id)
print(metallicity_info)

if __name__ == "__main__":
    # Input the TIC ID
    tic_id = input("Enter a TIC ID: ")

    # Call the function to retrieve star information
    star_info = get_star_info(tic_id)
    
    # Display the retrieved information
    if isinstance(star_info, dict):
        for key, value in star_info.items():
            print(f"{key}: {value}")
    else:
        print(star_info)