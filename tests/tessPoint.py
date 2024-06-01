from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import numpy as np
from astroquery.mast import Catalogs
from astropy import units as u
from astropy.coordinates import SkyCoord
import lightkurve as lk

app = Flask(__name__)
CORS(app, resources={r"/get_star_info": {"origins": "http://localhost:3000"}})

TIC_API_URL = "https://exo.mast.stsci.edu/api/v0.1/exoplanets/keplerid/"

def estimate_planet_radius(tic_id):
    # Retrieve light curve data using lightkurve
    lc = lk.search_lightcurvefile(target=f"TIC {tic_id}", mission="TESS").download()

    # Estimate planet radius
    radius_estimate = lc.estimate_radius()

    return {"radius_estimate": radius_estimate}

@app.route("/estimate_planet_radius", methods=["POST"])
def estimate_planet_radius_route():
    try:
        tic_id = request.json.get("ticId")  # Assuming JSON data with a "ticId" field

        result = estimate_planet_radius(tic_id)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

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

@app.route("/get_star_info", methods=["POST"])
def get_star_info_route():
    try:
        # Get the TIC ID from the POST request data
        tic_id = request.json.get("ticId")
        
        # Call the function to retrieve star information
        star_info = get_star_info(tic_id)
        
        # Return the retrieved information as JSON response
        return jsonify(star_info)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

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

@app.route("/generate_sector_plot", methods=["POST"])
def generate_sector_plot():
    try:
        tic_id = request.json.get("ticId")
        lc = lk.search_lightcurvefile(target=f"TIC {tic_id}", mission="TESS").download()
        lc.plot() # Generate a simple Lightkurve plot

        plot_filename = "/output/{tic_id}.png"
        plt.savefig(plot_filename)
        plt.close()

        # Return the path to the saved plot
        return jsonify({"plot_path": plot_filename})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)