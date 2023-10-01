from flask import Flask, request, jsonify
import requests
import numpy as np
from astroquery.mast import Catalogs
from astropy import units as u
from astropy.coordinates import SkyCoord

app = Flask(__name__)

TIC_API_URL = "https://exo.mast.stsci.edu/api/v0.1/exoplanets/keplerid/"

@app.route("/get_star_info", methods=["POST"])
def get_star_info():
    tic_id = request.args.get("ticId")
    result = Catalogs.query_criteria(catalog='Tic', ID=tic_id) # Query the TIC catalogue based on the initial request

    try:
        if len(result) == 0:
            return "No information found for the given TIC ID"

        # Initial values for star info
        star = result[0]
        metallicity = star['Teff']
        luminosity = star['lum']
        mass = star['mass']
        color = star['Tmag']
        # star_type = star['StarType']

        """ return {
            "Metallicity (Teff)": metallicity,
            "Luminosity (lum)": luminosity,
            "Mass (mass)": mass,
            "Color (Tmag)": color,
            # "Star Type": star_type
        }"""

        star_info = get_star_info(tic_id)

        return jsonify(star_info)
    except Exception as e:
        return jsonify({"error": str(e)})


def get_stellar_parameters(tic_id):
    try:
        # Query the MAST catalog for stellar parameters
        result = Catalogs.query_criteria(catalog="Tic", ID=tic_id)

        if result is not None:
            # Extract relevant stellar parameters from the result
            star_name = result['TICID'][0]
            radius = result['rad'][0]  # Stellar radius
            metallicity = result['met'][0]  # Metallicity
            mass = result['mass'][0]  # Stellar mass
            density = result['rho'][0]  # Stellar density
            luminosity = result['lum'][0]  # Luminosity

            # Return the extracted data
            stellar_data = {
                "star_name": star_name,
                "radius": radius,
                "metallicity": metallicity,
                "mass": mass,
                "density": density,
                "luminosity": luminosity
            }
            return stellar_data
        else:
            return {"error": "Star not found in the MAST catalog"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)