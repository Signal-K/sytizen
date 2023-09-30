import numpy as np
from astroquery.mast import Catalogs
from astropy import units as u
from astropy.coordinates import SkyCoord

def get_star_info(tic_id):
    # Query the TIC catalog for star information
    result = Catalogs.query_criteria(catalog="Tic", ID=tic_id)
    
    if len(result) == 0:
        return "No information found for the given TIC ID."

    # Extract relevant information
    star = result[0]
    metallicity = star['Teff']
    luminosity = star['lum']
    mass = star['mass']
    color = star['Tmag']
    # star_type = star['StarType']

    return {
        "Metallicity (Teff)": metallicity,
        "Luminosity (lum)": luminosity,
        "Mass (mass)": mass,
        "Color (Tmag)": color,
        # "Star Type": star_type
    }

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